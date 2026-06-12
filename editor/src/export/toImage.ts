import { toPng, toSvg } from 'html-to-image'

const EXPORT_OPTIONS = {
  backgroundColor: '#f9fafb',
  pixelRatio: 2,
}

async function prepareCanvas(): Promise<HTMLElement> {
  const fitView = (window as any).__regiaFitView as (() => void) | undefined
  fitView?.()

  // Wait one frame for the fit to apply
  await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)))

  const viewport = document.querySelector(
    '.react-flow__viewport'
  ) as HTMLElement | null

  if (!viewport) {
    throw new Error('Canvas not found — open a story with phases first')
  }

  return viewport
}

export async function exportCanvasAsPng(filename: string) {
  const viewport = await prepareCanvas()
  const dataUrl = await toPng(viewport, EXPORT_OPTIONS)
  downloadDataUrl(filename, dataUrl)
}

export async function exportCanvasAsSvg(filename: string) {
  const viewport = await prepareCanvas()
  const dataUrl = await toSvg(viewport, EXPORT_OPTIONS)
  downloadDataUrl(filename, dataUrl)
}

function downloadDataUrl(filename: string, dataUrl: string) {
  const a = document.createElement('a')
  a.href = dataUrl
  a.download = filename
  a.click()
}