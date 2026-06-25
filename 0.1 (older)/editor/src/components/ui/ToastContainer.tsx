import { AnimatePresence, motion } from 'framer-motion'
import { useToastStore, type ToastKind } from '../../store/useToastStore'

const STYLES: Record<ToastKind, string> = {
  success: 'bg-green-600 text-white',
  error:   'bg-red-600 text-white',
  info:    'bg-gray-800 text-white',
}

const ICONS: Record<ToastKind, string> = {
  success: '✓',
  error:   '✕',
  info:    'ℹ',
}

export function ToastContainer() {
  const { toasts, remove } = useToastStore()

  return (
    <div className="fixed bottom-4 right-4 z-50 flex flex-col gap-2 items-end">
      <AnimatePresence>
        {toasts.map((toast) => (
          <motion.div
            key={toast.id}
            initial={{ opacity: 0, y: 10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 10, scale: 0.95 }}
            transition={{ duration: 0.15 }}
            onClick={() => remove(toast.id)}
            className={`
              ${STYLES[toast.kind]}
              px-4 py-2.5 rounded-lg shadow-lg text-sm
              flex items-center gap-2 cursor-pointer max-w-sm
            `}
          >
            <span className="font-bold">{ICONS[toast.kind]}</span>
            <span>{toast.text}</span>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  )
}