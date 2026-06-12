import dagre from 'dagre'
import type { Node, Edge } from '@xyflow/react'

const NODE_WIDTH  = 220
const NODE_HEIGHT = 80

export function applyDagreLayout(
  nodes: Node[],
  edges: Edge[],
  direction: 'TB' | 'LR' = 'TB'
): Node[] {
  const graph = new dagre.graphlib.Graph()

  graph.setDefaultEdgeLabel(() => ({}))
  graph.setGraph({
    rankdir:  direction,
    nodesep:  60,
    ranksep:  80,
    marginx:  40,
    marginy:  40,
  })

  nodes.forEach((node) => {
    graph.setNode(node.id, {
      width:  NODE_WIDTH,
      height: NODE_HEIGHT,
    })
  })

  edges.forEach((edge) => {
    graph.setEdge(edge.source, edge.target)
  })

  dagre.layout(graph)

  return nodes.map((node) => {
    const { x, y } = graph.node(node.id)
    return {
      ...node,
      position: {
        x: x - NODE_WIDTH  / 2,
        y: y - NODE_HEIGHT / 2,
      },
    }
  })
}