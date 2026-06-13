import { useEffect } from 'react'
import { useStore } from '../store/useStore'
import { undo, redo } from '../store/history'
import { useToastStore } from '../store/useToastStore'

function isTypingTarget(el: EventTarget | null): boolean {
  if (!(el instanceof HTMLElement)) return false
  const tag = el.tagName
  return tag === 'INPUT' || tag === 'TEXTAREA' || el.isContentEditable
}

export function useKeyboardShortcuts() {
  const {
    project, activeStoryId, activePhaseId,
    deletePhase, deleteStory, setActivePhase, setActiveStory,
  } = useStore()
  const push = useToastStore((s) => s.push)

  useEffect(() => {
    function onKeyDown(e: KeyboardEvent) {
      const ctrlOrCmd = e.ctrlKey || e.metaKey

      // Undo / Redo — work everywhere except while typing
      if (ctrlOrCmd && !isTypingTarget(e.target)) {
        if (e.key === 'z' && !e.shiftKey) {
          e.preventDefault()
          undo()
          push('info', 'Undo')
          return
        }
        if ((e.key === 'z' && e.shiftKey) || e.key === 'y') {
          e.preventDefault()
          redo()
          push('info', 'Redo')
          return
        }
      }

      // Delete selected phase/story — only when not typing
      if ((e.key === 'Delete' || e.key === 'Backspace') && !isTypingTarget(e.target)) {
        if (activePhaseId && activeStoryId) {
          e.preventDefault()
          deletePhase(activeStoryId, activePhaseId)
          setActivePhase(null)
          push('info', 'Phase deleted')
          return
        }
      }

      // Escape — deselect
      if (e.key === 'Escape') {
        if (activePhaseId) {
          setActivePhase(null)
        } else if (activeStoryId) {
          setActiveStory(null)
        }
      }
    }

    window.addEventListener('keydown', onKeyDown)
    return () => window.removeEventListener('keydown', onKeyDown)
  }, [
    project, activeStoryId, activePhaseId,
    deletePhase, deleteStory, setActivePhase, setActiveStory, push,
  ])
}