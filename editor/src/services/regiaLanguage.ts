// src/services/regiaLanguage.ts

import type * as MonacoType from "monaco-editor";

// ==============================================================================
// REGIA CUSTOM THEME
// Derived directly from the CSS design tokens in src/index.css.
// All hex values here must be kept in sync with the :root variables.
// ==============================================================================

/** Maps the app's design token palette onto a Monaco editor theme. */
const REGIA_THEME: MonacoType.editor.IStandaloneThemeData = {
    base: "vs-dark",
    inherit: false,
    rules: [
        // === Structural keywords (ACTION, EVENT, FACT, PLAYBOOK, PLOT, PHASE, ROLE)
        { token: "keyword.declaration", foreground: "7c7cff", fontStyle: "bold" },
        // === Flow keywords (DURING, WHEN, IF, ELSE, ON, ENTER, EXIT, TRANSITION, TO)
        { token: "keyword.flow", foreground: "9898ff" },
        // === Action keywords (DO, ASSIGN, UNASSIGN, WORLD, SIGNAL, START, SUBPLOT, END, MAPPING)
        { token: "keyword.action", foreground: "4ade80" },
        // === Special built-in actions (TELL, BROADCAST, ACHIEVE, BELIEVE, FORGET, PRINT)
        { token: "keyword.builtin", foreground: "4ade80", fontStyle: "italic" },
        // === Modifiers (PRIORITY, TEMPER, EFFECTS, INITIAL, SELF, IMPORT, FROM)
        { token: "keyword.modifier", foreground: "9898b8" },
        // === Identifiers (PascalCase = type/playbook/plot names)
        { token: "identifier.type", foreground: "e2e2f0", fontStyle: "bold" },
        // === Identifiers (lowercase = actions, events, facts)
        { token: "identifier", foreground: "c8c8e0" },
        // === Numbers (priority values, temper floats)
        { token: "number", foreground: "f4b8e4" },
        // === Strings (PRINT arguments)
        { token: "string", foreground: "a6d189" },
        // === Doc Comments (#@..., #-...)
        { token: "comment.doc", foreground: "9898b8", fontStyle: "italic" },
        // === Normal Comments (#...)
        { token: "comment", foreground: "5a5a7a", fontStyle: "italic" },
        // === Punctuation (. : , ( ))
        { token: "delimiter", foreground: "5a5a7a" },
    ],
    colors: {
        // Editor backgrounds
        "editor.background":              "#1a1a2a",  // --color-bg-editor
        "editor.foreground":              "#e2e2f0",  // --color-text-primary
        // Line number gutter
        "editorLineNumber.foreground":    "#5a5a7a",  // --color-text-muted
        "editorLineNumber.activeForeground": "#9898b8", // --color-text-secondary
        // Current line highlight
        "editor.lineHighlightBackground": "#2a2a3e",  // --color-bg-surface
        "editor.lineHighlightBorder":     "#2a2a3e",
        // Selection
        "editor.selectionBackground":     "#7c7cff44",// --color-accent-primary at 27% opacity
        "editor.inactiveSelectionBackground": "#7c7cff22",
        // Cursor
        "editorCursor.foreground":        "#7c7cff",  // --color-accent-primary
        // Scrollbar
        "scrollbarSlider.background":     "#5a5a7a55",
        "scrollbarSlider.hoverBackground":"#7c7cff88",
        "scrollbarSlider.activeBackground":"#7c7cff",
        // Widget backgrounds (find, hover)
        "editorWidget.background":        "#2a2a3e",  // --color-bg-surface
        "editorWidget.border":            "#3a3a55",  // --color-border
        // Error / warning squiggle underlines use Monaco defaults (red/yellow)
        // so we do not override them here.
        // Overview ruler (the minimap-side error indicator bar)
        "editorOverviewRuler.border":     "#2a2a3e",
    },
};

// ==============================================================================
// MONARCH TOKENIZER
// A state-machine lexer that classifies each token in a Regia source file.
// ==============================================================================

