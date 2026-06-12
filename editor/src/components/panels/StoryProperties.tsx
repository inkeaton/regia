import type { Story } from '../../types/story'
import { useStore } from '../../store/useStore'
import { DeclarationList } from './DeclarationList'

interface Props {
  story: Story
}

export function StoryProperties({ story }: Props) {
  const { updateStory, deleteStory } = useStore()

  return (
    <div className="p-4 space-y-6">
      <div>
        <h3 className="font-semibold text-gray-800 mb-3">Story Settings</h3>

        {!story.isDefault && (
          <>
            <label className="block text-xs font-medium text-gray-500 mb-1">
              Name
            </label>
            <input
              value={story.name}
              onChange={(e) => updateStory(story.id, { name: e.target.value })}
              className="w-full px-2 py-1.5 border border-gray-300 rounded text-sm mb-3
                         focus:outline-none focus:ring-2 focus:ring-indigo-400"
            />

            <label className="block text-xs font-medium text-gray-500 mb-1">
              Priority
            </label>
            <input
              type="number"
              min={1}
              value={story.priority ?? 1}
              onChange={(e) =>
                updateStory(story.id, { priority: parseInt(e.target.value) || 1 })
              }
              className="w-full px-2 py-1.5 border border-gray-300 rounded text-sm mb-3
                         focus:outline-none focus:ring-2 focus:ring-indigo-400"
            />
          </>
        )}

        <label className="block text-xs font-medium text-gray-500 mb-1">
          Doc — Name
        </label>
        <input
          value={story.doc?.name ?? ''}
          onChange={(e) =>
            updateStory(story.id, { doc: { ...story.doc, name: e.target.value } })
          }
          placeholder="@NAME: ..."
          className="w-full px-2 py-1.5 border border-gray-300 rounded text-sm mb-3
                     focus:outline-none focus:ring-2 focus:ring-indigo-400"
        />

        <label className="block text-xs font-medium text-gray-500 mb-1">
          Doc — Meaning
        </label>
        <textarea
          value={story.doc?.meaning ?? ''}
          onChange={(e) =>
            updateStory(story.id, { doc: { ...story.doc, meaning: e.target.value } })
          }
          placeholder="@MEANING: ..."
          rows={2}
          className="w-full px-2 py-1.5 border border-gray-300 rounded text-sm
                     focus:outline-none focus:ring-2 focus:ring-indigo-400 resize-none"
        />
      </div>

      <DeclarationList story={story} kind="action" />
      <DeclarationList story={story} kind="event" />
      <DeclarationList story={story} kind="condition" />

      <div className="pt-4 border-t border-gray-200">
        <button
          onClick={() => deleteStory(story.id)}
          className="w-full py-2 text-sm text-red-600 hover:bg-red-50
                     rounded transition-colors"
        >
          Delete Story
        </button>
      </div>
    </div>
  )
}