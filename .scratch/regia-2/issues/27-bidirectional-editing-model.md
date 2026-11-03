# Bidirectional editing model

Type: grilling
Status: open
Blocked by: 01, 02, 26

## Question

How do edits on the Visual Editor's graph become edits to the Regia source? Building on the lossless-CST research (24), decide:
- Is the CST the model that edits are made on, or a read-only index used to patch text and reparse?
- Comment model: who owns a comment, leading/trailing on tokens vs separate siblings, and where `#@` doc comments attach.
- Indentation: absolute or relative to each block, and how optional `.`/`;` interact with DEDENT.
- Node identity across reparses: kept stable, or matched by structural hash as in Enso.
- How inserted nodes get formatted (elastic placeholders plus a formatter?).
- Is incremental parsing needed at all at Regia file sizes?
