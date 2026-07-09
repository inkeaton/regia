// src/store/useStore.ts
import { create } from "zustand";

import { fetchAst } from "../api/parser";
import type { Program } from "../types/ast";
import type { TransportError } from "../types/transport";

// ==============================================================================
// STATE TYPES
// ==============================================================================

/**
 * The complete shape of the global application state.
 *
 * State fields:
 * @property code       - The current raw Regia source code string.
 * @property ast        - The last successfully parsed AST, or null.
 * @property isParsing  - True while a parse request is in flight.
 * @property errors     - Human-readable error strings from the last failed parse.
 *
 * Actions:
 * @property setCode    - Update the code string (does NOT trigger a parse automatically).
 * @property parseCode  - Send the current code to the backend. Debounced in CodeEditor.
 */
export type EditorState = {
    code:       string;
    ast:        Program | null;
    isParsing:  boolean;
    errors:     string[];
    setCode:    (newCode: string) => void;
    parseCode:  () => Promise<void>;
};

// ==============================================================================
// CONSTANTS
// ==============================================================================

/**
 * The example code shown on first load (playground mode).
 * In VSCode extension mode, this will be replaced by the active file's content
 * injected via the transport layer.
 */
const INITIAL_CODE = `\
EVENT time_to_start.
EVENT song_ends.
EVENT technical_failure.

PLOT Concert.
    PHASE backstage INITIAL.
    PHASE performing.
    PHASE aftermath.

    DURING backstage:
        TRANSITION TO performing WHEN time_to_start.

    DURING performing:
        TRANSITION TO aftermath WHEN song_ends.
        TRANSITION TO backstage WHEN technical_failure.
`;

// ==============================================================================
// STORE IMPLEMENTATION
// ==============================================================================

/**
 * Global Zustand store for the Regia editor.
 * Manages source code, the parsed AST, loading state, and error messages.
 *
 * Usage:
 *   const { code, ast, errors } = useStore();
 */
export const useStore = create<EditorState>((set, get) => ({
    code:      INITIAL_CODE,
    ast:       null,
    isParsing: false,
    errors:    [],

    /**
     * Updates the raw code string in the state.
     * Does NOT trigger a parse. Parsing is debounced in CodeEditor.tsx
     * to avoid excessive backend calls while the user is typing.
     */
    setCode: (newCode: string) => {
        set({ code: newCode });
    },

    /**
     * Sends the current code to the backend parser via the transport layer.
     * On success: stores the new AST and clears errors.
     * On failure: clears the AST and stores formatted error strings.
     */
    parseCode: async () => {
        const { code } = get();

        // Early return if the editor is empty.
        if (!code.trim()) {
            set({ ast: null, errors: [] });
            return;
        }

        set({ isParsing: true, errors: [] });

        try {
            const parsedAst = await fetchAst(code);
            set({ ast: parsedAst, isParsing: false });

        } catch (error) {
            // The transport layer throws a TransportError object on failure.
            // We cast and extract the structured messages, falling back to a
            // generic message if the error is of an unexpected shape.
            const transportError = error as TransportError;

            let errorMessages: string[];

            if (transportError.messages && transportError.messages.length > 0) {
                // Format each structured compiler message into a readable string.
                errorMessages = transportError.messages.map((msg) => msg.message);
            } else if (transportError.message) {
                errorMessages = [transportError.message];
            } else {
                errorMessages = ["An unknown error occurred while parsing."];
            }

            set({ ast: null, errors: errorMessages, isParsing: false });
        }
    },
}));