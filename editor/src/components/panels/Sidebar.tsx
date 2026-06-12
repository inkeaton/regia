import { useStore } from '../../store/useStore'
import { motion, AnimatePresence } from 'framer-motion'

export function Sidebar() {
  const { project, activeStoryId, addStory, setActiveStory, deleteStory } =
    useStore()

  return (
    <div className="w-64 h-full bg-gray-900 text-white flex flex-col border-r border-gray-700">

      {/* Header */}
      <div className="px-4 py-3 border-b border-gray-700">
        <h1 className="font-bold text-lg text-indigo-400">RegiaScript</h1>
        <p className="text-xs text-gray-400">Story Editor</p>
      </div>

      {/* Story list */}
      <div className="flex-1 overflow-y-auto py-2">
        <div className="px-3 py-1 text-xs font-semibold text-gray-400 uppercase">
          Stories
        </div>
        <AnimatePresence>
          {project.stories.map((story) => (
            <motion.button
              key={story.id}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -10 }}
              onClick={() => setActiveStory(story.id)}
              className={`
                w-full text-left px-4 py-2 text-sm flex items-center gap-2
                hover:bg-gray-800 transition-colors
                ${activeStoryId === story.id
                  ? 'bg-gray-800 text-indigo-400'
                  : 'text-gray-300'}
              `}
            >
              <span className="flex-1 truncate">
                {story.isDefault ? '⚡ DEFAULT' : `📖 ${story.name}`}
              </span>
              {!story.isDefault && story.priority !== null && (
                <span className="text-xs text-gray-500">
                  P{story.priority}
                </span>
              )}
            </motion.button>
          ))}
        </AnimatePresence>
      </div>

      {/* Add buttons */}
      <div className="p-3 border-t border-gray-700 flex flex-col gap-2">
        <button
          onClick={() => addStory(false)}
          className="w-full py-2 px-3 bg-indigo-600 hover:bg-indigo-500
                     rounded text-sm font-medium transition-colors"
        >
          + Add Story
        </button>
        <button
          onClick={() => addStory(true)}
          disabled={project.stories.some((s) => s.isDefault)}
          className="w-full py-2 px-3 bg-gray-700 hover:bg-gray-600
                     rounded text-sm font-medium transition-colors
                     disabled:opacity-40 disabled:cursor-not-allowed"
        >
          + Add Default
        </button>
      </div>
    </div>
  )
}