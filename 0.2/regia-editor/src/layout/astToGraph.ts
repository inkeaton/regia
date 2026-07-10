// src/layout/astToGraph.ts
import { type Node, type Edge, MarkerType } from "reactflow";
import type { Program, PlotDef, DuringBlock } from "../types/ast";

import {
    EDGE_COLOR,
    EDGE_STROKE_WIDTH,
    EDGE_MARKER_WIDTH,
    EDGE_MARKER_HEIGHT,
} from "./constants";

// ==============================================================================
// AST-TO-GRAPH MAPPER
// ==============================================================================

/**
 * Converts a Regia AST Program into React Flow nodes and edges.
 *
 * Mapping rules:
 * - Each `PhaseDecl` becomes a node of type "phaseNode".
 * - Each `TransitionStmt` inside a `DuringBlock` becomes a directed edge.
 *
 * Smart edge routing:
 * - "Immediate forward" transitions (A→B where B is declared right after A)
 *   use `smoothstep` routing and the vertical Top/Bottom handles.
 * - "Long-jump", reverse, and duplicate-pair edges use Bezier arcs ("default")
 *   routed through the lateral Left/Right handles, alternating sides to avoid
 *   overlapping intermediate nodes.
 *
 * @param ast - The root AST Program object received from the Python backend.
 * @returns Unpositioned nodes and edges. Call `getLayoutedElements` to add positions.
 */
export const convertAstToGraph = (ast: Program | null): { nodes: Node[]; edges: Edge[] } => {
    const nodes: Node[] = [];
    const edges: Edge[] = [];

    if (!ast || !ast.items) return { nodes, edges };

    // We only visualize the first PlotDef found in the program.
    // Multi-Plot support is deferred; see the implementation plan.
    const plot = ast.items.find((item) => item.type === "PlotDef") as PlotDef | undefined;
    if (!plot) return { nodes, edges };

    // ==========================================================================
    // Step 1: Map PhaseDecl → Nodes
    // ==========================================================================

    // Record each phase's position in the declaration order.
    // This index is used below to determine whether a transition is
    // "immediate forward" (going to the very next declared phase).
    const phaseIndexMap: Record<string, number> = {};

    plot.phases.forEach((phase, index) => {
        phaseIndexMap[phase.name] = index;

        nodes.push({
            id: phase.name,
            type: "phaseNode",   // Must match the key in NODE_TYPES (AstCanvas.tsx)
            position: { x: 0, y: 0 }, // Placeholder; dagre will compute the real position
            data: {
                label:     phase.name,
                isInitial: phase.is_initial,
                line:      phase.loc.line,
            },
        });
    });

    // ==========================================================================
    // Step 2: Map TransitionStmt → Edges
    // ==========================================================================

    // Track how many edges already exist for each unordered node pair.
    // A pair with more than one edge needs lateral routing to avoid visual overlap.
    const edgePairCounts: Record<string, number> = {};

    // Alternates between left and right sides for lateral edges.
    let lateralCounter = 0;

    plot.during_blocks.forEach((block: DuringBlock) => {
        // Skip DURING PLOT blocks (phase_name is null); transitions only exist
        // inside phase-specific DURING blocks.
        if (!block.phase_name) return;

        block.transitions.forEach((trans) => {
            const source = block.phase_name as string;
            const target = trans.target_phase;

            const sourceIdx = phaseIndexMap[source] ?? 0;
            const targetIdx = phaseIndexMap[target] ?? 0;

            // An "immediate forward" transition goes from phase N to phase N+1 —
            // the most common case. These get straight vertical routing.
            const isImmediateForward = (targetIdx - sourceIdx) === 1;

            // Use an unordered key so A→B and B→A share a counter.
            const pairKey = [source, target].sort().join("-");
            edgePairCounts[pairKey] = (edgePairCounts[pairKey] ?? 0);
            const slot = edgePairCounts[pairKey]++;

            // Choose handle IDs and edge type based on routing strategy.
            let sourceHandle: string;
            let targetHandle: string;
            let edgeType: string;

            if (isImmediateForward && slot === 0) {
                // Straight vertical: top/bottom handles with step-style routing.
                sourceHandle = "bottom-s";
                targetHandle = "top-t";
                edgeType     = "smoothstep";
            } else {
                // Lateral/reverse: Bezier arc through left or right handles.
                // Alternating sides prevents all curved edges from going the same way.
                edgeType = "default";
                if (lateralCounter % 2 === 0) {
                    sourceHandle = "right-s";
                    targetHandle = "right-t";
                } else {
                    sourceHandle = "left-s";
                    targetHandle = "left-t";
                }
                lateralCounter++;
            }

            edges.push({
                id:           `edge-${source}-${target}-${trans.event}`,
                source,
                target,
                sourceHandle,
                targetHandle,
                type:         edgeType,
                label:        trans.event,
                animated:     true,
                zIndex:       -1, // Keep edges behind node cards
                style:        { stroke: EDGE_COLOR, strokeWidth: EDGE_STROKE_WIDTH },
                labelStyle:   { fill: EDGE_COLOR, fontWeight: 700, fontSize: 12 },
                labelBgStyle: { fill: "var(--color-edge-label-bg)", fillOpacity: 0.9 },
                markerEnd: {
                    type:   MarkerType.ArrowClosed,
                    width:  EDGE_MARKER_WIDTH,
                    height: EDGE_MARKER_HEIGHT,
                    color:  EDGE_COLOR,
                },
            });
        });
    });

    return { nodes, edges };
};