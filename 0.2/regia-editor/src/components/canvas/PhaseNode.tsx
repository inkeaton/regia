// src/components/canvas/PhaseNode.tsx
import { Handle, Position, type NodeProps } from "reactflow";

import styles from "./PhaseNode.module.css";

// ==============================================================================
// TYPE DEFINITIONS
// ==============================================================================

/**
 * Data payload attached to every Phase node in the React Flow graph.
 * The `storyToGraph.ts` mapper populates this from the AST.
 *
 * @property label     - The phase name (e.g. "backstage").
 * @property isInitial - True if this is the INITIAL phase.
 * @property line      - Source line number for click-to-navigate (future feature).
 */
export type PhaseNodeData = {
    label: string;
    isInitial: boolean;
    line: number;
};

// ==============================================================================
// HANDLE STYLE
// ==============================================================================

// Handles are the small connection dots on the node edges.
// React Flow requires their style to be passed directly via the `style` prop,
// so we define it here rather than in the CSS module.
const HANDLE_STYLE = {
    width: 8,
    height: 8,
    background: "var(--color-accent-primary)",
    border: "2px solid var(--color-bg-surface)",
} as const;

// ==============================================================================
// COMPONENT IMPLEMENTATION
// ==============================================================================

/**
 * Custom React Flow node that renders a single Regia Phase.
 *
 * Each node exposes six handles (top, bottom, left-source, left-target,
 * right-source, right-target) so that the smart edge router in
 * `storyToGraph.ts` can avoid visual overlaps for reverse/lateral transitions.
 *
 * @param data - The PhaseNodeData payload set by `storyToGraph.ts`.
 */
export const PhaseNode = ({ data }: NodeProps<PhaseNodeData>) => {
    const cardClass = data.isInitial
        ? `${styles.nodeCard} ${styles.nodeCardInitial}`
        : styles.nodeCard;

    return (
        <div className={cardClass}>
            {/* === Connection handles === */}
            {/* Primary vertical flow (forward transitions) */}
            <Handle type="target" position={Position.Top}    id="top-t"     style={HANDLE_STYLE} />
            <Handle type="source" position={Position.Bottom} id="bottom-s"  style={HANDLE_STYLE} />

            {/* Lateral flow: right side (slot 1 for reverse/skip edges) */}
            <Handle type="source" position={Position.Right}  id="right-s"   style={{ ...HANDLE_STYLE, top: "40%" }} />
            <Handle type="target" position={Position.Right}  id="right-t"   style={{ ...HANDLE_STYLE, top: "60%" }} />

            {/* Lateral flow: left side (slot 2 for a third overlapping edge) */}
            <Handle type="source" position={Position.Left}   id="left-s"    style={{ ...HANDLE_STYLE, top: "40%" }} />
            <Handle type="target" position={Position.Left}   id="left-t"    style={{ ...HANDLE_STYLE, top: "60%" }} />

            {/* === Node content === */}
            <div className={styles.nodeHeader}>
                <span className={styles.nodeLabel}>{data.label}</span>
                {data.isInitial && (
                    <span className={styles.initialBadge}>INITIAL</span>
                )}
            </div>

            <div className={styles.nodeFooter}>
                Line: {data.line}
            </div>
        </div>
    );
};