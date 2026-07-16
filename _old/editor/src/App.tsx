import { useEffect, useMemo } from 'react'
import { Sidebar } from './components/panels/Sidebar'
import { StoryCanvas } from './components/canvas/StoryCanvas'
import { PropertiesPanel } from './components/panels/PropertiesPanel'
import { ExportMenu } from './components/panels/ExportMenu'
import { HistoryControls } from './components/panels/HistoryControls'
import { ToastContainer } from './components/ui/ToastContainer'
import { useStore } from './store/useStore'
import { initHistory } from './store/history'
import { useKeyboardShortcuts } from './hooks/useKeyboardShortcuts'
import { ReactFlowProvider } from '@xyflow/react'

export default function App() {
  const { project, activeStoryId, addPhase, setActivePhase } = useStore()

  useEffect(() => {
    initHistory()
  }, [])

  useKeyboardShortcuts()

  const activeStory = useMemo(
    () => project.stories.find((s) => s.id === activeStoryId) ?? null,
    [project.stories, activeStoryId]
  )

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-gray-50">
      <Sidebar />

      <div className="flex-1 flex flex-col">
        {activeStory ? (
          <>
            <div className="h-12 bg-white border-b border-gray-200
                            flex items-center px-4 gap-3 shrink-0">
              <h2 className="font-semibold text-gray-800">
                {activeStory.isDefault ? 'DEFAULT' : activeStory.name}
                {activeStory.priority !== null && (
                  <span className="ml-2 text-sm text-gray-400 font-normal">
                    Priority {activeStory.priority}
                  </span>
                )}
              </h2>

              <HistoryControls />

              <div className="flex-1" />

              {!activeStory.isDefault && (
                <button
                  onClick={() => addPhase(activeStory.id)}
                  className="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500
                             text-white text-sm rounded transition-colors"
                >
                  + Add Phase
                </button>
              )}
              <ExportMenu />
            </div>

            <div className="flex-1 overflow-hidden">
              <ReactFlowProvider>
                <StoryCanvas
                  story={activeStory}
                  onPhaseSelect={setActivePhase}
                />
              </ReactFlowProvider>
            </div>
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center text-gray-400">
            <div className="text-center">
              <div className="text-4xl mb-3">📖</div>
              <div className="text-lg font-medium">No story selected</div>
              <div className="text-sm mt-1">
                Select a story from the sidebar or create a new one
              </div>
              <div className="text-xs mt-3 text-gray-300">
                Tip: Ctrl+Z / Ctrl+Shift+Z to undo/redo
              </div>
            </div>
          </div>
        )}
      </div>

      <PropertiesPanel />
      <ToastContainer />
    </div>
  )
}