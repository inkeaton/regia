import { useStore } from '../../store/useStore'
import { StoryProperties } from './StoryProperties'
import { PhaseProperties } from './PhaseProperties'
import { motion, AnimatePresence } from 'framer-motion'

export function PropertiesPanel() {
  const { project, activeStoryId, activePhaseId } = useStore()

  const story = project.stories.find((s) => s.id === activeStoryId)
  const phase = story?.phases.find((p) => p.id === activePhaseId)

  if (!story) return null

  return (
    <div className="w-96 h-full bg-white border-l border-gray-200 overflow-y-auto shrink-0">
      <AnimatePresence mode="wait">
        {phase ? (
          <motion.div
            key={phase.id}
            initial={{ opacity: 0, x: 10 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 10 }}
            transition={{ duration: 0.15 }}
          >
            <PhaseProperties story={story} phase={phase} />
          </motion.div>
        ) : (
          <motion.div
            key="story"
            initial={{ opacity: 0, x: 10 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 10 }}
            transition={{ duration: 0.15 }}
          >
            <StoryProperties story={story} />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}