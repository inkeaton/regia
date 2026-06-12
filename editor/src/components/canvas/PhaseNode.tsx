import { memo } from 'react'
import { Handle, Position, type NodeProps } from '@xyflow/react'
import { motion } from 'framer-motion'
import type { PhaseNodeData } from '../../layout/storyToGraph'

export const PhaseNode = memo(({ data, selected }: NodeProps) => {
  const d = data as PhaseNodeData

  const borderColor = d.isEnd
    ? 'border-red-400'
    : d.isInitial
    ? 'border-green-500'
    : d.isAlways
    ? 'border-blue-400'
    : 'border-amber-400'

  const bgColor = d.isEnd
    ? 'bg-red-50'
    : d.isInitial
    ? 'bg-green-50'
    : d.isAlways
    ? 'bg-blue-50'
    : 'bg-amber-50'

  const headerColor = d.isEnd
    ? 'bg-red-200'
    : d.isInitial
    ? 'bg-green-200'
    : d.isAlways
    ? 'bg-blue-200'
    : 'bg-amber-200'

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.15 }}
      className={`
        rounded-lg border-2 shadow-sm w-[220px] overflow-hidden
        ${borderColor} ${bgColor}
        ${selected ? 'ring-2 ring-indigo-500 ring-offset-1' : ''}
      `}
    >
      {/* Header */}
      <div className={`px-3 py-1.5 ${headerColor}`}>
        <div className="flex items-center gap-2">
          {d.isInitial && (
            <span className="text-[10px] font-bold text-green-700 uppercase">
              Initial
            </span>
          )}
          {d.isAlways && (
            <span className="text-[10px] font-bold text-blue-700 uppercase">
              Always
            </span>
          )}
          {d.isEnd && (
            <span className="text-[10px] font-bold text-red-700 uppercase">
              Terminal
            </span>
          )}
        </div>
        <div className="font-bold text-sm text-gray-800 truncate">
          {d.label.toUpperCase()}
        </div>
      </div>

      {/* Body */}
      {!d.isEnd && (
        <div className="px-3 py-2 text-xs text-gray-600">
          {d.agentCount === 0
            ? 'No agents'
            : `${d.agentCount} agent${d.agentCount > 1 ? 's' : ''}`}
        </div>
      )}

      {/* Handles */}
      <Handle type="target" position={Position.Top}    className="!bg-gray-400" />
      <Handle type="source" position={Position.Bottom} className="!bg-gray-400" />
    </motion.div>
  )
})

PhaseNode.displayName = 'PhaseNode'