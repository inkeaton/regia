// src/components/editor/CodeEditor.tsx
import { useEffect } from "react";

import { useStore } from "../../store/useStore";
import { useDebounce } from "../../hooks/useDebounce";

import styles from "./CodeEditor.module.css";

// ==============================================================================
// COMPONENT IMPLEMENTATION
// ==============================================================================

/**
 * Text editor component for writing Regia source code.
 *
 * Implements a 500ms debounce so that the backend parser is only called
 * once the user pauses typing, preventing excessive HTTP requests.
 *
 * Displays a list of syntax errors below the textarea when parsing fails.
 */
export const CodeEditor = () => {
    const { code, setCode, parseCode, errors, isParsing } = useStore();
    const debouncedCode = useDebounce(code, 500);

    // Trigger a parse whenever the debounced code value changes.
    // The dependency on `parseCode` is stable because Zustand actions
    // are created once and never recreated.
    useEffect(() => {
        parseCode();
    }, [debouncedCode, parseCode]);

    return (
        <div className={styles.editorContainer}>
            {/* Header: title and live parsing indicator */}
            <div className={styles.editorHeader}>
                <h2 className={styles.editorTitle}>Regia Source</h2>
                {isParsing && (
                    <span className={styles.parsingIndicator}>Parsing…</span>
                )}
            </div>

            {/* Code input area */}
            <textarea
                className={styles.codeTextarea}
                value={code}
                onChange={(e) => setCode(e.target.value)}
                spellCheck={false}
                aria-label="Regia source code editor"
            />

            {/* Error panel: only rendered when there are parse errors */}
            {errors.length > 0 && (
                <div className={styles.errorPanel} role="alert">
                    <p className={styles.errorPanelTitle}>Syntax Errors</p>
                    <ul className={styles.errorList}>
                        {errors.map((err, idx) => (
                            // Using the index as key is acceptable here because
                            // the error list is always fully replaced on each parse.
                            <li key={idx} className={styles.errorItem}>{err}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};