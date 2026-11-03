# Bidirectional editing model

Type: grilling
Status: open
Blocked by: 01, 02, 26

## Question

How do edits on the Visual Editor's graph become edits to the Regia source? Building on the lossless-CST research (24), decide:
- Is the CST the model that edits are made on, or a read-only index used to patch text and reparse?
- Comment model: who owns a plain comment (leading/trailing trivia on tokens vs separate siblings). Doc comment attachment at the language level is settled in [Comment syntax](02-comment-syntax.md): directly above the declaration, no blank line.
- Indentation: absolute or relative to each block, and how optional `.`/`;` interact with DEDENT.
- Node identity across reparses: kept stable, or matched by structural hash as in Enso.
- How inserted nodes get formatted (elastic placeholders plus a formatter?).
- Is incremental parsing needed at all at Regia file sizes?

## Comments

- From Statement and block syntax: indentation and explicit `.`/`;` styles mix freely, and redundant terminators are allowed. Decide whether write-back preserves the user's style or normalises it.
