// src/api/parser.ts

// ==============================================================================
// PARSER API
// ==============================================================================
// This module is a thin façade over the Transport layer.
// All HTTP/communication details live in src/services/transport.ts.
// The store imports `fetchAst` from here — it does not need to know whether
// the transport is HTTP, VSCode postMessage, or Pyodide.

import { transport } from "../services/transport";
import type { Program } from "../types/ast";

/**
 * Sends Regia source code to the compiler backend and returns the parsed AST.
 *
 * @param sourceCode - The raw Regia script text.
 * @returns A promise that resolves to the parsed `Program` AST.
 * @throws A `TransportError` object if parsing fails or the server is unavailable.
 *         The store in `useStore.ts` handles this error and formats it for display.
 */
export const fetchAst = (sourceCode: string): Promise<Program> => {
    return transport.parse(sourceCode);
};