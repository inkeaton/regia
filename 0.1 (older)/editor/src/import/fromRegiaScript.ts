import { nanoid } from 'nanoid'
import { tokenize, type Token } from './tokenizer'
import { ImportError } from './errors'
import type {
  RegiaProject, Story, Phase, AgentInPhase, Plan, TransitionRule,
  DoAction, CondExpr, CondAtom, Origin, ActionDecl, EventDecl, ConditionDecl,
} from '../types/story'

const ORIGINS = new Set(['ENVIRONMENT', 'DIRECTOR', 'MYSELF', 'PLAYER', 'TIMER'])

// ── Parser cursor ──────────────────────────────────────────────────────────────

class Cursor {
  private tokens: Token[];
  private pos: number;

  constructor(tokens: Token[], pos = 0) {
    this.tokens = tokens;
    this.pos = pos;
  }

  peek(offset = 0): Token { return this.tokens[this.pos + offset] }
  at(type: string): boolean { return this.peek().type === type }
  advance(): Token { return this.tokens[this.pos++] }

  expect(type: string): Token {
    const t = this.peek()
    if (t.type !== type) {
      throw new ImportError(
        `Expected ${type} but found ${t.type}${t.value ? ` ('${t.value}')` : ''}`,
        t.line, t.col
      )
    }
    return this.advance()
  }

  // First non-DOC_COMMENT token type ahead — for lookahead decisions
  peekKind(): string {
    let i = 0
    while (this.peek(i).type === 'DOC_COMMENT') i++
    return this.peek(i).type
  }

  consumeDocComments(): { name?: string; meaning?: string } | undefined {
    let doc: { name?: string; meaning?: string } | undefined
    while (this.at('DOC_COMMENT')) {
      const text = this.advance().value.trim()
      const m = text.match(/^@([A-Za-z]+):\s*(.*)$/)
      if (m) {
        doc = doc ?? {}
        const key = m[1].toUpperCase()
        if (key === 'NAME')    doc.name    = m[2].trim()
        if (key === 'MEANING') doc.meaning = m[2].trim()
      }
    }
    return doc
  }

  expectOrigin(): Origin {
    const t = this.peek()
    if (!ORIGINS.has(t.type)) {
      throw new ImportError(
        `Expected an origin (ENVIRONMENT, DIRECTOR, MYSELF, PLAYER, or TIMER) but found ${t.type}`,
        t.line, t.col
      )
    }
    this.advance()
    return t.type as Origin
  }
}

// ── Entry point ──────────────────────────────────────────────────────────────

export function parseRegiaScript(source: string): RegiaProject {
  const c = new Cursor(tokenize(source))
  const stories: Story[] = []

  while (!c.at('EOF')) {
    stories.push(parseStoryDef(c))
  }

  return { version: '1.0', stories }
}

// ── Story ────────────────────────────────────────────────────────────────────

function parseStoryDef(c: Cursor): Story {
  const doc = c.consumeDocComments()
  c.expect('STORY')

  if (c.at('DEFAULT')) {
    c.advance()
    c.expect('PERIOD')
    const story: Story = {
      id: nanoid(), name: 'DEFAULT', priority: null, isDefault: true,
      actions: [], events: [], conditions: [], phases: [], doc,
    }
    parseDuringBlocks(c, story)
    return story
  }

  const nameTok = c.expect('ID')
  c.expect('PRIORITY')
  const priorityTok = c.expect('NUMBER')
  c.expect('PERIOD')

  const story: Story = {
    id: nanoid(), name: nameTok.value, priority: parseInt(priorityTok.value, 10),
    isDefault: false, actions: [], events: [], conditions: [], phases: [], doc,
  }

  // declaration*
  while (['ACTION', 'EVENT', 'CONDITION'].includes(c.peekKind())) {
    parseDeclarationInto(c, story.actions, story.events, story.conditions)
  }

  // phaseDecl*
  while (c.peekKind() === 'PHASE') {
    story.phases.push(parsePhaseDecl(c))
  }

  parseDuringBlocks(c, story)
  return story
}

// ── Declarations ─────────────────────────────────────────────────────────────

