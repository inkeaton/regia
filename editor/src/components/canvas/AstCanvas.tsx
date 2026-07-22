// src/components/canvas/AstCanvas.tsx
import { useEffect, useState } from "react";
import ReactFlow, { Background, Controls, type Node, type Edge, Panel } from "reactflow";

import { useStore } from "../../store/useStore";
import { PhaseNode } from "./PhaseNode";
import { convertAstToGraph } from "../../layout/astToGraph";
import { getLayoutedElements } from "../../layout/autoLayout";
import { exportCanvas } from "../../export/toImage";

import styles from "./AstCanvas.module.css";
import "reactflow/dist/style.css";

// ==============================================================================
// CONFIGURATION
// ==============================================================================

/**
 * Registry of custom node types for React Flow.
 * Add new custom node types here when extending the visualization.
 * The key ("phaseNode") must match the `type` field set in `astToGraph.ts`.
 */
const NODE_TYPES = {
    phaseNode: PhaseNode,
};

// ==============================================================================
// COMPONENT IMPLEMENTATION
// ==============================================================================

/**
 * Renders the interactive React Flow canvas that visualizes the AST as a graph.
 *
 * Behavior:
 * - Listens to the global `ast` state in the Zustand store.
 * - Whenever the AST changes, re-converts it to nodes/edges and applies layout.
 * - Dims the canvas when there are parse errors to signal stale state.
 * - Provides PNG/SVG export via the top-right toolbar panel.
 *
 * Extension points:
 * - To add interactivity (drag, add, delete), add `onNodesChange`, `onEdgesChange`,
 *   and `onConnect` props to the `<ReactFlow>` element.
 * - To add new node types, register them in `NODE_TYPES` above.
 */
export const AstCanvas = () => {
    const { ast, errors } = useStore();
    const [nodes, setNodes] = useState<Node[]>([]);
    const [edges, setEdges] = useState<Edge[]>([]);

    // Recompute the graph layout whenever the AST updates.
    // The layout pipeline is: AST → raw nodes/edges → dagre layout → positioned nodes.
    useEffect(() => {
        if (!ast || !ast.items) return;

        const { nodes: rawNodes, edges: rawEdges } = convertAstToGraph(ast);

        // If no Phase nodes were found (e.g. Playbook-only file), clear the canvas.
        if (rawNodes.length === 0) {
            setNodes([]);
            setEdges([]);
            return;
        }

        const { nodes: layoutedNodes, edges: layoutedEdges } = getLayoutedElements(
            rawNodes,
            rawEdges,
            "TB" // Top-to-Bottom layout direction
        );

        setNodes(layoutedNodes);
        setEdges(layoutedEdges);
    }, [ast]);

    const hasSyntaxErrors = errors.length > 0;

    return (
        <div className={`${styles.canvasWrapper} ${hasSyntaxErrors ? styles.canvasWrapperDimmed : ""}`}>
            <ReactFlow
                nodes={nodes}
                edges={edges}
                nodeTypes={NODE_TYPES}
                fitView
                fitViewOptions={{ padding: 0.2 }}
            >
                <Background color="var(--color-border)" gap={20} />
                <Controls />

                {/* Export toolbar in the top-right corner */}
                <Panel position="top-right">
                    <div className={styles.exportPanel}>
                        <span className={styles.exportPanelTitle}>Export</span>
                        <div className={styles.exportButtonRow}>
                            <button
                                className={styles.exportButton}
                                onClick={() => exportCanvas("png", "plot")}
                            >
                                PNG
                            </button>
                            <button
                                className={styles.exportButton}
                                onClick={() => exportCanvas("svg", "plot")}
                            >
                                SVG
                            </button>
                        </div>
                    </div>
                </Panel>
            </ReactFlow>
        </div>
    );
};