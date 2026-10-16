// src/layout/autoLayout.ts
import dagre from "dagre";
import type { Node, Edge } from "reactflow";

import {
    NODE_WIDTH,
    NODE_HEIGHT,
    LAYOUT_RANK_SEP,
    LAYOUT_NODE_SEP,
} from "./constants";

// ==============================================================================
// LAYOUT ENGINE
// ==============================================================================

/**
 * Applies a directed acyclic graph (DAG) layout to a set of React Flow nodes
 * and edges using the dagre library.
 *
 * Dagre calculates optimal positions automatically, so we don't have to place
 * nodes manually. The calculated positions are center-based, but React Flow
 * uses top-left corners, so we offset accordingly.
 *
 * @param nodes     - Unpositioned React Flow nodes (position values are ignored).
 * @param edges     - React Flow edges defining the connections.
 * @param direction - "TB" for top-to-bottom flow, "LR" for left-to-right.
 * @returns A new array of nodes with updated `position` values, plus the unchanged edges.
 */
export const getLayoutedElements = (
    nodes: Node[],
    edges: Edge[],
    direction: "TB" | "LR" = "TB"
): { nodes: Node[]; edges: Edge[] } => {
    const dagreGraph = new dagre.graphlib.Graph();
    dagreGraph.setDefaultEdgeLabel(() => ({}));
    dagreGraph.setGraph({
        rankdir: direction,
        ranksep: LAYOUT_RANK_SEP,
        nodesep: LAYOUT_NODE_SEP,
    });

    // Register node dimensions so dagre can compute spacing correctly.
    nodes.forEach((node) => {
        dagreGraph.setNode(node.id, { width: NODE_WIDTH, height: NODE_HEIGHT });
    });

    // Register edges so dagre knows the connectivity.
    edges.forEach((edge) => {
        dagreGraph.setEdge(edge.source, edge.target);
    });

    // Run the layout algorithm.
    dagre.layout(dagreGraph);

    // Dagre returns center coordinates; React Flow needs top-left. Offset by half-dimensions.
    const layoutedNodes = nodes.map((node) => {
        const { x, y } = dagreGraph.node(node.id);
        return {
            ...node,
            position: {
                x: x - NODE_WIDTH  / 2,
                y: y - NODE_HEIGHT / 2,
            },
        };
    });

    return { nodes: layoutedNodes, edges };
};