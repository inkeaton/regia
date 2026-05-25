from dataclasses import dataclass, field
from enum import Enum, auto


class Severity(Enum):
    WARNING = auto()
    ERROR   = auto()


@dataclass
class CompilerMessage:
    severity: Severity
    line:     int
    column:   int
    length:   int
    message:  str
    hint:     str
    source_line: str = ""   # the raw source line for caret display


class ErrorReporter:
    """
    Central error and warning collector for the RegiaScript compiler.
    Receives the full source text at construction so it can display
    the offending line with a caret for every message.
    """

    def __init__(self, source: str):
        self._lines:    list[str]            = source.splitlines()
        self._messages: list[CompilerMessage] = []

    # ── Public reporting API ─────────────────────────────────────────────────

    def error(
        self,
        line:    int,
        column:  int,
        length:  int,
        message: str,
        hint:    str = ""
    ):
        self._add(Severity.ERROR, line, column, length, message, hint)

    def warning(
        self,
        line:    int,
        column:  int,
        length:  int,
        message: str,
        hint:    str = ""
    ):
        self._add(Severity.WARNING, line, column, length, message, hint)

    # ── Queries ──────────────────────────────────────────────────────────────

    def has_errors(self) -> bool:
        return any(m.severity == Severity.ERROR for m in self._messages)

    def error_count(self) -> int:
        return sum(1 for m in self._messages if m.severity == Severity.ERROR)

    def warning_count(self) -> int:
        return sum(1 for m in self._messages if m.severity == Severity.WARNING)

    # ── Output ───────────────────────────────────────────────────────────────

    def print_all(self):
        # Sort by line number so messages appear in source order
        sorted_messages = sorted(self._messages, key=lambda m: m.line)
        for msg in sorted_messages:
            self._print_message(msg)
        self._print_summary()

    def print_summary(self):
        self._print_summary()

    # ── Internal ─────────────────────────────────────────────────────────────

    def _add(
        self,
        severity: Severity,
        line:     int,
        column:   int,
        length:   int,
        message:  str,
        hint:     str
    ):
        # Retrieve the raw source line for display (1-indexed)
        source_line = ""
        if 1 <= line <= len(self._lines):
            source_line = self._lines[line - 1]

        self._messages.append(CompilerMessage(
            severity    = severity,
            line        = line,
            column      = column,
            length      = max(length, 1),
            message     = message,
            hint        = hint,
            source_line = source_line,
        ))

    def _print_message(self, msg: CompilerMessage):
        # ── Header ───────────────────────────────────────────────────────────
        divider = "─" * 60
        label   = "ERROR" if msg.severity == Severity.ERROR else "WARNING"
        print(f"\n{divider}")
        print(f" {label}  line {msg.line}, column {msg.column}")

        # ── Message and hint ─────────────────────────────────────────────────
        print(f" {msg.message}")
        if msg.hint:
            print(f" Hint: {msg.hint}")

        # ── Source line with caret ────────────────────────────────────────────
        if msg.source_line:
            print()
            print(f"    {msg.source_line}")
            caret = " " * (4 + msg.column) + "^" * msg.length
            print(caret)

        print(divider)

    def _print_summary(self):
        e = self.error_count()
        w = self.warning_count()
        print()
        if e > 0:
            print(f"Compilation failed: {e} error(s), {w} warning(s).")
        else:
            print(f"Compilation successful: {e} error(s), {w} warning(s).")