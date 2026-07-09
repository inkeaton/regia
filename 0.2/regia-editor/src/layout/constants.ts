// src/layout/constants.ts

// ==============================================================================
// GRAPH LAYOUT CONSTANTS
// ==============================================================================
// Single source of truth for all geometry values used by storyToGraph.ts,
// autoLayout.ts, and the CSS modules.
// Changing these values adjusts the entire graph layout uniformly.

/** Width assumed for each Phase node (must match PhaseNode.module.css min-width). */
export const NODE_WIDTH  = 220;

/** Height assumed for each Phase node (approximate rendered height). */
export const NODE_HEIGHT = 100;

/** Vertical spacing between node rows in the dagre layout (in pixels). */
export const LAYOUT_RANK_SEP = 150;

/** Horizontal spacing between nodes in the same row (in pixels). */
export const LAYOUT_NODE_SEP = 120;

// ==============================================================================
// EDGE STYLE DEFAULTS
// ==============================================================================
// These are used in storyToGraph.ts when constructing React Flow Edge objects.
// Centralising them here means a single edit propagates to all edges.

/** Default stroke color for transition edges. Matches --color-edge in index.css. */
export const EDGE_COLOR = "#7c7cff";

/** Default stroke width for transition edges. */
export const EDGE_STROKE_WIDTH = 2;

/** Arrow marker width. */
export const EDGE_MARKER_WIDTH  = 20;

/** Arrow marker height. */
export const EDGE_MARKER_HEIGHT = 20;
