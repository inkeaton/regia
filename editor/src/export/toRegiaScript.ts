import type {
  RegiaProject, Story, Phase, CondExpr, DoAction, Origin,
} from '../types/story'

const INDENT = '    '

export function projectToRegiaScript(project: RegiaProject): string {
  return project.stories
    .map((story) => storyToRgs(story))
    .join('\n\n')
}

// ── Story ────────────────────────────────────────────────────────────────────

function storyToRgs(story: Story): string {
  const lines: string[] = []

  lines.push(...docComment(story.doc, 0))

  if (story.isDefault) {
    lines.push('STORY DEFAULT.')
  } else {
    lines.push(`STORY ${story.name} PRIORITY ${story.priority ?? 1}.`)
  }

  // Story-level declarations
  story.actions.forEach((a) => lines.push(...docComment(a.doc, 1), `${INDENT}ACTION ${a.name}.`))
  story.events.forEach((e) => lines.push(...docComment(e.doc, 1), `${INDENT}EVENT ${pad(e.name)} ${e.origin}.`))
  story.conditions.forEach((c) => lines.push(...docComment(c.doc, 1), `${INDENT}CONDITION ${pad(c.name)} ${c.origin}.`))

  if (story.actions.length || story.events.length || story.conditions.length) {
    lines.push('')
  }

  // Phase declarations — exclude the synthetic ALWAYS phase
  const namedPhases = story.phases.filter((p) => !p.isAlways)
  namedPhases.forEach((p) => {
    lines.push(...docComment(p.doc, 1), `${INDENT}PHASE ${p.name}.`)
  })
  if (namedPhases.length) lines.push('')

  // DURING blocks — ALWAYS phases last, named phases in declared order
  const ordered = [
    ...story.phases.filter((p) => !p.isAlways),
    ...story.phases.filter((p) => p.isAlways),
  ]

  ordered.forEach((phase, idx) => {
    lines.push(...duringBlockToRgs(story, phase))
    if (idx < ordered.length - 1) lines.push('')
  })

  return lines.join('\n')
}

// ── DURING block ─────────────────────────────────────────────────────────────

function duringBlockToRgs(story: Story, phase: Phase): string[] {
  const lines: string[] = []
  const phaseRef = phase.isAlways ? 'ALWAYS' : phase.name

  lines.push(...docComment(phase.doc, 1))
  lines.push(`${INDENT}DURING ${phaseRef}:`)

  // Transition rules
  phase.transitions.forEach((t) => {
    lines.push(transitionToRgs(t.toPhase, t.eventName, t.origin, t.condition))
  })
  if (phase.transitions.length) lines.push('')

  // Agent blocks
  phase.agents.forEach((agent, idx) => {
    lines.push(...agentBlockToRgs(agent))
    if (idx < phase.agents.length - 1) lines.push('')
  })

  return lines
}

function transitionToRgs(
  toPhase: string,
  eventName: string,
  origin: Origin,
  condition?: CondExpr
): string {
  const target = toPhase === 'END' ? 'END' : toPhase
  const ifPart = condition ? ` IF ${condExprToRgs(condition)}` : ''
  return `${INDENT}${INDENT}TRANSITION TO ${target} WHEN ${eventName} ${origin}${ifPart}.`
}

// ── Agent block ──────────────────────────────────────────────────────────────

function agentBlockToRgs(agent: {
  agentName: string
  actions: { id: string; name: string; doc?: any }[]
  events: { id: string; name: string; origin: Origin; doc?: any }[]
  conditions: { id: string; name: string; origin: Origin; doc?: any }[]
  plans: {
    id: string; eventName: string; origin: Origin
    condition?: CondExpr; actions: DoAction[]; doc?: any
  }[]
}): string[] {
  const lines: string[] = []
  lines.push(`${INDENT}${INDENT}AGENT ${agent.agentName}:`)

  // Agent-local declarations
  agent.actions.forEach((a) =>
    lines.push(...docComment(a.doc, 3), `${INDENT}${INDENT}${INDENT}ACTION ${a.name}.`)
  )
  agent.events.forEach((e) =>
    lines.push(...docComment(e.doc, 3), `${INDENT}${INDENT}${INDENT}EVENT ${pad(e.name)} ${e.origin}.`)
  )
  agent.conditions.forEach((c) =>
    lines.push(...docComment(c.doc, 3), `${INDENT}${INDENT}${INDENT}CONDITION ${pad(c.name)} ${c.origin}.`)
  )

  // WHEN blocks
  agent.plans.forEach((plan) => {
    if (!plan.eventName) return  // skip incomplete plans
    lines.push(...whenBlockToRgs(plan))
  })

  return lines
}

// ── WHEN block ───────────────────────────────────────────────────────────────

function whenBlockToRgs(plan: {
  eventName: string; origin: Origin
  condition?: CondExpr; actions: DoAction[]; doc?: any
}): string[] {
  const lines: string[] = []
  const base = INDENT.repeat(3)

  lines.push(...docComment(plan.doc, 3))

  const ifPart = plan.condition ? ` IF ${condExprToRgs(plan.condition)}` : ''
  lines.push(`${base}WHEN ${plan.eventName} ${plan.origin}${ifPart}:`)

  // DO sequence
  if (plan.actions.length === 0) {
    lines.push(`${base}${INDENT}DO .`)  // placeholder — shouldn't normally happen
    return lines
  }

  plan.actions.forEach((action, idx) => {
    const isLast = idx === plan.actions.length - 1
    const suffix = isLast ? '.' : ','
    lines.push(`${base}${INDENT}${doActionToRgs(action)}${suffix}`)
  })

  return lines
}

function doActionToRgs(action: DoAction): string {
  switch (action.kind) {
    case 'believe': return `DO BELIEVE ${action.target}`
    case 'forget':  return `DO FORGET ${action.target}`
    default:        return `DO ${action.target}`
  }
}

// ── Condition expression ───────────────────────────────────────────────────────

function condExprToRgs(expr: CondExpr): string {
  const ands = expr.ands.map((and) =>
    and.terms
      .map((term) => `${term.negated ? 'NOT ' : ''}${term.name} ${term.origin}`)
      .join(' AND ')
  )
  return ands.join(' OR ')
}

// ── Doc comments ─────────────────────────────────────────────────────────────

function docComment(
  doc: { name?: string; meaning?: string } | undefined,
  level: number
): string[] {
  if (!doc) return []
  const lines: string[] = []
  const prefix = INDENT.repeat(level)
  if (doc.name)    lines.push(`${prefix}# @NAME: ${doc.name}`)
  if (doc.meaning) lines.push(`${prefix}# @MEANING: ${doc.meaning}`)
  return lines
}

// ── Padding for alignment (cosmetic) ────────────────────────────────────────

function pad(name: string): string {
  return name.padEnd(16)
}