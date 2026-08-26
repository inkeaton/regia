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

/**
 * Scans downwards from a start line to find the end of a Regia block.
 * Uses Regia's major keywords to detect the start of the next block.
 * Ignores purely blank lines and comments.
 * Returns the 1-indexed line number where new code should be injected (right after the block).
 */
function findBlockEnd(code: string, startLine: number): number {
    const lines = code.split("\n");
    let index = startLine; // startLine is 1-indexed, so index points to the line *after* it
    
    const boundaryRegex = /^\s*(DURING|PHASE|ROLE|PLOT|PLAYBOOK|EVENT|ACTION|FACT)\b/;
    
    while (index < lines.length) {
        const line = lines[index];
        const trimmed = line.trim();
        
        if (trimmed === "" || trimmed.startsWith("#") || trimmed.startsWith("//")) {
            index++;
            continue;
        }
        
        if (boundaryRegex.test(line)) {
            break;
        }
        
        index++;
    }
    
    let endIndex = index - 1;
    // Backtrack past trailing blank lines and comments
    // But don't backtrack past the actual start line!
    while (endIndex >= startLine) {
        const trimmed = lines[endIndex].trim();
        if (trimmed !== "" && !trimmed.startsWith("#") && !trimmed.startsWith("//")) {
            break;
        }
        endIndex--;
    }
    
    return endIndex + 2; // +1 for 1-indexing, +1 to insert *after* the line
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

    // 2. Insert DuringBlock
    let duringInsertLine = newCode.split("\n").length + 1; // Fallback to EOF
    
    if (plot.during_blocks.length > 0) {
        const lastDuring = plot.during_blocks[plot.during_blocks.length - 1];
        // Find block end in original code, then shift +1 because we inserted a PhaseDecl above it
        const originalEndLine = findBlockEnd(code, lastDuring.loc.line);
        duringInsertLine = originalEndLine + 1;
    } else {
        // No during blocks yet, insert right after the phase we just added
        duringInsertLine = phaseInsertLine + 1;
    }

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

    // Find the end of this DuringBlock in the ORIGINAL code
    const originalEndLine = findBlockEnd(code, sourceBlock.loc.line);
    
    // The actual insert line in newCode is shifted by however many lines we prepended
    const endOfBlockLine = originalEndLine + linesShifted;

    newCode = insertLines(newCode, endOfBlockLine, [
        `    WHEN ${eventName}:`,
        `        TRANSITION TO ${targetPhaseName}.`,
        ""
    ]);

    return newCode;
}
