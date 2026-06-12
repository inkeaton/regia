import type { Story, Origin } from '../../types/story'
import { useStore } from '../../store/useStore'

const ORIGINS: Origin[] = ['ENVIRONMENT', 'DIRECTOR', 'MYSELF', 'PLAYER', 'TIMER']

interface Props {
  story: Story
  kind:  'action' | 'event' | 'condition'
}

const CONFIG = {
  action:    { label: 'Actions',    hasOrigin: false },
  event:     { label: 'Events',     hasOrigin: true  },
  condition: { label: 'Conditions', hasOrigin: true  },
} as const

export function DeclarationList({ story, kind }: Props) {
  const store = useStore()
  const cfg = CONFIG[kind]

  const items =
    kind === 'action' ? story.actions :
    kind === 'event'  ? story.events  :
    story.conditions

  const add = () =>
    kind === 'action' ? store.addAction(story.id) :
    kind === 'event'  ? store.addEvent(story.id)  :
    store.addCondition(story.id)

  const update = (id: string, patch: any) =>
    kind === 'action' ? store.updateAction(story.id, id, patch) :
    kind === 'event'  ? store.updateEvent(story.id, id, patch)  :
    store.updateCondition(story.id, id, patch)

  const remove = (id: string) =>
    kind === 'action' ? store.deleteAction(story.id, id) :
    kind === 'event'  ? store.deleteEvent(story.id, id)  :
    store.deleteCondition(story.id, id)

  return (
    <div>
      <div className="flex items-center justify-between mb-2">
        <h4 className="text-xs font-semibold text-gray-500 uppercase">
          {cfg.label}
        </h4>
        <button
          onClick={add}
          className="text-xs text-indigo-600 hover:text-indigo-800 font-medium"
        >
          + Add
        </button>
      </div>

      <div className="space-y-1.5">
        {items.map((item: any) => (
          <div key={item.id} className="flex items-center gap-1.5">
            <input
              value={item.name}
              onChange={(e) => update(item.id, { name: e.target.value })}
              className="flex-1 px-2 py-1 border border-gray-300 rounded text-xs
                         focus:outline-none focus:ring-1 focus:ring-indigo-400"
            />
            {cfg.hasOrigin && (
              <select
                value={item.origin}
                onChange={(e) => update(item.id, { origin: e.target.value })}
                className="px-1 py-1 border border-gray-300 rounded text-xs
                           focus:outline-none focus:ring-1 focus:ring-indigo-400"
              >
                {ORIGINS.map((o) => (
                  <option key={o} value={o}>{o}</option>
                ))}
              </select>
            )}
            <button
              onClick={() => remove(item.id)}
              className="text-gray-400 hover:text-red-500 px-1"
              title="Remove"
            >
              ✕
            </button>
          </div>
        ))}
        {items.length === 0 && (
          <p className="text-xs text-gray-400 italic">None declared</p>
        )}
      </div>
    </div>
  )
}