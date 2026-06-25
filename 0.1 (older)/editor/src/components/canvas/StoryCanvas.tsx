import { useCallback, useEffect, useMemo } from 'react'
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  BackgroundVariant,
  type Connection,
} from '@xyflow/react'
import type { Story } from '../../types/story'
import { storyToGraph } from '../../layout/storyToGraph'
import { PhaseNode } from './PhaseNode'
import { useStore } from '../../store/useStore'
//import { useReactFlow } from '@xyflow/react'

const nodeTypes = { phaseNode: PhaseNode }

//const { fitView } = useReactFlow()

// Expose fitView globally for the export menu to call before capture
/*
useEffect(() => {
  ;(window as any).__regiaFitView = () => fitView({ padding: 0.15, duration: 0 })
}, [fitView])
*/
interface Props {
  story: Story
  onPhaseSelect: (phaseId: string) => void
}

export function StoryCanvas({ story, onPhaseSelect }: Props) {
  const addTransition     = useStore((s) => s.addTransition)
  const setActiveTransition = useStore((s) => s.setActiveTransition)

  const { nodes: initialNodes, edges: initialEdges } = useMemo(
    () => storyToGraph(story),
    [story]
  )

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes)
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges)

  useEffect(() => {
    const { nodes: n, edges: e } = storyToGraph(story)
    setNodes(n)
    setEdges(e)
  }, [story, setNodes, setEdges])

  const onNodeClick = useCallback(
    (_: React.MouseEvent, node: { id: string }) => {
      if (node.id !== '__end__') {
        onPhaseSelect(node.id)
      }
    },
    [onPhaseSelect]
  )

  // Dragging a connection creates a new TransitionRule
  const onConnect = useCallback(
    (connection: Connection) => {
      const { source, target } = connection
      if (!source || !target) return
      if (source === '__end__') return  // cannot start a transition from END

      const targetPhaseName =
        target === '__end__'
          ? 'END'
          : story.phases.find((p) => p.id === target)?.name ?? target

      const newId = addTransition(story.id, source, targetPhaseName)
      setActiveTransition(newId)
      onPhaseSelect(source)
    },
    [story, addTransition, setActiveTransition, onPhaseSelect]
  )

  return (
    <div className="w-full h-full">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeClick={onNodeClick}
        onConnect={onConnect}
        nodeTypes={nodeTypes}
        fitView
        fitViewOptions={{ padding: 0.2 }}
        minZoom={0.3}
        maxZoom={2}
      >
        <Background variant={BackgroundVariant.Dots} gap={16} size={1} />
        <Controls />
        <MiniMap
          nodeColor={(node) => {
            const d = node.data as { isEnd?: boolean; isInitial?: boolean; isAlways?: boolean }
            if (d.isEnd)     return '#fca5a5'
            if (d.isInitial) return '#86efac'
            if (d.isAlways)  return '#93c5fd'
            return '#fcd34d'
          }}
        />
      </ReactFlow>
    </div>
  )
}