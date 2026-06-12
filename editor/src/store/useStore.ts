import { create } from 'zustand'
import type  {
  RegiaProject, Story, Phase, ActionDecl, EventDecl,
  ConditionDecl, AgentInPhase, Plan, TransitionRule, Origin
} from '../types/story'
import { nanoid } from 'nanoid'

// Install nanoid for generating unique IDs
// npm install nanoid

interface EditorState {
  project:        RegiaProject
  activeStoryId:  string | null
  activePhaseId:  string | null

  // Project actions
  setProject:     (project: RegiaProject) => void

  // Story actions
  addStory:       (isDefault?: boolean) => void
  updateStory:    (id: string, patch: Partial<Story>) => void
  deleteStory:    (id: string) => void
  setActiveStory: (id: string | null) => void

  // Phase actions
  addPhase:       (storyId: string) => void
  updatePhase:    (storyId: string, phaseId: string, patch: Partial<Phase>) => void
  deletePhase:    (storyId: string, phaseId: string) => void
  setActivePhase: (id: string | null) => void

  // Selection
  activeTransitionId: string | null
  setActiveTransition: (id: string | null) => void

  // Story-level declarations
  addAction:    (storyId: string) => void
  updateAction: (storyId: string, id: string, patch: Partial<ActionDecl>) => void
  deleteAction: (storyId: string, id: string) => void

  addEvent:    (storyId: string) => void
  updateEvent: (storyId: string, id: string, patch: Partial<EventDecl>) => void
  deleteEvent: (storyId: string, id: string) => void

  addCondition:    (storyId: string) => void
  updateCondition: (storyId: string, id: string, patch: Partial<ConditionDecl>) => void
  deleteCondition: (storyId: string, id: string) => void

  // Agents within a phase
  addAgentToPhase:      (storyId: string, phaseId: string) => void
  updateAgentInPhase:   (storyId: string, phaseId: string, agentName: string, patch: Partial<AgentInPhase>) => void
  removeAgentFromPhase: (storyId: string, phaseId: string, agentName: string) => void

  // Plans (WHEN blocks)
  addPlan:    (storyId: string, phaseId: string, agentName: string) => void
  updatePlan: (storyId: string, phaseId: string, agentName: string, planId: string, patch: Partial<Plan>) => void
  deletePlan: (storyId: string, phaseId: string, agentName: string, planId: string) => void

  // Transitions
  addTransition:    (storyId: string, phaseId: string, toPhase: string) => string
  updateTransition: (storyId: string, phaseId: string, transitionId: string, patch: Partial<TransitionRule>) => void
  deleteTransition: (storyId: string, phaseId: string, transitionId: string) => void
}

const emptyProject = (): RegiaProject => ({
  version: '1.0',
  stories: [],
})

