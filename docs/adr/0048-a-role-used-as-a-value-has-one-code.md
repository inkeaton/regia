# A Role used as a Value has one code, `R0303`

A Role name written where a Value goes (`toast(Host)`, `?n + Guest`) had two codes: `R0303` in chapter 03, with the hint to fill a Placeholder with `FROM Role ?x`, and `R1501` in chapter 15, "as an argument or in an Expression". A tool builder couldn't tell which one the Transpiler reports, and a check case couldn't be written for both.

`R0303` keeps the check and takes `R1501`'s detail: "A Role name used as a Value, as an argument or in an Expression". **`R1501` is retired.** Chapter 15 lists it as retired, pointing at `R0303`, and the number is never reused (chapter 27).

`R0303` was kept because chapter 03 is where Values are defined and where a writer looks for what can fill a slot, and because the guide already used it.

## Considered options

- **Keep `R1501`, retire `R0303`.** Chapter 15 is where Roles are defined, but the misuse is about what a Value is, and the hint is chapter 03's.
- **Split them**: `R0303` for an argument, `R1501` for an Expression. Two codes for one mistake, with the same fix.

## Consequences

- A Transpiler never reports `R1501`. A check case annotated `R1501` is wrong.
- Decided in the ticket *Decide: Diagnostic codes and the Vocabulary* (`.scratch/regia-spec-findings/issues/02-decide-diagnostic-codes.md`).
