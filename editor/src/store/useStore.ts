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
    code: string;
    ast: Program | null;
    isParsing: boolean;
    /** Human-readable error strings derived from `compilerMessages`. */
    errors: string[];
    /** Structured compiler diagnostics with precise line/column info for Monaco markers. */
    compilerMessages: CompilerMessage[];
    setCode: (newCode: string) => void;
    parseCode: () => Promise<void>;
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
ACTION walk(ARG1).
ACTION speak(ARG1, ARG2).
ACTION hide.

EVENT start_scene.
EVENT timer_ticked.
EVENT danger_spotted.
EVENT safe_again.

FACT has_weapon.
FACT health_low.
FACT is_daytime.

PLAYBOOK PbExplore:
    WHEN start_scene:
        DO PRINT("Exploration started").
        DO BELIEVE(has_weapon).
    
    WHEN danger_spotted PRIORITY 8:
        DO hide.
        IF has_weapon AND NOT (health_low):
            DO speak("threat", "Charge!").
            SIGNAL timer_ticked.
        IF health_low OR NOT (is_daytime):
            DO PRINT("Too weak to fight").
            SIGNAL safe_again.
        ELSE:
            DO FORGET(has_weapon).

PLAYBOOK PbCombat:
    WHEN timer_ticked:
        DO speak(attack_cry, "Charge!").
        IF has_weapon:
            DO walk(forward).

PLOT GrandTest.
    PHASE peace INITIAL.
    PHASE battle.
    
    ROLE Hero.
    
    DURING peace:
        WHEN danger_spotted:
            IF NOT (is_daytime):
                TRANSITION TO battle.
        
        ON ENTER:
            WORLD DO PRINT("Peace begins").
            ASSIGN PbExplore TO Hero.
            Hero DO speak(greetings, "Hello world").
            
        ON EXIT:
            UNASSIGN PbExplore FROM Hero.
            Hero DO walk(away).
            
        WHEN timer_ticked PRIORITY 2:
            WORLD DO BROADCAST(start_scene).
            
    DURING battle:
        WHEN safe_again:
            TRANSITION TO peace.
        
        ON ENTER:
            ASSIGN PbCombat TO Hero.
            WORLD DO PRINT("Battle begins").

    DURING PLOT:
        WHEN start_scene:
            WORLD DO PRINT("Plot is starting!").

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
    code: INITIAL_CODE,
    ast: null,
    isParsing: false,
    errors: [],
    compilerMessages: [],

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

        set({ isParsing: true, errors: [], compilerMessages: [] });

        try {
            const parsedAst = await fetchAst(code);
            set({ ast: parsedAst, isParsing: false, compilerMessages: [] });

        } catch (error) {
            // The transport layer throws a TransportError object on failure.
            // We cast and extract the structured messages, falling back to a
            // generic message if the error is of an unexpected shape.
            const transportError = error as TransportError;

            let errorMessages: string[];
            let compilerMessages: CompilerMessage[] = [];

            if (transportError.messages && transportError.messages.length > 0) {
                // Preserve the full structured messages for Monaco inline markers,
                // and derive the flat string list for backward compatibility.
                compilerMessages = transportError.messages;
                errorMessages = compilerMessages.map((msg) => msg.message);
            } else if (transportError.message) {
                errorMessages = [transportError.message];
            } else {
                errorMessages = ["An unknown error occurred while parsing."];
            }

            set({ ast: null, errors: errorMessages, compilerMessages, isParsing: false });
        }
    },
}));