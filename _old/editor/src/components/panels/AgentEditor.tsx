import { useState } from 'react'
import type { Story, Phase, AgentInPhase } from '../../types/story'
import { useStore } from '../../store/useStore'
import { PlanEditor } from './PlanEditor'
import { motion, AnimatePresence } from 'framer-motion'

interface Props {
  story: Story
  phase: Phase
  agent: AgentInPhase
}

export function AgentEditor({ story, phase, agent }: Props) {
  const { updateAgentInPhase, removeAgentFromPhase, addPlan } = useStore()
  const [expanded, setExpanded] = useState(true)

  return (
    <div className="border border-gray-200 rounded-md overflow-hidden">
      <div className="flex items-center gap-2 px-2 py-1.5 bg-gray-50">
        <button
          onClick={() => setExpanded(!expanded)}
          className="text-gray-400 hover:text-gray-600 text-xs w-4"
        >
          {expanded ? '▾' : '▸'}
        </button>
        <input
          value={agent.agentName}
          onChange={(e) =>
            updateAgentInPhase(story.id, phase.id, agent.agentName, {
              agentName: e.target.value,
            })
          }
          className="flex-1 px-1.5 py-1 border border-gray-300 rounded text-xs font-medium
                     focus:outline-none focus:ring-1 focus:ring-indigo-400"
        />
        <button
          onClick={() => removeAgentFromPhase(story.id, phase.id, agent.agentName)}
          className="text-gray-400 hover:text-red-500 px-1"
        >
          ✕
        </button>
      </div>

      <AnimatePresence>
        {expanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden"
          >
            <div className="p-2 space-y-2">
              {agent.plans.map((plan) => (
                <PlanEditor
                  key={plan.id}
                  story={story}
                  phase={phase}
                  agent={agent}
                  plan={plan}
                />
              ))}

              <button
                onClick={() => addPlan(story.id, phase.id, agent.agentName)}
                className="w-full py-1 text-xs text-indigo-600 hover:bg-indigo-50
                           rounded border border-dashed border-indigo-300"
              >
                + Add WHEN block
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}