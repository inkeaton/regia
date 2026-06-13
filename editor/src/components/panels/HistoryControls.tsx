import { useEffect, useState } from 'react'
import { undo, redo, canUndo, canRedo, subscribeHistory } from '../../store/history'

export function HistoryControls() {
  const [, forceUpdate] = useState(0)

  useEffect(() => {
    return subscribeHistory(() => forceUpdate((n) => n + 1))
  }, [])

  return (
    <div className="flex items-center gap-1">
      <button
        onClick={undo}
        disabled={!canUndo()}
        title="Undo (Ctrl+Z)"
        className="px-2 py-1.5 text-sm border border-gray-300 rounded
                   hover:bg-gray-50 disabled:opacity-30 disabled:cursor-not-allowed
                   transition-colors"
      >
        ↶
      </button>
      <button
        onClick={redo}
        disabled={!canRedo()}
        title="Redo (Ctrl+Shift+Z)"
        className="px-2 py-1.5 text-sm border border-gray-300 rounded
                   hover:bg-gray-50 disabled:opacity-30 disabled:cursor-not-allowed
                   transition-colors"
      >
        ↷
      </button>
    </div>
  )
}