function parseDeclarationInto(
  c: Cursor,
  actions: ActionDecl[], events: EventDecl[], conditions: ConditionDecl[]
) {
  const doc = c.consumeDocComments()

  if (c.at('ACTION')) {
    c.advance()
    const name = c.expect('ID').value
    c.expect('PERIOD')
    actions.push({ id: nanoid(), name, doc })
    return
  }
  if (c.at('EVENT')) {
    c.advance()
    const name = c.expect('ID').value
    const origin = c.expectOrigin()
    c.expect('PERIOD')
    events.push({ id: nanoid(), name, origin, doc })
    return
  }
  if (c.at('CONDITION')) {
    c.advance()
    const name = c.expect('ID').value
    const origin = c.expectOrigin()
    c.expect('PERIOD')
    conditions.push({ id: nanoid(), name, origin, doc })
    return
  }

  const t = c.peek()
  throw new ImportError(`Expected ACTION, EVENT, or CONDITION but found ${t.type}`, t.line, t.col)
}

// ── Phase declaration ────────────────────────────────────────────────────────

function parsePhaseDecl(c: Cursor): Phase {
  const doc = c.consumeDocComments()
  c.expect('PHASE')
  const name = c.expect('ID').value
  c.expect('PERIOD')
  return {
    id: nanoid(), name, isAlways: false, isInitial: false,
    agents: [], transitions: [], doc,
  }
}

// ── During blocks ────────────────────────────────────────────────────────────

function parseDuringBlocks(c: Cursor, story: Story) {
  // First declared phase is the initial phase
  if (story.phases.length > 0) {
    story.phases[0].isInitial = true
  }

  while (c.peekKind() === 'DURING') {
    parseDuringBlock(c, story)
  }
}

function parseDuringBlock(c: Cursor, story: Story) {
  const doc = c.consumeDocComments()
  c.expect('DURING')

  let phase: Phase

  if (c.at('ALWAYS')) {
    c.advance()
    let existing = story.phases.find((p) => p.isAlways)
    if (!existing) {
      existing = {
        id: nanoid(), name: 'ALWAYS', isAlways: true, isInitial: false,
        agents: [], transitions: [], doc,
      }
      story.phases.push(existing)
    } else if (doc) {
      existing.doc = { ...existing.doc, ...doc }
    }
    phase = existing
  } else {
    const idTok = c.expect('ID')
    const existing = story.phases.find((p) => p.name === idTok.value && !p.isAlways)
    if (!existing) {
      throw new ImportError(
        `DURING references undeclared phase '${idTok.value}'`,
        idTok.line, idTok.col
      )
    }
    if (doc) existing.doc = { ...existing.doc, ...doc }
    phase = existing
  }

  c.expect('COLON')

  while (c.peekKind() === 'TRANSITION') {
    phase.transitions.push(parseTransitionRule(c))
  }

  while (c.peekKind() === 'AGENT') {
    parseAgentBlock(c, phase)
  }
}

// ── Transition rule ──────────────────────────────────────────────────────────

function parseTransitionRule(c: Cursor): TransitionRule {
  c.consumeDocComments()  // not stored — TransitionRule has no doc field
  c.expect('TRANSITION')
  c.expect('TO')

  let toPhase: string
  if (c.at('END')) {
    c.advance()
    toPhase = 'END'
  } else {
    toPhase = c.expect('ID').value
  }

  c.expect('WHEN')
  const eventName = c.expect('ID').value
  const origin = c.expectOrigin()

  let condition: CondExpr | undefined
  if (c.at('IF')) {
    c.advance()
    condition = parseCondExpr(c)
  }

  c.expect('PERIOD')
  return { id: nanoid(), toPhase, eventName, origin, condition }
}

// ── Agent block ──────────────────────────────────────────────────────────────

function parseAgentBlock(c: Cursor, phase: Phase) {
  c.consumeDocComments()
  c.expect('AGENT')
  const name = c.expect('ID').value
  c.expect('COLON')

  let agent = phase.agents.find((a) => a.agentName === name)
  if (!agent) {
    agent = { agentName: name, actions: [], events: [], conditions: [], plans: [] }
    phase.agents.push(agent)
  }

  while (true) {
    const kind = c.peekKind()
    if (kind === 'ACTION' || kind === 'EVENT' || kind === 'CONDITION') {
      parseDeclarationInto(c, agent.actions, agent.events, agent.conditions)
    } else if (kind === 'WHEN') {
      agent.plans.push(parseWhenBlock(c))
    } else {
      break
    }
  }
}

