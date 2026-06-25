import type { Story, Phase, TransitionRule, Origin } from '../../types/story'
import { useStore } from '../../store/useStore'

const ORIGINS: Origin[] = ['ENVIRONMENT', 'DIRECTOR', 'MYSELF', 'PLAYER', 'TIMER']

interface Props {
  story:      Story
  phase:      Phase
  transition: TransitionRule
}

export function TransitionEditor({ story, phase, transition }: Props) {
  const { updateTransition, deleteTransition } = useStore()

  const setT = (patch: Partial<TransitionRule>) =>
    updateTransition(story.id, phase.id, transition.id, patch)

  const condTerms = transition.condition?.ands[0]?.terms ?? []

  const setCondTerms = (terms: typeof condTerms) =>
    setT({ condition: terms.length ? { ands: [{ terms }] } : undefined })

  const addCondTerm = () => {
    const first = story.conditions[0]
    if (!first) return
    setCondTerms([
      ...condTerms,
      { type: 'condition', name: first.name, origin: first.origin, negated: false },
    ])
  }

  const targetPhases = story.phases.filter((p) => !p.isAlways)

  return (
    <div className="border border-gray-200 rounded p-2 bg-indigo-50/40 space-y-1.5 text-xs">
      <div className="flex items-center gap-1.5">
        <span className="font-semibold text-gray-500 shrink-0">TO</span>
        <select
          value={transition.toPhase}
          onChange={(e) => setT({ toPhase: e.target.value })}
          className="flex-1 px-1.5 py-1 border border-gray-300 rounded
                     focus:outline-none focus:ring-1 focus:ring-indigo-400"
        >
          <option value="END">END</option>
          {targetPhases.map((p) => (
            <option key={p.id} value={p.name}>{p.name}</option>
          ))}
        </select>
        <button
          onClick={() => deleteTransition(story.id, phase.id, transition.id)}
          className="text-gray-400 hover:text-red-500 px-1"
        >
          ✕
        </button>
      </div>

      <div className="flex items-center gap-1.5">
        <span className="font-semibold text-gray-500 shrink-0">WHEN</span>
        <select
          value={transition.eventName}
          onChange={(e) => {
            const ev = story.events.find((ev) => ev.name === e.target.value)
            setT({ eventName: e.target.value, origin: ev?.origin ?? transition.origin })
          }}
          className="flex-1 px-1.5 py-1 border border-gray-300 rounded
                     focus:outline-none focus:ring-1 focus:ring-indigo-400"
        >
          <option value="">— select event —</option>
          {story.events.map((ev) => (
            <option key={ev.id} value={ev.name}>{ev.name}</option>
          ))}
        </select>
        <select
          value={transition.origin}
          onChange={(e) => setT({ origin: e.target.value as Origin })}
          className="px-1 py-1 border border-gray-300 rounded
                     focus:outline-none focus:ring-1 focus:ring-indigo-400"
        >
          {ORIGINS.map((o) => <option key={o} value={o}>{o}</option>)}
        </select>
      </div>

      <div>
        <div className="flex items-center justify-between">
          <span className="font-semibold text-gray-500">IF (all must hold)</span>
          <button
            onClick={addCondTerm}
            disabled={story.conditions.length === 0}
            className="text-indigo-600 hover:text-indigo-800 font-medium disabled:opacity-30"
          >
            + Add condition
          </button>
        </div>
        {condTerms.map((term, i) => (
          <div key={i} className="flex items-center gap-1.5 mt-1">
            <label className="flex items-center gap-1">
              <input
                type="checkbox"
                checked={term.negated}
                onChange={(e) =>
                  setCondTerms(
                    condTerms.map((t, idx) =>
                      idx === i ? { ...t, negated: e.target.checked } : t
                    )
                  )
                }
              />
              NOT
            </label>
            <select
              value={term.name}
              onChange={(e) => {
                const cond = story.conditions.find((c) => c.name === e.target.value)
                setCondTerms(
                  condTerms.map((t, idx) =>
                    idx === i
                      ? { ...t, name: e.target.value, origin: cond?.origin ?? t.origin }
                      : t
                  )
                )
              }}
              className="flex-1 px-1.5 py-1 border border-gray-300 rounded
                         focus:outline-none focus:ring-1 focus:ring-indigo-400"
            >
              {story.conditions.map((c) => (
                <option key={c.id} value={c.name}>{c.name}</option>
              ))}
            </select>
            <button
              onClick={() => setCondTerms(condTerms.filter((_, idx) => idx !== i))}
              className="text-gray-400 hover:text-red-500 px-1"
            >
              ✕
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}