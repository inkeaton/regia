# Findings

Spec contradictions, gaps and glossary problems found while working the *Regia 1.5 showcase and guide* map. One line each: what, where, and the ticket that found it. Fixing them is a later spec effort, unless one blocks a chapter.


- The Quota quantity writes `n OF` as `of(k)` (chapter 33, *Quantity*), while `regia.pick` writes it as `count(N)` (chapters 35, 39); `n% OF` is `share(…)` in both since *Rename generated ASL names built on retired words*. One of the two should give way. Quotas are 2.0 only, so it doesn't block a 1.5 chapter.
- Chapter 21, *Agent kinds*: "With no Body, the header ends with `.`" is a rule from before the syntax review; a trailing `.` is silent now (chapter 01), and the chapter's own examples (`KIND servant, PLAYS Servant`) write none. Found by *Bring the showcase to the 1.5 syntax*.
- Trailing `.` is still written in some spec examples and inline quotes (about 17 quotes such as `DO clear_tables.` in chapter 30 and `DROP strike.` in chapter 40, and code in chapter 38, lines 12–16 and 94), against chapter 01's "no trailing `.`" default. Harmless, since the dot is silent. Found by *Bring the showcase to the 1.5 syntax*.
- Chapter 02, *Transpiler checks*: `R0201` is "an unclosed multiline comment", but the chapter calls only `#[ … ]#` a multiline comment; whether an unclosed `#@key[` (a multiline Doc comment) is also `R0201` isn't said. The guide reads it as yes. Found by *Write guide chapter 02, Syntax*.
- Chapter 10, *What the game produces*, says `GAME` goes on `FACT` and `CUE` only, but `R1016` lists only `GOAL`, `ACTION`, `NAME` and local declarations: `GAME TRAIT` / `GAME MOOD` has no code. Found by *Write guide chapter 03, Vocabulary and files*.
- Chapter 03, *Names are declared*: "Agent names are never Names", while chapter 21, *Individual Agents*, calls an Agent's name "a Name inside Instancing" that a Plan "meets at runtime as an ordinary Name". The two should use one wording; the guide follows chapter 21. Found by *Write guide chapter 03, Vocabulary and files*.
- `GLOSSARY.md`: *Vocabulary* lists Facts, Cues, Actions, Goals and Propensities and doesn't say whether declared Names belong to it; and *Mood* ends with a stray second line, `_Avoid_: Notification, message`, apparently left from a removed entry. Found by *Write guide chapter 03, Vocabulary and files*.
- Chapter 10, `R1005`, lists kind, parameter count and External name; the text above it (*What the game produces*) adds disagreeing on `GAME`. The check's line should name `GAME` too. Found by *Write guide chapter 03, Vocabulary and files*.