// ── When block ───────────────────────────────────────────────────────────────

function parseWhenBlock(c: Cursor): Plan {
  const doc = c.consumeDocComments()
  c.expect('WHEN')
  const eventName = c.expect('ID').value
  const origin = c.expectOrigin()

  let condition: CondExpr | undefined
  if (c.at('IF')) {
    c.advance()
    condition = parseCondExpr(c)
  }

  c.expect('COLON')
  const actions = parseDoSequence(c)

  return { id: nanoid(), eventName, origin, condition, actions, doc }
}

// ── Do sequence ──────────────────────────────────────────────────────────────

function parseDoSequence(c: Cursor): DoAction[] {
  const actions: DoAction[] = [parseDoAction(c)]
  while (c.at('COMMA')) {
    c.advance()
    actions.push(parseDoAction(c))
  }
  c.expect('PERIOD')
  return actions
}

function parseDoAction(c: Cursor): DoAction {
  c.expect('DO')
  if (c.at('BELIEVE')) {
    c.advance()
    return { kind: 'believe', target: c.expect('ID').value }
  }
  if (c.at('FORGET')) {
    c.advance()
    return { kind: 'forget', target: c.expect('ID').value }
  }
  return { kind: 'action', target: c.expect('ID').value }
}

// ── Condition expressions — parse to AST, normalize to DNF ───────────────────

type CAst =
  | { kind: 'atom'; name: string; origin: Origin }
  | { kind: 'not';  expr: CAst }
  | { kind: 'and';  items: CAst[] }
  | { kind: 'or';   items: CAst[] }

function parseCondExpr(c: Cursor): CondExpr {
  const ast = parseOrAst(c)
  const dnf = astToDNF(ast)
  return { ands: dnf.map((terms) => ({ terms })) }
}

function parseOrAst(c: Cursor): CAst {
  const items = [parseAndAst(c)]
  while (c.at('OR')) {
    c.advance()
    items.push(parseAndAst(c))
  }
  return items.length === 1 ? items[0] : { kind: 'or', items }
}

function parseAndAst(c: Cursor): CAst {
  const items = [parseTermAst(c)]
  while (c.at('AND')) {
    c.advance()
    items.push(parseTermAst(c))
  }
  return items.length === 1 ? items[0] : { kind: 'and', items }
}

function parseTermAst(c: Cursor): CAst {
  if (c.at('NOT')) {
    c.advance()
    return { kind: 'not', expr: parseAtomAst(c) }
  }
  return parseAtomAst(c)
}

function parseAtomAst(c: Cursor): CAst {
  if (c.at('LPAREN')) {
    c.advance()
    const expr = parseOrAst(c)
    c.expect('RPAREN')
    return expr
  }
  const name = c.expect('ID').value
  const origin = c.expectOrigin()
  return { kind: 'atom', name, origin }
}

// ── AST → DNF (disjunctive normal form) via De Morgan + distribution ─────────

type Conjunction = CondAtom[]

function astToDNF(ast: CAst): Conjunction[] {
  switch (ast.kind) {
    case 'atom':
      return [[{ type: 'condition', name: ast.name, origin: ast.origin, negated: false }]]

    case 'not':
      return negateDNF(astToDNF(ast.expr))

    case 'and': {
      let result: Conjunction[] = [[]]
      for (const item of ast.items) {
        const child = astToDNF(item)
        const next: Conjunction[] = []
        for (const r of result) {
          for (const cterm of child) {
            next.push([...r, ...cterm])
          }
        }
        result = next
      }
      return result
    }

    case 'or': {
      const result: Conjunction[] = []
      for (const item of ast.items) {
        result.push(...astToDNF(item))
      }
      return result
    }
  }
}

// NOT(A1 OR A2 OR ...) = NOT(A1) AND NOT(A2) AND ...
// NOT(conjunction)     = OR of negated atoms in that conjunction
function negateDNF(dnf: Conjunction[]): Conjunction[] {
  let result: Conjunction[] = [[]]
  for (const conj of dnf) {
    const negatedAtoms: Conjunction[] = conj.map((atom) => [
      { ...atom, negated: !atom.negated },
    ])
    const next: Conjunction[] = []
    for (const r of result) {
      for (const c of negatedAtoms) {
        next.push([...r, ...c])
      }
    }
    result = next
  }
  return result
}