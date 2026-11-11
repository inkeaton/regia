# Write: The Logic of Regia

Type: task
Status: closed
Assignee: Edoardo Vassallo
Blocked by: 03

## Task

Write `docs/guide/1 - The Logic of Regia.md`.

Covers: How one writes in Regia: Agents, Roles, Playbooks, Plots, Directors and Phases, what a Playbook is and what a Plot is, and how they combine. Built around one small complete Program cut from the showcase and read line by line. Later chapters refer back to it.

Sources: glossary; 15, 20.

Follow the chapter template fixed in *Fix the chapter template with a sample chapter* (03) and the map's Notes. Take snippets from `docs/guide/showcase/`; if a construct has no natural place there, either add it to the showcase or tag it `#revise`. Finish by re-reading every example against the cited spec chapters.

## Resolution

Written on 2026-11-11: [`docs/guide/1 - The Logic of Regia.md`](../../../docs/guide/1%20-%20The%20Logic%20of%20Regia.md), about 2,050 words counting snippets and diagrams (roughly 1,650 of prose). Longer than the sample because later chapters refer back to it. Not yet read by the user.

- **The Program**: the banquet up to the toast, as cuts of five showcase files: `vocabulary.regia`, `playbooks/courtesy.regia`, `plots/royal_banquet.regia` (Roles `Host` and `Guest`, Phases `arrival`, `reception`, and `feast` with no Block), `playbooks/noble_socializing.regia` (the `idle` Plan with two Options), `banquet.regin` (`king` and `noble`, no Propensity values). Lines are only removed, never added, and the cuts together are a valid Program. No file was added to the showcase, and the showcase is unchanged.
- **Sections**: The Program; Names first; A Playbook; A Plot; Phases; A Playbook given for a while; From Roles to Agents; One run; How this combines with… (Failure, several Playbooks on one Agent, late Agents, Subplots); Since 1.0.
- **Diagrams**: a flowchart of who declares, gives and plays what, and a sequence diagram of one run.
- **Checked against**: spec chapters 15, 16 and 20 in full; 11 (an Event with no Plan is ignored), 21 (kinds, `ROOT`, `PLAYS`), 09 (Weights); the glossary.
- **Review notes**, two `#revise`:
  - New: a Playbook declares its Roles, but the Goals it expects to be asked and the Signals it sends are found only by reading its Plans. `Courtesy` and `RoyalBanquet` depend on each other through `take_seat` and `took_seat` with nothing declaring it.
  - `Host` and `host` told apart by case. This repeats a note already in the showcase README, with one addition (a Role is a class of Agents in a Plot and an address in a Playbook). *Write: Review List* should merge the two.
- **For the consistency pass**: later chapters can refer to this Program as "the Program of *The Logic of Regia*". The chapter explains Giving, Mapping, Role setup, Quota Trigger and Agent kind in one or two sentences each; the chapters that own them should not assume more than that.
- Five `#changes` lines, taken from spec chapters 15, 16 and 20 and primer chapter 5.
