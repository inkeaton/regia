import { useState } from 'react'
import { useStore } from '../../store/useStore'
import { projectToRegiaScript } from '../../export/toRegiaScript'
import { projectToJSON, jsonToProject, downloadText } from '../../export/projectIO'
import { exportCanvasAsPng, exportCanvasAsSvg } from '../../export/toImage'
import { motion, AnimatePresence } from 'framer-motion'
import { parseRegiaScript } from '../../import/fromRegiaScript'
import { ImportError } from '../../import/errors'
import { clearHistory } from '../../store/history'
import { useToastStore } from '../../store/useToastStore'

export function ExportMenu() {
  const { project, setProject } = useStore()
  const [open, setOpen] = useState(false)
  const push = useToastStore((s) => s.push)

 const handleExportRgs = () => {
  const text = projectToRegiaScript(project)
  downloadText('story.rgs', text, 'text/plain')
  push('success', 'Exported story.rgs')
  setOpen(false)
}

const handleExportJson = () => {
  downloadText('story.regia.json', projectToJSON(project), 'application/json')
  push('success', 'Exported story.regia.json')
  setOpen(false)
}

const handleExportPng = async () => {
  try {
    await exportCanvasAsPng('story.png')
    push('success', 'Exported story.png')
  } catch (e) {
    push('error', e instanceof Error ? e.message : 'Export failed')
  }
  setOpen(false)
}

const handleExportSvg = async () => {
  try {
    await exportCanvasAsSvg('story.svg')
    push('success', 'Exported story.svg')
  } catch (e) {
    push('error', e instanceof Error ? e.message : 'Export failed')
  }
  setOpen(false)
}

const handleImportJson = (e: React.ChangeEvent<HTMLInputElement>) => {
  const file = e.target.files?.[0]
  if (!file) return

  const reader = new FileReader()
  reader.onload = () => {
    try {
      const text = reader.result as string
      const imported = jsonToProject(text)
      setProject(imported)
      clearHistory()
      push('success', `Imported ${file.name}`)
    } catch (err) {
      push('error', err instanceof Error ? err.message : 'Invalid file')
    }
  }
  reader.readAsText(file)
  setOpen(false)
  e.target.value = ''
}

const handleImportRgs = (e: React.ChangeEvent<HTMLInputElement>) => {
  const file = e.target.files?.[0]
  if (!file) return

  const reader = new FileReader()
  reader.onload = () => {
    try {
      const text = reader.result as string
      const imported = parseRegiaScript(text)
      setProject(imported)
      clearHistory()
      push('success', `Imported ${file.name}`)
    } catch (err) {
      if (err instanceof ImportError) {
        push('error', err.message)
      } else {
        push('error', err instanceof Error ? err.message : 'Invalid RegiaScript file')
      }
    }
  }
  reader.readAsText(file)
  setOpen(false)
  e.target.value = ''
}

  return (
    <div className="relative">
      <button
        onClick={() => setOpen(!open)}
        className="px-3 py-1.5 bg-white border border-gray-300 hover:bg-gray-50
                   text-sm rounded transition-colors flex items-center gap-1.5"
      >
        Export / Import
        <span className="text-gray-400 text-xs">▾</span>
      </button>

      <AnimatePresence>
        {open && (
          <>
            {/* Click-away backdrop */}
            <div
              className="fixed inset-0 z-10"
              onClick={() => setOpen(false)}
            />

            <motion.div
              initial={{ opacity: 0, y: -4 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -4 }}
              transition={{ duration: 0.12 }}
              className="absolute right-0 mt-1 w-56 bg-white border border-gray-200
                         rounded-md shadow-lg z-20 overflow-hidden"
            >
              <div className="px-3 py-1.5 text-xs font-semibold text-gray-400 uppercase
                              bg-gray-50 border-b border-gray-100">
                Export
              </div>
              <MenuItem onClick={handleExportRgs} icon="📄">
                RegiaScript (.rgs)
              </MenuItem>
              <MenuItem onClick={handleExportJson} icon="🗂️">
                Project (.json)
              </MenuItem>
              <MenuItem onClick={handleExportPng} icon="🖼️">
                Current view (.png)
              </MenuItem>
              <MenuItem onClick={handleExportSvg} icon="🖼️">
                Current view (.svg)
              </MenuItem>

              <div className="px-3 py-1.5 text-xs font-semibold text-gray-400 uppercase
                              bg-gray-50 border-y border-gray-100">
                Import
              </div>
              <label className="block px-3 py-2 text-sm hover:bg-gray-50
                                 cursor-pointer transition-colors flex items-center gap-2">
                <span>📂</span> Project (.json)
                <input
                  type="file"
                  accept="application/json"
                  className="hidden"
                  onChange={handleImportJson}
                />
              </label>

              <label className="block px-3 py-2 text-sm hover:bg-gray-50
                   cursor-pointer transition-colors flex items-center gap-2">
                <span>📄</span> RegiaScript (.rgs)
                <input
                  type="file"
                  accept=".rgs,text/plain"
                  className="hidden"
                  onChange={handleImportRgs}
                />
              </label>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </div>
  )
}

function MenuItem({
  onClick, icon, children,
}: { onClick: () => void; icon: string; children: React.ReactNode }) {
  return (
    <button
      onClick={onClick}
      className="w-full text-left px-3 py-2 text-sm hover:bg-gray-50
                 transition-colors flex items-center gap-2"
    >
      <span>{icon}</span> {children}
    </button>
  )
}