const MONARCH_LANGUAGE: MonacoType.languages.IMonarchLanguage = {
    // Keywords grouped by semantic role for fine-grained theming
    declarationKeywords: [
        "ACTION", "EVENT", "FACT", "PLAYBOOK", "PLOT",
        "PHASE", "ROLE", "IMPORT",
    ],
    flowKeywords: [
        "DURING", "WHEN", "IF", "ELSE", "ON", "ENTER",
        "EXIT", "TRANSITION",
    ],
    actionKeywords: [
        "DO", "ASSIGN", "UNASSIGN", "WORLD", "SIGNAL",
        "START", "SUBPLOT", "END", "MAPPING", "TO",
    ],
    builtinKeywords: [
        "TELL", "BROADCAST", "ACHIEVE", "BELIEVE", "FORGET", "PRINT",
    ],
    modifierKeywords: [
        "PRIORITY", "TEMPER", "EFFECTS", "INITIAL", "SELF",
        "FROM", "AND", "OR", "NOT",
    ],

    tokenizer: {
        root: [
            // === Doc Comments: #@ or #- to end of line
            [/#[@-].*$/, "comment.doc"],

            // === Normal Comments: # to end of line
            [/#.*$/, "comment"],

            // === Strings: "..."
            [/"([^"\\]|\\.)*$/, "string.invalid"],
            [/"/, { token: "string.quote", bracket: "@open", next: "@string" }],

            // === Numbers: integer or float
            [/\d+\.\d+/, "number.float"],
            [/\d+/, "number"],

            // === Keywords and identifiers
            [/[A-Z][a-zA-Z0-9_]*/, {
                cases: {
                    "@declarationKeywords": "keyword.declaration",
                    "@flowKeywords":        "keyword.flow",
                    "@actionKeywords":      "keyword.action",
                    "@builtinKeywords":     "keyword.builtin",
                    "@modifierKeywords":    "keyword.modifier",
                    "@default":             "identifier.type",
                },
            }],
            [/[a-z][a-zA-Z0-9_]*/, "identifier"],

            // === Punctuation
            [/[.:,]/, "delimiter"],
            [/[()]/, "delimiter.parenthesis"],

            // === Whitespace
            [/\s+/, "white"],
        ],

        string: [
            [/[^\\"]+/, "string"],
            [/\\./,     "string.escape"],
            [/"/,       { token: "string.quote", bracket: "@close", next: "@pop" }],
        ],
    },
};

// ==============================================================================
// LANGUAGE CONFIGURATION
// Enables comment toggling, bracket matching, and auto-closing pairs.
// ==============================================================================

const LANGUAGE_CONFIG: MonacoType.languages.LanguageConfiguration = {
    comments: {
        lineComment: "#",
    },
    brackets: [["(", ")"]],
    autoClosingPairs: [
        { open: "(", close: ")" },
        { open: '"', close: '"', notIn: ["string", "comment"] },
    ],
    surroundingPairs: [
        { open: "(", close: ")" },
        { open: '"', close: '"' },
    ],
};

// ==============================================================================
// REGISTRATION
// Call this once before the Monaco editor mounts.
// ==============================================================================

/** The Monaco language ID for Regia source files. */
export const REGIA_LANGUAGE_ID = "regia";

/** The Monaco theme ID for the Regia editor. */
export const REGIA_THEME_ID = "regia-dark";

/**
 * Registers the Regia language definition and custom theme with Monaco.
 *
 * Must be called once inside the `beforeMount` callback of <Editor>.
 * Subsequent calls are safe (Monaco ignores duplicate registrations).
 *
 * @param monaco - The Monaco API object provided by @monaco-editor/react.
 */
export const registerRegiaLanguage = (
    monaco: typeof MonacoType,
): void => {
    monaco.languages.register({ id: REGIA_LANGUAGE_ID });
    monaco.languages.setMonarchTokensProvider(REGIA_LANGUAGE_ID, MONARCH_LANGUAGE);
    monaco.languages.setLanguageConfiguration(REGIA_LANGUAGE_ID, LANGUAGE_CONFIG);
    monaco.editor.defineTheme(REGIA_THEME_ID, REGIA_THEME);
};
