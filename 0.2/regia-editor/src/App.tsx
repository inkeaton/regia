// src/App.tsx
import { CodeEditor } from "./components/editor/CodeEditor";
import { StoryCanvas } from "./components/canvas/StoryCanvas";

import styles from "./App.module.css";

// ==============================================================================
// COMPONENT IMPLEMENTATION
// ==============================================================================

/**
 * Root application component.
 * Establishes the two-column split layout:
 *   Left  (40%) = Code Editor panel
 *   Right (60%) = Graph Canvas panel
 */
export const App = () => {
    return (
        <div className={styles.appShell}>
            {/* Left Column: Code Editor */}
            <div className={styles.editorPanel}>
                <CodeEditor />
            </div>

            {/* Right Column: Visual Graph */}
            <div className={styles.canvasPanel}>
                <StoryCanvas />
            </div>
        </div>
    );
};

export default App;