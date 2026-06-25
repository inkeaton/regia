import { create } from 'zustand'
import { nanoid } from 'nanoid'

export type ToastKind = 'success' | 'error' | 'info'

export interface Toast {
  id:   string
  kind: ToastKind
  text: string
}

interface ToastState {
  toasts: Toast[]
  push:   (kind: ToastKind, text: string) => void
  remove: (id: string) => void
}

export const useToastStore = create<ToastState>((set) => ({
  toasts: [],

  push: (kind, text) => {
    const id = nanoid()
    set((s) => ({ toasts: [...s.toasts, { id, kind, text }] }))
    setTimeout(() => {
      set((s) => ({ toasts: s.toasts.filter((t) => t.id !== id) }))
    }, 3500)
  },

  remove: (id) =>
    set((s) => ({ toasts: s.toasts.filter((t) => t.id !== id) })),
}))