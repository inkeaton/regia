# A Role used as a Value has one code, `R03_03-role-as-value`

A Role name written where a Value goes (`toast(Host)`, `?n + Guest`) had two codes: `R03_03-role-as-value` in chapter 03, with the hint to fill a Placeholder with `FROM Role ?x`, and `R15_01-role-name-as-value` in chapter 15, "as an argument or in an Expression". A tool builder couldn't tell which one the Transpiler reports, and a check case couldn't be written for both.

`R03_03-role-as-value` keeps the check and takes `R15_01-role-name-as-value`'s detail: "A Role name used as a Value, as an argument or in an Expression". **`R15_01-role-name-as-value` is retired.** Chapter 15 lists it as retired, pointing at `R03_03-role-as-value`, and the number is never reused (chapter 27).

`R03_03-role-as-value` was kept because chapter 03 is where Values are defined and where a writer looks for what can fill a slot, and because the guide already used it.

## Considered options

- **Keep `R15_01-role-name-as-value`, retire `R03_03-role-as-value`.** Chapter 15 is where Roles are defined, but the misuse is about what a Value is, and the hint is chapter 03's.
- **Split them**: `R03_03-role-as-value` for an argument, `R15_01-role-name-as-value` for an Expression. Two codes for one mistake, with the same fix.

## Consequences

- A Transpiler never reports `R15_01-role-name-as-value`. A check case annotated `R15_01-role-name-as-value` is wrong.
- Decided in the ticket *Decide: Diagnostic codes and the Vocabulary* (`.scratch/regia-spec-findings/issues/02-decide-diagnostic-codes.md`).
