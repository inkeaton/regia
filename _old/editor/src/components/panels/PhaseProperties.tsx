import type { Story, Phase } from '../../types/story'
import { useStore } from '../../store/useStore'
import { AgentEditor } from './AgentEditor'
import { TransitionEditor } from './TransitionEditor'

interface Props {
  story: Story
  phase: Phase
}

export function PhaseProperties({ story, phase }: Props) {
  const {
    updatePhase, deletePhase, setActivePhase,
    addAgentToPhase, addTransition, setActiveTransition,
  } = useStore()

  return (
    <div className="p-4 space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold text-gray-800">Phase Settings</h3>
        <button
          onClick={() => setActivePhase(null)}
          className="text-xs text-gray-400 hover:text-gray-600"
        >
          ← Story
        </button>
      </div>

      <div>
        <label className="block text-xs font-medium text-gray-500 mb-1">
          Name
        </label>
        <input
          value={phase.name}
          onChange={(e) =>
            updatePhase(story.id, phase.id, { name: e.target.value })
          }
          disabled={phase.isAlways}
          className="w-full px-2 py-1.5 border border-gray-300 rounded text-sm mb-2
                     focus:outline-none focus:ring-2 focus:ring-indigo-400
                     disabled:bg-gray-100 disabled:text-gray-400"
        />

        <div className="flex gap-3 text-xs">
          <label className="flex items-center gap-1.5">
            <input
              type="checkbox"
              checked={phase.isInitial}
              onChange={(e) =>
                updatePhase(story.id, phase.id, { isInitial: e.target.checked })
              }
              disabled={phase.isAlways}
            />
            Initial phase
          </label>
          <label className="flex items-center gap-1.5">
            <input
              type="checkbox"
              checked={phase.isAlways}
              onChange={(e) =>
                updatePhase(story.id, phase.id, {
                  isAlways: e.target.checked,
                  name: e.target.checked ? 'ALWAYS' : phase.name,
                  isInitial: e.target.checked ? false : phase.isInitial,
                })
              }
            />
            DURING ALWAYS
          </label>
        </div>
      </div>

      {/* Transitions */}
      {!phase.isAlways && (
        <div>
          <div className="flex items-center justify-between mb-2">
            <h4 className="text-xs font-semibold text-gray-500 uppercase">
              Transitions
            </h4>
            <button
              onClick={() => {
                const id = addTransition(story.id, phase.id, 'END')
                setActiveTransition(id)
              }}
              className="text-xs text-indigo-600 hover:text-indigo-800 font-medium"
            >
              + Add
            </button>
          </div>
          <div className="space-y-2">
            {phase.transitions.map((t) => (
              <TransitionEditor
                key={t.id}
                story={story}
                phase={phase}
                transition={t}
              />
            ))}
            {phase.transitions.length === 0 && (
              <p className="text-xs text-gray-400 italic">
                None — drag a connection on the canvas to create one
              </p>
            )}
          </div>
        </div>
      )}

      {/* Agents */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <h4 className="text-xs font-semibold text-gray-500 uppercase">
            Agents
          </h4>
          <button
            onClick={() => addAgentToPhase(story.id, phase.id)}
            className="text-xs text-indigo-600 hover:text-indigo-800 font-medium"
          >
            + Add
          </button>
        </div>
        <div className="space-y-3">
          {phase.agents.map((agent) => (
            <AgentEditor
              key={agent.agentName}
              story={story}
              phase={phase}
              agent={agent}
            />
          ))}
          {phase.agents.length === 0 && (
            <p className="text-xs text-gray-400 italic">No agents in this phase</p>
          )}
        </div>
      </div>

      <div className="pt-4 border-t border-gray-200">
        <button
          onClick={() => {
            deletePhase(story.id, phase.id)
            setActivePhase(null)
          }}
          className="w-full py-2 text-sm text-red-600 hover:bg-red-50
                     rounded transition-colors"
        >
          Delete Phase
        </button>
      </div>
    </div>
  )
}