export const useStore = create<EditorState>((set, get) => ({
  project:       emptyProject(),
  activeStoryId: null,
  activePhaseId: null,

  setProject: (project) => set({ project }),

  addStory: (isDefault = false) => {
    const story: Story = {
      id:         nanoid(),
      name:       isDefault ? 'DEFAULT' : 'new_story',
      priority:   isDefault ? null : 1,
      isDefault,
      actions:    [],
      events:     [],
      conditions: [],
      phases:     [],
    }
    set((s) => ({
      project: {
        ...s.project,
        stories: [...s.project.stories, story],
      },
      activeStoryId: story.id,
    }))
  },

  updateStory: (id, patch) =>
    set((s) => ({
      project: {
        ...s.project,
        stories: s.project.stories.map((story) =>
          story.id === id ? { ...story, ...patch } : story
        ),
      },
    })),

  deleteStory: (id) =>
    set((s) => ({
      project: {
        ...s.project,
        stories: s.project.stories.filter((story) => story.id !== id),
      },
      activeStoryId: s.activeStoryId === id ? null : s.activeStoryId,
    })),

  setActiveStory: (id) => set({ activeStoryId: id, activePhaseId: null }),

  addPhase: (storyId) => {
    const story = get().project.stories.find((s) => s.id === storyId)
    if (!story) return
    const phase: Phase = {
      id:          nanoid(),
      name:        'new_phase',
      isAlways:    false,
      isInitial:   story.phases.length === 0,
      agents:      [],
      transitions: [],
    }
    set((s) => ({
      project: {
        ...s.project,
        stories: s.project.stories.map((st) =>
          st.id === storyId
            ? { ...st, phases: [...st.phases, phase] }
            : st
        ),
      },
      activePhaseId: phase.id,
    }))
  },

  updatePhase: (storyId, phaseId, patch) =>
    set((s) => ({
      project: {
        ...s.project,
        stories: s.project.stories.map((st) =>
          st.id === storyId
            ? {
                ...st,
                phases: st.phases.map((ph) =>
                  ph.id === phaseId ? { ...ph, ...patch } : ph
                ),
              }
            : st
        ),
      },
    })),

  deletePhase: (storyId, phaseId) =>
    set((s) => ({
      project: {
        ...s.project,
        stories: s.project.stories.map((st) =>
          st.id === storyId
            ? { ...st, phases: st.phases.filter((ph) => ph.id !== phaseId) }
            : st
        ),
      },
    })),
    activeTransitionId: null,
  setActiveTransition: (id) => set({ activeTransitionId: id }),

  // ── Story-level declarations ─────────────────────────────────────────────

  addAction: (storyId) =>
    set((s) => ({
      project: mapStory(s.project, storyId, (story) => ({
        ...story,
        actions: [...story.actions, { id: nanoid(), name: 'new_action' }],
      })),
    })),

  updateAction: (storyId, id, patch) =>
    set((s) => ({
      project: mapStory(s.project, storyId, (story) => ({
        ...story,
        actions: story.actions.map((a) => (a.id === id ? { ...a, ...patch } : a)),
      })),
    })),

  deleteAction: (storyId, id) =>
    set((s) => ({
      project: mapStory(s.project, storyId, (story) => ({
        ...story,
        actions: story.actions.filter((a) => a.id !== id),
      })),
    })),

  addEvent: (storyId) =>
    set((s) => ({
      project: mapStory(s.project, storyId, (story) => ({
        ...story,
        events: [...story.events, { id: nanoid(), name: 'new_event', origin: 'ENVIRONMENT' as Origin }],
      })),
    })),

  updateEvent: (storyId, id, patch) =>
    set((s) => ({
      project: mapStory(s.project, storyId, (story) => ({
        ...story,
        events: story.events.map((e) => (e.id === id ? { ...e, ...patch } : e)),
      })),
    })),

  deleteEvent: (storyId, id) =>
    set((s) => ({
      project: mapStory(s.project, storyId, (story) => ({
        ...story,
        events: story.events.filter((e) => e.id !== id),
      })),
    })),

  addCondition: (storyId) =>
    set((s) => ({
      project: mapStory(s.project, storyId, (story) => ({
        ...story,
        conditions: [...story.conditions, { id: nanoid(), name: 'new_condition', origin: 'MYSELF' as Origin }],
      })),
    })),

  updateCondition: (storyId, id, patch) =>
    set((s) => ({
      project: mapStory(s.project, storyId, (story) => ({
        ...story,
        conditions: story.conditions.map((c) => (c.id === id ? { ...c, ...patch } : c)),
      })),
    })),

  deleteCondition: (storyId, id) =>
    set((s) => ({
      project: mapStory(s.project, storyId, (story) => ({
        ...story,
        conditions: story.conditions.filter((c) => c.id !== id),
      })),
    })),

  // ── Agents within a phase ─────────────────────────────────────────────────

  addAgentToPhase: (storyId, phaseId) =>
    set((s) => ({
      project: mapPhase(s.project, storyId, phaseId, (phase) => ({
        ...phase,
        agents: [
          ...phase.agents,
          { agentName: 'NewAgent', actions: [], events: [], conditions: [], plans: [] },
        ],
      })),
    })),

  updateAgentInPhase: (storyId, phaseId, agentName, patch) =>
    set((s) => ({
      project: mapPhase(s.project, storyId, phaseId, (phase) => ({
        ...phase,
        agents: phase.agents.map((a) =>
          a.agentName === agentName ? { ...a, ...patch } : a
        ),
      })),
    })),

  removeAgentFromPhase: (storyId, phaseId, agentName) =>
    set((s) => ({
      project: mapPhase(s.project, storyId, phaseId, (phase) => ({
        ...phase,
        agents: phase.agents.filter((a) => a.agentName !== agentName),
      })),
    })),

  // ── Plans ──────────────────────────────────────────────────────────────────

  addPlan: (storyId, phaseId, agentName) =>
    set((s) => ({
      project: mapPhase(s.project, storyId, phaseId, (phase) => ({
        ...phase,
        agents: phase.agents.map((a) =>
          a.agentName === agentName
            ? {
                ...a,
                plans: [
                  ...a.plans,
                  {
                    id: nanoid(),
                    eventName: '',
                    origin: 'ENVIRONMENT' as Origin,
                    actions: [],
                  },
                ],
              }
            : a
        ),
      })),
    })),

  updatePlan: (storyId, phaseId, agentName, planId, patch) =>
    set((s) => ({
      project: mapPhase(s.project, storyId, phaseId, (phase) => ({
        ...phase,
        agents: phase.agents.map((a) =>
          a.agentName === agentName
            ? {
                ...a,
                plans: a.plans.map((p) => (p.id === planId ? { ...p, ...patch } : p)),
              }
            : a
        ),
      })),
    })),

  deletePlan: (storyId, phaseId, agentName, planId) =>
    set((s) => ({
      project: mapPhase(s.project, storyId, phaseId, (phase) => ({
        ...phase,
        agents: phase.agents.map((a) =>
          a.agentName === agentName
            ? { ...a, plans: a.plans.filter((p) => p.id !== planId) }
            : a
        ),
      })),
    })),

  // ── Transitions ────────────────────────────────────────────────────────────

  addTransition: (storyId, phaseId, toPhase) => {
    const newId = nanoid()
    set((s) => ({
      project: mapPhase(s.project, storyId, phaseId, (phase) => ({
        ...phase,
        transitions: [
          ...phase.transitions,
          { id: newId, toPhase, eventName: '', origin: 'ENVIRONMENT' as Origin },
        ],
      })),
    }))
    return newId
  },

  updateTransition: (storyId, phaseId, transitionId, patch) =>
    set((s) => ({
      project: mapPhase(s.project, storyId, phaseId, (phase) => ({
        ...phase,
        transitions: phase.transitions.map((t) =>
          t.id === transitionId ? { ...t, ...patch } : t
        ),
      })),
    })),

  deleteTransition: (storyId, phaseId, transitionId) =>
    set((s) => ({
      project: mapPhase(s.project, storyId, phaseId, (phase) => ({
        ...phase,
        transitions: phase.transitions.filter((t) => t.id !== transitionId),
      })),
    })),

  setActivePhase: (id) => set({ activePhaseId: id }),
}))

// ── Helpers ──────────────────────────────────────────────────────────────────

function mapStory(
  project: RegiaProject,
  storyId: string,
  fn: (story: Story) => Story
): RegiaProject {
  return {
    ...project,
    stories: project.stories.map((s) => (s.id === storyId ? fn(s) : s)),
  }
}

function mapPhase(
  project: RegiaProject,
  storyId: string,
  phaseId: string,
  fn: (phase: Phase) => Phase
): RegiaProject {
  return mapStory(project, storyId, (story) => ({
    ...story,
    phases: story.phases.map((p) => (p.id === phaseId ? fn(p) : p)),
  }))
}
