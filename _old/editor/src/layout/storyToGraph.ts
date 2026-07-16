import type { Node, Edge } from '@xyflow/react'
import type { Story } from '../types/story'
import { applyDagreLayout } from './autoLayout'

export interface PhaseNodeData extends Record<string, unknown> {
  label:     string
  isInitial: boolean
  isAlways:  boolean
  isEnd:     boolean
  phaseId:   string
  storyId:   string
  agentCount: number
}

export function storyToGraph(story: Story): { nodes: Node[]; edges: Edge[] } {
  const nodes: Node[] = []
  const edges: Edge[] = []

  // Replace the "Add an implicit END node" section with:

// Always add an END node — users can drag connections to it
nodes.push({
  id:   '__end__',
  type: 'phaseNode',
  data: {
    label:      'END',
    isInitial:  false,
    isAlways:   false,
    isEnd:      true,
    phaseId:    '__end__',
    storyId:    story.id,
    agentCount: 0,
  } satisfies PhaseNodeData,
  position: { x: 0, y: 0 },
})
  // Phase nodes
  story.phases.forEach((phase) => {
    nodes.push({
      id:   phase.id,
      type: 'phaseNode',
      data: {
        label:      phase.name,
        isInitial:  phase.isInitial,
        isAlways:   phase.isAlways,
        isEnd:      false,
        phaseId:    phase.id,
        storyId:    story.id,
        agentCount: phase.agents.length,
      } satisfies PhaseNodeData,
      position: { x: 0, y: 0 },  // dagre overwrites this
    })
  })

  // Transition edges
  // In storyToGraph.ts, replace the transition edge resolution:
  story.phases.forEach((phase) => {
    phase.transitions.forEach((transition) => {
      const targetId =
        transition.toPhase === 'END'
          ? '__end__'
          : story.phases.find((p) => p.name === transition.toPhase)?.id
            ?? story.phases.find((p) => p.id === transition.toPhase)?.id
            ?? transition.toPhase

      edges.push({
        id:           transition.id,
        source:       phase.id,
        target:       targetId,
        label:        buildEdgeLabel(transition.eventName, transition.condition),
        type:         'smoothstep',
        animated:     false,
        style:        { stroke: '#6366f1' },
        labelStyle:   { fontSize: 11, fill: '#374151' },
        labelBgStyle: { fill: '#f9fafb', fillOpacity: 0.9 },
      })
    })
  })

  // Apply auto-layout
  const laidOutNodes = applyDagreLayout(nodes, edges, 'TB')

  return { nodes: laidOutNodes, edges }
}

function buildEdgeLabel(
  eventName: string,
  condition?: { ands: { terms: unknown[] }[] }
): string {
  if (!condition || condition.ands.length === 0) return eventName
  return `${eventName} [IF...]`
}