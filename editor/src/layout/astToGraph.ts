// src/layout/astToGraph.ts
import { type Node, type Edge, MarkerType } from "reactflow";
import type { Program, PlotDef, DuringBlock, ImperativeStmt } from "../types/ast";

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

        // Find the matching DuringBlock
        const block = plot.during_blocks.find(b => b.phase_name === phase.name);
        
        let line = phase.loc.line;
        let planCount = 0;
        let isTerminal = false;
        let hasOnEnter = false;
        let hasOnExit = false;

        if (block) {
            line = block.loc.line;
            planCount = block.when_blocks.length;

            // Helper to recursively search for PlotEndStmt
            const hasEndPlot = (stmts: ImperativeStmt[]): boolean => {
                for (const stmt of stmts) {
                    if (stmt.type === "PlotEndStmt") return true;
                }
                return false;
            };

            // Check if this phase has any PlotEndStmt in its reactive plans
            for (const whenBlock of block.when_blocks) {
                if (hasEndPlot(whenBlock.prefix_stmts)) {
                    isTerminal = true;
                    break;
                }
                for (const branch of whenBlock.branches) {
                    if (hasEndPlot(branch.stmts)) {
                        isTerminal = true;
                        break;
                    }
                }
                if (!isTerminal && whenBlock.else_branch) {
                    if (hasEndPlot(whenBlock.else_branch.stmts)) {
                        isTerminal = true;
                        break;
                    }
                }
                if (isTerminal) break;
            }
            
            hasOnEnter = block.on_enters.length > 0;
            hasOnExit = block.on_exits.length > 0;
        }

        nodes.push({
            id: phase.name,
            type: "phaseNode",   // Must match the key in NODE_TYPES (AstCanvas.tsx)
            position: { x: 0, y: 0 }, // Placeholder; dagre will compute the real position
            data: {
                label:     phase.name,
                isInitial: phase.is_initial,
                line:      line,
                planCount: planCount,
                isTerminal: isTerminal,
                hasOnEnter: hasOnEnter,
                hasOnExit: hasOnExit,
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

    const addEdge = (source: string, target: string, eventLabel: string) => {
        // Use an unordered key so A→B and B→A share a counter.
        const pairKey = [source, target].sort().join("-");
        edgePairCounts[pairKey] = (edgePairCounts[pairKey] ?? 0);
        const slot = edgePairCounts[pairKey]++;

        // Use custom edge to avoid label collisions
        const edgeType = "transitionEdge";
        
        let sourceHandle: string;
        let targetHandle: string;

        if (slot === 0) {
            // First edge between these nodes goes straight top-to-bottom
            sourceHandle = "bottom-s";
            targetHandle = "top-t";
        } else {
            // Additional edges route laterally to avoid overlap
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
            id:           `edge-${source}-${target}-${eventLabel}-${slot}`,
            source,
            target,
            sourceHandle,
            targetHandle,
            type:         edgeType,
            label:        eventLabel,
            animated:     true,
            zIndex:       -1, // Keep edges behind node cards
            style:        { stroke: EDGE_COLOR, strokeWidth: EDGE_STROKE_WIDTH },
            data:         { slot },
            markerEnd: {
                type:   MarkerType.ArrowClosed,
                width:  EDGE_MARKER_WIDTH,
                height: EDGE_MARKER_HEIGHT,
                color:  EDGE_COLOR,
            },
        });
    };

    plot.during_blocks.forEach((block: DuringBlock) => {
        // Skip DURING PLOT blocks (phase_name is null); transitions only exist
        // inside phase-specific DURING blocks.
        if (!block.phase_name) return;

        // 1. Extract reactive/inline transitions (inside when_blocks)
        block.when_blocks.forEach((whenBlock) => {
            const source = block.phase_name as string;
            const eventLabel = whenBlock.type === "PlotWhenRoleSignalsBlock" 
                ? `ROLE ${whenBlock.role_name} SIGNALS ${whenBlock.event}` 
                : "event" in whenBlock 
                    ? whenBlock.event 
                    : `SUBPLOT ${whenBlock.subplot_name} ENDS`;

            // Helper to scan a list of imperative statements for inline transitions
            const scanStmts = (stmts: ImperativeStmt[]) => {
                stmts.forEach((stmt) => {
                    if (stmt.type === "InlineTransitionStmt") {
                        addEdge(source, stmt.target_phase, eventLabel);
                    }
                });
            };

            scanStmts(whenBlock.prefix_stmts);
            whenBlock.branches.forEach((branch) => scanStmts(branch.stmts));
            if (whenBlock.else_branch) {
                scanStmts(whenBlock.else_branch.stmts);
            }
        });
    });

    return { nodes, edges };
};