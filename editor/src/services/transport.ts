// src/services/transport.ts

// ==============================================================================
// TRANSPORT ABSTRACTION
// ==============================================================================
// A Transport is the communication layer between the editor frontend and the
// Regia compiler backend.
//
// The interface is kept deliberately minimal so that swapping the underlying
// mechanism (HTTP fetch → VSCode postMessage → Pyodide WASM) requires only:
//   1. Writing a new class that implements Transport.
//   2. Updating `createTransport()` to return it.
//
// No other file in the application needs to change.

import type { Program } from "../types/ast";
import type { CompilerMessage, TransportError } from "../types/transport";

// ==============================================================================
// TRANSPORT INTERFACE
// ==============================================================================

/**
 * Defines the communication contract between the editor and the backend.
 * All transport implementations must satisfy this interface.
 */
export interface Transport {
    /**
     * Send Regia source code to the backend for parsing.
     *
     * @param sourceCode - The raw Regia script text.
     * @returns A promise that resolves to the parsed AST Program.
     * @throws A `TransportError` if parsing fails or the backend is unavailable.
     */
    parse(sourceCode: string): Promise<Program>;

    // NOTE: `emitRegia(ast: Program): Promise<string>` will be added here
    // when the reverse-sync (graph → code) feature is implemented.
    // The server-side endpoint will be: POST /emit-regia
}

// ==============================================================================
// HTTP TRANSPORT (current implementation)
// ==============================================================================

/** The base URL for the local FastAPI server. Change this if the port changes. */
const HTTP_API_BASE_URL = "http://127.0.0.1:8000";

/**
 * Transport implementation that communicates with the local Python FastAPI server
 * via standard HTTP fetch calls.
 *
 * This is the only transport used in the standalone prototype.
 * In the VSCode extension, it will be replaced by a VscodeTransport that
 * uses the `vscode.postMessage` / `window.addEventListener("message")` API.
 */
class HttpTransport implements Transport {
    private readonly baseUrl: string;

    /**
     * @param baseUrl - The base URL of the FastAPI server. Defaults to localhost:8000.
     */
    constructor(baseUrl: string = HTTP_API_BASE_URL) {
        this.baseUrl = baseUrl;
    }

    /** @inheritdoc */
    async parse(sourceCode: string): Promise<Program> {
        let response: Response;

        try {
            response = await fetch(`${this.baseUrl}/parse`, {
                method:  "POST",
                headers: { "Content-Type": "application/json" },
                body:    JSON.stringify({ source_code: sourceCode }),
            });
        } catch {
            // Network failure (server not running, CORS, etc.)
            // We intentionally discard the raw network error and produce a
            // user-friendly message instead.
            const err: TransportError = {
                message:  "Cannot reach the Regia server. Is it running on port 8000?",
                messages: [],
            };
            throw err;
        }

        if (response.ok) {
            return (await response.json()) as Program;
        }

        // The FastAPI server returns compiler errors as:
        // { "detail": [ { message, severity, filename, line, column }, ... ] }
        const errorBody = await response.json().catch(() => ({}));
        const rawMessages: CompilerMessage[] = Array.isArray(errorBody.detail)
            ? errorBody.detail
            : [];

        const err: TransportError = {
            message:  `Parse failed with ${rawMessages.length} error(s).`,
            messages: rawMessages,
        };
        throw err;
    }
}

// ==============================================================================
// FACTORY FUNCTION
// ==============================================================================

/**
 * Creates and returns the appropriate Transport for the current environment.
 *
 * Currently always returns an `HttpTransport`.
 * In the future, this function can detect whether it is running inside a VSCode
 * WebView (by checking for `window.acquireVsCodeApi`) and return a different
 * implementation accordingly.
 *
 * @returns The active Transport instance.
 */
export const createTransport = (): Transport => {
    // Future: if (typeof window.acquireVsCodeApi !== "undefined") return new VscodeTransport();
    return new HttpTransport();
};

/**
 * The singleton transport instance used throughout the application.
 * Import this in api/parser.ts and the store — do not call `createTransport()`
 * in multiple places.
 */
export const transport = createTransport();
