// src/components/editor/CodeEditor.tsx
import { useEffect, useRef } from "react";
import MonacoEditor, { type BeforeMount, type OnChange, type OnMount } from "@monaco-editor/react";
import type * as MonacoType from "monaco-editor";

import { useStore } from "../../store/useStore";
import { useDebounce } from "../../hooks/useDebounce";
import {
    registerRegiaLanguage,
    REGIA_LANGUAGE_ID,
    REGIA_THEME_ID,
} from "../../services/regiaLanguage";

import styles from "./CodeEditor.module.css";

// ==============================================================================
// CONSTANTS
// ==============================================================================

/** Maps backend severity strings to Monaco marker severities. */
const SEVERITY_MAP: Record<string, MonacoType.MarkerSeverity> = {
    ERROR: 4, // MonacoType.MarkerSeverity.Error
    WARNING: 2, // MonacoType.MarkerSeverity.Warning
    INFO: 1, // MonacoType.MarkerSeverity.Hint
};

// ==============================================================================
// COMPONENT IMPLEMENTATION
// ==============================================================================

/**
 * Monaco-based code editor for writing Regia source files.
 *
 * Responsibilities:
 * - Registers the Regia language definition and custom theme before mount.
 * - Propagates code changes to the global store (debounced parse at 500ms).
 * - Converts structured CompilerMessages from the store into inline Monaco
 *   error markers (red squiggles at the correct line/column).
 *
 * The store, transport layer, and debounce hook are completely unchanged
 * from the previous textarea implementation.
 */
export const CodeEditor = () => {
    const { code, setCode, parseCode, compilerMessages, isParsing, targetLine } = useStore();
    const debouncedCode = useDebounce(code, 500);

    // Keep a ref to the Monaco editor instance so we can push markers to it.
    const editorRef = useRef<MonacoType.editor.IStandaloneCodeEditor | null>(null);
    const monacoRef = useRef<typeof MonacoType | null>(null);

    // ============================================================
    // PARSE TRIGGER
    // ============================================================

    // Trigger a parse whenever the debounced code value changes.
    useEffect(() => {
        parseCode();
    }, [debouncedCode, parseCode]);

    // ============================================================
    // INLINE MARKER SYNC
    // ============================================================

    // Whenever the store's compilerMessages change, push them as Monaco markers.
    useEffect(() => {
        const monaco = monacoRef.current;
        const editor = editorRef.current;
        if (!monaco || !editor) return;

        const model = editor.getModel();
        if (!model) return;

        const markers: MonacoType.editor.IMarkerData[] = compilerMessages.map((msg) => ({
            severity: SEVERITY_MAP[msg.severity] ?? SEVERITY_MAP.ERROR,
            message: msg.message,
            startLineNumber: msg.line > 0 ? msg.line : 1,
            startColumn: msg.column > 0 ? msg.column : 1,
            endLineNumber: msg.line > 0 ? msg.line : 1,
            // Underline to the end of the line for a natural squiggle feel.
            endColumn: model.getLineMaxColumn(msg.line > 0 ? msg.line : 1),
        }));

        monaco.editor.setModelMarkers(model, "regia-compiler", markers);
    }, [compilerMessages]);

    // ============================================================
    // NAVIGATION SYNC
    // ============================================================

    // Whenever targetLine changes, reveal that line in the editor and move cursor.
    useEffect(() => {
        const editor = editorRef.current;
        if (!editor || targetLine === null) return;

        editor.revealLineInCenter(targetLine);
        editor.setPosition({ lineNumber: targetLine, column: 1 });
        editor.focus();
    }, [targetLine]);

    // ============================================================
    // MONACO LIFECYCLE CALLBACKS
    // ============================================================

    /** Register the Regia language and theme before the editor instance mounts. */
    const handleBeforeMount: BeforeMount = (monaco) => {
        registerRegiaLanguage(monaco);
    };

    /** Store refs to the editor and monaco API after mounting. */
    const handleMount: OnMount = (editor, monaco) => {
        editorRef.current = editor;
        monacoRef.current = monaco;
    };

    /** Propagate text changes to the store (triggers debounced parse). */
    const handleChange: OnChange = (value) => {
        setCode(value ?? "");
    };

    // ============================================================
    // RENDER
    // ============================================================

    return (
        <div className={styles.editorContainer}>
            {/* Header: title and live parsing indicator */}
            <div className={styles.editorHeader}>
                <h2 className={styles.editorTitle}>Regia Source</h2>
                {isParsing && (
                    <span className={styles.parsingIndicator}>Parsing…</span>
                )}
            </div>

            {/* Monaco editor: fills all remaining vertical space */}
            <div className={styles.monacoWrapper}>
                <MonacoEditor
                    height="100%"
                    language={REGIA_LANGUAGE_ID}
                    theme={REGIA_THEME_ID}
                    value={code}
                    beforeMount={handleBeforeMount}
                    onMount={handleMount}
                    onChange={handleChange}
                    options={{
                        // we don't need the minimap
                        minimap: { enabled: false },
                        fontSize: 14,
                        fontFamily: "'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace",
                        lineNumbers: "on",
                        scrollBeyondLastLine: false,
                        automaticLayout: true,
                        wordWrap: "on",
                        folding: true,
                        renderLineHighlight: "line",
                        smoothScrolling: true,
                        cursorBlinking: "smooth",
                        padding: { top: 12, bottom: 12 },
                    }}
                />
            </div>
        </div>
    );
};
