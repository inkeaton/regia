// src/types/transport.ts

// ==============================================================================
// TRANSPORT TYPES
// ==============================================================================
// These types define the shape of messages between the editor frontend and the
// Regia compiler backend. They are deliberately decoupled from the HTTP fetch
// API so that switching to VSCode postMessage or Pyodide requires only a new
// Transport implementation, not changes to these types.

import type { Program } from "./ast";

/**
 * The payload sent to the backend when requesting a parse.
 */
export type ParseRequest = {
    source_code: string;
};

/**
 * A successful parse response.
 * The backend returns a `Program` AST JSON directly as the response body.
 */
export type ParseResponse = Program;

/**
 * A single compiler diagnostic message returned on parse failure.
 */
export type CompilerMessage = {
    /** The human-readable error description. */
    message:  string;
    /** Severity level as a string (e.g. "ERROR", "WARNING"). */
    severity: string;
    /** Source filename. */
    filename: string;
    /** 1-based line number, or 0 if unknown. */
    line:     number;
    /** 1-based column number, or 0 if unknown. */
    column:   number;
};

/**
 * A transport-level error. Contains parsed compiler messages when available.
 */
export type TransportError = {
    /** Human-readable error message for display. */
    message:  string;
    /** Structured compiler messages if the backend returned them. */
    messages: CompilerMessage[];
};
