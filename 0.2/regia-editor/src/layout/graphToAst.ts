// src/layout/graphToAst.ts

// ==============================================================================
// GRAPH-TO-AST REVERSE MAPPER (stub)
// ==============================================================================
// This module will contain the reverse of storyToGraph.ts:
// given a set of React Flow nodes and edges, reconstruct the PlotDef portion
// of the AST so it can be sent to the /emit-regia endpoint.
//
// HOW TO IMPLEMENT (when ready):
//
//   1. For each Node of type "phaseNode" → create a PhaseDecl.
//   2. For each Edge → find which source phase it belongs to,
//      then create a TransitionStmt with target_phase and event.
//   3. Wrap phases + transitions into DuringBlocks, then into a PlotDef.
//   4. Call transport.emitRegia(ast) → get Regia DSL string back.
//   5. Update the store's `code` field with the result.
//
// The round-trip guarantee: because the Python server is the source of truth
// for both parsing and emission, the resulting code will always be valid.
//
// NOTE: This file is intentionally empty for now. The architecture is already
// in place: the Transport interface in services/transport.ts has a stub for
// the emitRegia() method. Implement this module when tackling Phase 5.

import type { Node, Edge } from "reactflow";
import type { PlotDef } from "../types/ast";

/**
 * Converts the current React Flow graph state back into a partial PlotDef AST.
 *
 * @param nodes - The current React Flow nodes (Phase nodes).
 * @param edges - The current React Flow edges (Transition edges).
 * @param plotName - The name of the Plot being edited.
 * @returns A partial PlotDef AST fragment, without ON ENTER/EXIT or WHEN blocks.
 *
 * @todo Implement when Phase 5 (bidirectional editing) begins.
 */
export const convertGraphToAst = (
    _nodes: Node[],
    _edges: Edge[],
    _plotName: string
): PlotDef => {
    // Stub: not yet implemented.
    throw new Error("convertGraphToAst is not yet implemented. See the Phase 5 plan.");
};
