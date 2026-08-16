// src/components/canvas/AstCanvas.tsx
import { useEffect, useState } from "react";
import ReactFlow, { Background, Controls, type Node, type Edge, Panel } from "reactflow";

import { useStore } from "../../store/useStore";
import type { PlotDef } from "../../types/ast";
import { PhaseNode } from "./PhaseNode";
import { convertAstToGraph } from "../../layout/astToGraph";
import { getLayoutedElements } from "../../layout/autoLayout";
import { exportCanvas } from "../../export/toImage";
import { useGraphEditing } from "../../hooks/useGraphEditing";
import { AddPhaseModal } from "./AddPhaseModal";
import { EventPickerModal } from "./EventPickerModal";
import { TransitionEdge } from "./TransitionEdge";

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

const EDGE_TYPES = {
    transitionEdge: TransitionEdge,
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

    const {
        onConnect,
        onPaneDoubleClick,
        pendingConnection,
        isAddingPhase,
        cancelPending,
        confirmAddPhase,
        confirmAddTransition,
    } = useGraphEditing();

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

    const plot = ast?.items?.find((item) => item.type === "PlotDef") as PlotDef | undefined;
    const roles = plot?.roles?.map((r) => r.name) || [];

    return (
        <div className={`${styles.canvasWrapper} ${hasSyntaxErrors ? styles.canvasWrapperDimmed : ""}`}>
            <ReactFlow
                nodes={nodes}
                edges={edges}
                nodeTypes={NODE_TYPES}
                edgeTypes={EDGE_TYPES}
                fitView
                fitViewOptions={{ padding: 0.2 }}
                onConnect={onConnect}
                nodesDraggable={false}
                nodesConnectable={true}
            >
                <Background color="var(--color-border)" gap={20} />
                <Controls />

                {/* Info panel in the top-left corner */}
                {plot && (
                    <Panel position="top-left">
                        <div className={styles.infoPanel}>
                            <div className={styles.plotNameSection}>
                                <span className={styles.infoPanelTitle}>Plot: {plot.name}</span>
                            </div>
                            
                            {roles.length > 0 && (
                                <>
                                    <span className={styles.infoPanelTitle}>Roles</span>
                                    <div className={styles.roleChipContainer}>
                                        {roles.map((role) => (
                                            <span key={role} className={styles.roleChip}>
                                                {role}
                                            </span>
                                        ))}
                                    </div>
                                </>
                            )}
                            
                            <div className={styles.actionsSection}>
                                <button 
                                    className={styles.actionButton}
                                    onClick={onPaneDoubleClick}
                                >
                                    + Add Phase
                                </button>
                            </div>
                        </div>
                    </Panel>
                )}

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

            {pendingConnection && ast && (
                <EventPickerModal
                    ast={ast}
                    connection={pendingConnection}
                    onConfirm={confirmAddTransition}
                    onCancel={cancelPending}
                />
            )}
            
            {isAddingPhase && (
                <AddPhaseModal
                    onConfirm={confirmAddPhase}
                    onCancel={cancelPending}
                />
            )}
        </div>
    );
};