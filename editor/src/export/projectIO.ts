import type { RegiaProject } from '../types/story'

export function projectToJSON(project: RegiaProject): string {
  return JSON.stringify(project, null, 2)
}

export function jsonToProject(json: string): RegiaProject {
  const parsed = JSON.parse(json)

  if (!parsed || typeof parsed !== 'object') {
    throw new Error('Invalid project file: not an object')
  }
  if (!Array.isArray(parsed.stories)) {
    throw new Error('Invalid project file: missing "stories" array')
  }
  if (typeof parsed.version !== 'string') {
    throw new Error('Invalid project file: missing "version" field')
  }

  return parsed as RegiaProject
}

export function downloadText(filename: string, content: string, mime: string) {
  const blob = new Blob([content], { type: mime })
  const url  = URL.createObjectURL(blob)
  const a    = document.createElement('a')
  a.href     = url
  a.download = filename
  a.click()
  URL.revokeObjectURL(url)
}