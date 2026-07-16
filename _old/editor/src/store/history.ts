import { useStore } from './useStore'
import type { RegiaProject } from '../types/story'

const MAX_HISTORY = 50
const DEBOUNCE_MS = 500

let past:   RegiaProject[] = []
let future: RegiaProject[] = []

let isRestoring = false
let pendingPrev: RegiaProject | null = null
let debounceTimer: ReturnType<typeof setTimeout> | null = null

type Listener = () => void
const listeners = new Set<Listener>()

export function subscribeHistory(fn: Listener): () => void {
  listeners.add(fn)
  return () => listeners.delete(fn)
}

function notify() {
  listeners.forEach((fn) => fn())
}

export function canUndo(): boolean { return past.length > 0 }
export function canRedo(): boolean { return future.length > 0 }

export function initHistory() {
  let prevProject = useStore.getState().project

  useStore.subscribe((state) => {
    if (isRestoring) {
      prevProject = state.project
      return
    }
    if (state.project === prevProject) return

    // First change in a burst — remember the "before" snapshot
    if (!debounceTimer) {
      pendingPrev = prevProject
    }

    if (debounceTimer) clearTimeout(debounceTimer)
    debounceTimer = setTimeout(() => {
      if (pendingPrev) {
        past.push(pendingPrev)
        if (past.length > MAX_HISTORY) past.shift()
        future = []
        pendingPrev = null
        notify()
      }
      debounceTimer = null
    }, DEBOUNCE_MS)

    prevProject = state.project
  })
}

export function undo() {
  // Flush any pending debounced snapshot first
  if (pendingPrev) {
    past.push(pendingPrev)
    if (past.length > MAX_HISTORY) past.shift()
    pendingPrev = null
    if (debounceTimer) { clearTimeout(debounceTimer); debounceTimer = null }
  }

  const previous = past.pop()
  if (!previous) return

  const current = useStore.getState().project
  future.push(current)

  isRestoring = true
  useStore.getState().setProject(previous, false)
  isRestoring = false

  notify()
}

export function redo() {
  const next = future.pop()
  if (!next) return

  const current = useStore.getState().project
  past.push(current)

  isRestoring = true
  useStore.getState().setProject(next, false)
  isRestoring = false

  notify()
}

export function clearHistory() {
  past = []
  future = []
  pendingPrev = null
  if (debounceTimer) { clearTimeout(debounceTimer); debounceTimer = null }
  notify()
}