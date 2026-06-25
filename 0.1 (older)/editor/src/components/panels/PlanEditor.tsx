import type { Story, Phase, AgentInPhase, Plan, Origin, DoAction } from '../../types/story'
import { useStore } from '../../store/useStore'

const ORIGINS: Origin[] = ['ENVIRONMENT', 'DIRECTOR', 'MYSELF', 'PLAYER', 'TIMER']

interface Props {
  story: Story
  phase: Phase
  agent: AgentInPhase
  plan: Plan
}

export function PlanEditor({ story, phase, agent, plan }: Props) {
  const { updatePlan, deletePlan } = useStore()

  const setPlan = (patch: Partial<Plan>) =>
    updatePlan(story.id, phase.id, agent.agentName, plan.id, patch)

  // Condition editing — flat AND list (single OR-group) for simplicity
  const condTerms = plan.condition?.ands[0]?.terms ?? []

  const setCondTerms = (terms: typeof condTerms) =>
    setPlan({ condition: terms.length ? { ands: [{ terms }] } : undefined })

  const addCondTerm = () => {
    const first = story.conditions[0]
    if (!first) return
    setCondTerms([
      ...condTerms,
      { type: 'condition', name: first.name, origin: first.origin, negated: false },
    ])
  }

  const updateCondTerm = (i: number, patch: Partial<typeof condTerms[0]>) =>
    setCondTerms(condTerms.map((t, idx) => (idx === i ? { ...t, ...patch } : t)))

  const removeCondTerm = (i: number) =>
    setCondTerms(condTerms.filter((_, idx) => idx !== i))

  // Actions (DO sequence)
  const addAction = (kind: DoAction['kind']) => {
    const target =
      kind === 'action'
        ? story.actions[0]?.name ?? ''
        : story.conditions[0]?.name ?? ''
    setPlan({ actions: [...plan.actions, { kind, target }] })
  }

  const updateAction = (i: number, patch: Partial<DoAction>) =>
    setPlan({
      actions: plan.actions.map((a, idx) => (idx === i ? { ...a, ...patch } : a)),
    })

  const removeAction = (i: number) =>
    setPlan({ actions: plan.actions.filter((_, idx) => idx !== i) })

  return (
    <div className="border border-gray-200 rounded p-2 bg-gray-50 space-y-2 text-xs">
      {/* WHEN event + origin */}
      <div className="flex items-center gap-1.5">
        <span className="font-semibold text-gray-500 w-12">WHEN</span>
        <select
          value={plan.eventName}
          onChange={(e) => {
            const ev = story.events.find((ev) => ev.name === e.target.value)
            setPlan({ eventName: e.target.value, origin: ev?.origin ?? plan.origin })
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
          value={plan.origin}
          onChange={(e) => setPlan({ origin: e.target.value as Origin })}
          className="px-1 py-1 border border-gray-300 rounded
                     focus:outline-none focus:ring-1 focus:ring-indigo-400"
        >
          {ORIGINS.map((o) => <option key={o} value={o}>{o}</option>)}
        </select>
        <button
          onClick={() => deletePlan(story.id, phase.id, agent.agentName, plan.id)}
          className="text-gray-400 hover:text-red-500 px-1"
        >
          ✕
        </button>
      </div>

      {/* IF condition */}
      <div className="pl-1">
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
                onChange={(e) => updateCondTerm(i, { negated: e.target.checked })}
              />
              NOT
            </label>
            <select
              value={term.name}
              onChange={(e) => {
                const cond = story.conditions.find((c) => c.name === e.target.value)
                updateCondTerm(i, { name: e.target.value, origin: cond?.origin ?? term.origin })
              }}
              className="flex-1 px-1.5 py-1 border border-gray-300 rounded
                         focus:outline-none focus:ring-1 focus:ring-indigo-400"
            >
              {story.conditions.map((c) => (
                <option key={c.id} value={c.name}>{c.name}</option>
              ))}
            </select>
            <button
              onClick={() => removeCondTerm(i)}
              className="text-gray-400 hover:text-red-500 px-1"
            >
              ✕
            </button>
          </div>
        ))}
      </div>

      {/* DO sequence */}
      <div className="pl-1">
        <div className="flex items-center justify-between">
          <span className="font-semibold text-gray-500">DO</span>
          <div className="flex gap-2">
            <button
              onClick={() => addAction('action')}
              disabled={story.actions.length === 0}
              className="text-indigo-600 hover:text-indigo-800 font-medium disabled:opacity-30"
            >
              + Action
            </button>
            <button
              onClick={() => addAction('believe')}
              disabled={story.conditions.length === 0}
              className="text-indigo-600 hover:text-indigo-800 font-medium disabled:opacity-30"
            >
              + Believe
            </button>
            <button
              onClick={() => addAction('forget')}
              disabled={story.conditions.length === 0}
              className="text-indigo-600 hover:text-indigo-800 font-medium disabled:opacity-30"
            >
              + Forget
            </button>
          </div>
        </div>
        {plan.actions.map((action, i) => (
          <div key={i} className="flex items-center gap-1.5 mt-1">
            <span className="text-gray-400 w-14 shrink-0">
              {action.kind === 'action' ? 'DO' : action.kind === 'believe' ? 'BELIEVE' : 'FORGET'}
            </span>
            <select
              value={action.target}
              onChange={(e) => updateAction(i, { target: e.target.value })}
              className="flex-1 px-1.5 py-1 border border-gray-300 rounded
                         focus:outline-none focus:ring-1 focus:ring-indigo-400"
            >
              {(action.kind === 'action' ? story.actions : story.conditions).map((d) => (
                <option key={d.id} value={d.name}>{d.name}</option>
              ))}
            </select>
            <button
              onClick={() => removeAction(i)}
              className="text-gray-400 hover:text-red-500 px-1"
            >
              ✕
            </button>
          </div>
        ))}
        {plan.actions.length === 0 && (
          <p className="text-gray-400 italic mt-1">No actions</p>
        )}
      </div>
    </div>
  )
}