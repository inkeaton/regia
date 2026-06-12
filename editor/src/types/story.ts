// ── Origin tags ───────────────────────────────────────────────────────────────

export type Origin =
  | 'ENVIRONMENT'
  | 'DIRECTOR'
  | 'MYSELF'
  | 'PLAYER'
  | 'TIMER'

// ── Declarations ──────────────────────────────────────────────────────────────

export interface ActionDecl {
  id:   string
  name: string
  doc?: { name?: string; meaning?: string }
}

export interface EventDecl {
  id:     string
  name:   string
  origin: Origin
  doc?:   { name?: string; meaning?: string }
}

export interface ConditionDecl {
  id:     string
  name:   string
  origin: Origin
  doc?:   { name?: string; meaning?: string }
}

// ── Condition expression (mirrors grammar) ────────────────────────────────────

export type CondAtom =
  | { type: 'condition'; name: string; origin: Origin; negated: boolean }

export type CondAnd  = { terms: CondAtom[] }
export type CondExpr = { ands: CondAnd[] }   // ands joined by OR

// ── Plan (WHEN block) ─────────────────────────────────────────────────────────

export interface DoAction {
  kind:      'action' | 'believe' | 'forget'
  target:    string
}

export interface Plan {
  id:         string
  eventName:  string
  origin:     Origin
  condition?: CondExpr
  actions:    DoAction[]
  doc?:       { name?: string; meaning?: string }
}

// ── Transition rule ───────────────────────────────────────────────────────────

export interface TransitionRule {
  id:          string
  toPhase:     string | 'END'
  eventName:   string
  origin:      Origin
  condition?:  CondExpr
}

// ── Agent ─────────────────────────────────────────────────────────────────────

export interface AgentInPhase {
  agentName:  string
  actions:    ActionDecl[]
  events:     EventDecl[]
  conditions: ConditionDecl[]
  plans:      Plan[]
}

// ── Phase ─────────────────────────────────────────────────────────────────────

export interface Phase {
  id:          string
  name:        string
  isAlways:    boolean
  isInitial:   boolean
  agents:      AgentInPhase[]
  transitions: TransitionRule[]
  doc?:        { name?: string; meaning?: string }
}

// ── Story ─────────────────────────────────────────────────────────────────────

export interface Story {
  id:         string
  name:       string
  priority:   number | null   // null for DEFAULT
  isDefault:  boolean
  actions:    ActionDecl[]
  events:     EventDecl[]
  conditions: ConditionDecl[]
  phases:     Phase[]
  doc?:       { name?: string; meaning?: string }
}

// ── Project (top-level file model) ────────────────────────────────────────────

export interface RegiaProject {
  version:  string
  stories:  Story[]
}