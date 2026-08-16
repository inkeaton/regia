import type { Program, PlotDef } from "../types/ast";

// ==============================================================================
// HELPERS
// ==============================================================================

/**
 * Inserts lines into the source code at the specified line number (1-indexed).
 * If the line is beyond the current lines, appends to the end.
 */
function insertLines(code: string, lineNumber: number, linesToInsert: string[]): string {
    const lines = code.split("\n");
    // Line number is 1-indexed, array is 0-indexed.
    // Inserting at lineNumber 5 means it becomes the new line 5 (index 4).
    const index = Math.max(0, Math.min(lineNumber - 1, lines.length));
    
    lines.splice(index, 0, ...linesToInsert);
    return lines.join("\n");
}

function toSnakeCase(str: string): string {
    return str
        .replace(/\W+/g, " ")
        .split(/ |\B(?=[A-Z])/)
        .map(word => word.toLowerCase())
        .join('_')
        .replace(/_+/g, "_") // remove double underscores
        .trim();
}

// ==============================================================================
// PUBLIC API
// ==============================================================================

/**
 * Adds a new Phase to the source code.
 * 1. Adds `PHASE name.` after the last PhaseDecl.
 * 2. Adds `DURING name:` after the last DuringBlock.
 */
export function addPhase(code: string, ast: Program, rawName: string): string {
    const plot = ast.items?.find((item) => item.type === "PlotDef") as PlotDef | undefined;
    if (!plot) return code; // Should not happen if graph is rendered

    const name = toSnakeCase(rawName);

    let newCode = code;

    // 1. Insert PhaseDecl
    // Find the last phase declaration
    const lastPhase = plot.phases.length > 0 ? plot.phases[plot.phases.length - 1] : null;
    let phaseInsertLine = plot.loc.line + 1; // Fallback to right after PLOT definition
    if (lastPhase) {
        phaseInsertLine = lastPhase.loc.line + 1; // Insert after the last phase
    }

    newCode = insertLines(newCode, phaseInsertLine, [`    PHASE ${name}.`]);

    // Re-split lines because we added one, which shifts all subsequent line numbers by +1
    // We need to account for this shift when calculating the DURING insert line.
    
    // 2. Insert DuringBlock
    // Infer the end of the last during block
    // We don't have loc_end. A DuringBlock goes until the next DuringBlock, or EOF.
    let duringInsertLine = newCode.split("\n").length + 1; // Default to EOF

    // Note: since we inserted a line above, the original line numbers below phaseInsertLine
    // are now shifted by +1. But we just append to the end anyway, so EOF is safe.
    // To be precise, if there's anything after PlotDef (which shouldn't be per grammar),
    // it would be tricky. Appending to EOF is the safest heuristic for Regia.

    newCode = insertLines(newCode, duringInsertLine, [
        "",
        `    DURING ${name}:`,
        `        ON ENTER:`,
        `            WORLD DO PRINT ("${name} started").`,
        ""
    ]);

    return newCode;
}

/**
 * Adds a transition to the source code.
 * Adds `WHEN {event}: TRANSITION TO {target}.` inside the source Phase's DuringBlock.
 * If the event doesn't exist in the AST, it also creates `EVENT {event}.` at the top level.
 */
export function addTransition(
    code: string,
    ast: Program,
    sourcePhaseName: string,
    targetPhaseName: string,
    rawEventName: string
): string {
    const plot = ast.items?.find((item) => item.type === "PlotDef") as PlotDef | undefined;
    if (!plot) return code;

    const eventName = toSnakeCase(rawEventName);
    let newCode = code;
    let linesShifted = 0;

    // 1. Check if event exists. If not, add it before PLOT
    const events = ast.items?.filter((item) => item.type === "EventDecl") || [];
    // @ts-ignore
    const eventExists = events.some((e: any) => e.name === eventName);
    
    if (!eventExists) {
        // Insert right before PLOT
        const plotLine = plot.loc.line;
        newCode = insertLines(newCode, plotLine, [`EVENT ${eventName}.`, ""]);
        linesShifted += 2;
    }

    // 2. Insert inside the DuringBlock
    const sourceBlock = plot.during_blocks.find((b) => b.phase_name === sourcePhaseName);
    if (!sourceBlock) return newCode;

    // Find the end of this DuringBlock to append the WHEN block
    let endOfBlockLine = newCode.split("\n").length + 1; // Default to EOF

    // Find the next block in the list to determine where this one ends
    const index = plot.during_blocks.indexOf(sourceBlock);
    if (index >= 0 && index < plot.during_blocks.length - 1) {
        // The next block's start line (adjusted for the lines we might have shifted above)
        endOfBlockLine = plot.during_blocks[index + 1].loc.line + linesShifted;
    } else {
        // It's the last block, so insert at EOF
    }

    newCode = insertLines(newCode, endOfBlockLine, [
        `    WHEN ${eventName}:`,
        `        TRANSITION TO ${targetPhaseName}.`,
        ""
    ]);

    return newCode;
}
