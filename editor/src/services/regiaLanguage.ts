// src/services/regiaLanguage.ts

import type * as MonacoType from "monaco-editor";

// ==============================================================================
// REGIA CUSTOM THEME
// Derived directly from the CSS design tokens in src/index.css.
// All hex values here must be kept in sync with the :root variables.
// ==============================================================================

/** Maps the app's design token palette onto a Monaco editor theme. */
const REGIA_THEME: MonacoType.editor.IStandaloneThemeData = {
    base: "vs",
    inherit: false,
    rules: [
        // === Structural keywords (ACTION, EVENT, FACT, PLAYBOOK, PLOT, PHASE, ROLE)
        { token: "keyword.declaration", foreground: "1769aa", fontStyle: "bold" },
        // === Flow keywords (DURING, WHEN, IF, ELSE, ON, ENTER, EXIT, TRANSITION, TO)
        { token: "keyword.flow", foreground: "0f4f82" },
        // === Action keywords (DO, ASSIGN, UNASSIGN, WORLD, SIGNAL, START, SUBPLOT, END, MAPPING)
        { token: "keyword.action", foreground: "18864b" },
        // === Special built-in actions (TELL, BROADCAST, ACHIEVE, BELIEVE, FORGET, PRINT)
        { token: "keyword.builtin", foreground: "18864b", fontStyle: "italic" },
        // === Modifiers (PRIORITY, TEMPER, EFFECTS, INITIAL, SELF, IMPORT, FROM)
        { token: "keyword.modifier", foreground: "52616d" },
        // === Identifiers (PascalCase = type/playbook/plot names)
        { token: "identifier.type", foreground: "1f2933", fontStyle: "bold" },
        // === Identifiers (lowercase = actions, events, facts)
        { token: "identifier", foreground: "344451" },
        // === Numbers (priority values, temper floats)
        { token: "number", foreground: "9a4d00" },
        // === Strings (PRINT arguments)
        { token: "string", foreground: "087f5b" },
        // === Doc Comments (#@..., #-...)
        { token: "comment.doc", foreground: "52616d", fontStyle: "italic" },
        // === Normal Comments (#...)
        { token: "comment", foreground: "7b8993", fontStyle: "italic" },
        // === Punctuation (. : , ( ))
        { token: "delimiter", foreground: "7b8993" },
    ],
    colors: {
        // Editor backgrounds
        "editor.background":              "#ffffff",  // --color-bg-editor
        "editor.foreground":              "#1f2933",  // --color-text-primary
        // Line number gutter
        "editorLineNumber.foreground":    "#7b8993",  // --color-text-muted
        "editorLineNumber.activeForeground": "#52616d", // --color-text-secondary
        // Current line highlight
        "editor.lineHighlightBackground": "#f3f5f7",  // --color-bg-app
        "editor.lineHighlightBorder":     "#e8edf1",
        // Selection
        "editor.selectionBackground":     "#1769aa33",// --color-accent-primary at 20% opacity
        "editor.inactiveSelectionBackground": "#1769aa1f",
        // Cursor
        "editorCursor.foreground":        "#1769aa",  // --color-accent-primary
        // Scrollbar
        "scrollbarSlider.background":     "#9aaab655",
        "scrollbarSlider.hoverBackground":"#1769aa88",
        "scrollbarSlider.activeBackground":"#1769aa",
        // Widget backgrounds (find, hover)
        "editorWidget.background":        "#ffffff",  // --color-bg-surface
        "editorWidget.border":            "#cbd5dc",  // --color-border
        // Error / warning squiggle underlines use Monaco defaults (red/yellow)
        // so we do not override them here.
        // Overview ruler (the minimap-side error indicator bar)
        "editorOverviewRuler.border":     "#eef2f5",
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
        "EXIT", "TRANSITION", "ENDS", "SIGNALS",
    ],
    actionKeywords: [
        "DO", "ASSIGN", "UNASSIGN", "WORLD", "SIGNAL",
        "START", "SUBPLOT", "END", "MAPPING", "TO", "AS",
    ],
    builtinKeywords: [
        "TELL", "BROADCAST", "ACHIEVE", "BELIEVE", "FORGET", "PRINT", "WAIT",
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
