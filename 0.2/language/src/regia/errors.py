"""
Error reporting for the Regia compiler.

Collects, formats, and displays compiler messages (errors and warnings).
Ported from v0.1 with improvements:
  - Public ``messages`` property (no more accessing private fields)
  - Counters maintained incrementally (no full-scan on every check)
  - Source-line caret display is centralised here only
"""

from dataclasses import dataclass
from enum        import Enum, auto
from typing      import List


# == Severity ==================================================================

class Severity(Enum):
    """Severity levels for compiler diagnostics."""

    WARNING = auto()
    ERROR   = auto()


# == Compiler message ==========================================================

@dataclass
class CompilerMessage:
    """A single compiler diagnostic (error or warning).

    Attributes:
        severity:    Whether this is an ERROR or WARNING.
        line:        1-based line number in the source file.
        column:      0-based column offset within the line.
        length:      Length of the offending token (for caret display).
        message:     Human-readable description of the issue.
        hint:        Optional suggestion for how to fix the issue.
        source_line: The raw source line text (for caret display).
    """

    severity:    Severity
    line:        int
    column:      int
    length:      int
    message:     str
    hint:        str = ""
    source_line: str = ""


# == Error reporter ============================================================

class ErrorReporter:
    """Central error and warning collector for the Regia compiler.

    Constructed with the full source text so it can display the
    offending line with a caret for every message. Counters are
    maintained incrementally for O(1) queries.
    """

    def __init__(self, source: str) -> None:
        """Initialise the reporter with the full source text.

        Args:
            source: The complete source code string, used to extract
                    individual lines for caret display.
        """
        self._lines:         List[str]             = source.splitlines()
        self._messages:      List[CompilerMessage] = []
        self._error_count:   int                   = 0
        self._warning_count: int                   = 0

    # == Public reporting API ==================================================

    def error(
        self,
        line:    int,
        column:  int,
        length:  int,
        message: str,
        hint:    str = "",
    ) -> None:
        """Record an error diagnostic.

        Args:
            line:    1-based line number of the issue.
            column:  0-based column offset within the line.
            length:  Length of the offending span (for caret width).
            message: Human-readable description of the error.
            hint:    Optional suggestion for how to fix it.
        """
        self._add(Severity.ERROR, line, column, length, message, hint)

    def warning(
        self,
        line:    int,
        column:  int,
        length:  int,
        message: str,
        hint:    str = "",
    ) -> None:
        """Record a warning diagnostic.

        Args:
            line:    1-based line number of the issue.
            column:  0-based column offset within the line.
            length:  Length of the offending span (for caret width).
            message: Human-readable description of the warning.
            hint:    Optional suggestion for how to address it.
        """
        self._add(Severity.WARNING, line, column, length, message, hint)

    # == Queries ===============================================================

    @property
    def messages(self) -> List[CompilerMessage]:
        """Return a copy of all collected messages."""
        return list(self._messages)

    def has_errors(self) -> bool:
        """Check whether any errors have been recorded.

        Returns:
            True if at least one ERROR-severity message exists.
        """
        return self._error_count > 0

    @property
    def error_count(self) -> int:
        """The total number of recorded errors."""
        return self._error_count

    @property
    def warning_count(self) -> int:
        """The total number of recorded warnings."""
        return self._warning_count

    # == Formatted output ======================================================

    def format_all(self) -> str:
        """Return all messages as a formatted string, sorted by line.

        Returns:
            A multi-line string containing all diagnostics with carets
            and a final summary line.
        """
        parts: List[str] = []
        for msg in sorted(self._messages, key=lambda m: m.line):
            parts.append(self._format_message(msg))
        parts.append(self._format_summary())
        return "\n".join(parts)

    # == Internal ==============================================================

    def _add(
        self,
        severity: Severity,
        line:     int,
        column:   int,
        length:   int,
        message:  str,
        hint:     str,
    ) -> None:
        """Create a CompilerMessage and append it to the internal list.

        Args:
            severity: ERROR or WARNING.
            line:     1-based line number.
            column:   0-based column offset.
            length:   Offending span length.
            message:  Description text.
            hint:     Optional fix suggestion.
        """
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

        if severity == Severity.ERROR:
            self._error_count += 1
        else:
            self._warning_count += 1

    def _format_message(self, msg: CompilerMessage) -> str:
        """Format a single message with header, text, hint, and caret.

        Args:
            msg: The compiler message to format.

        Returns:
            A formatted multi-line string for this diagnostic.
        """
        divider = "=" * 60
        label   = "ERROR" if msg.severity == Severity.ERROR else "WARNING"
        parts: List[str] = [
            f"\n{divider}",
            f" {label}  line {msg.line}, column {msg.column}",
            f" {msg.message}",
        ]
        if msg.hint:
            parts.append(f" Hint: {msg.hint}")
        if msg.source_line:
            parts.append("")
            parts.append(f"    {msg.source_line}")
            parts.append(" " * (4 + msg.column) + "^" * msg.length)
        parts.append(divider)
        return "\n".join(parts)

    def _format_summary(self) -> str:
        """Format the final compilation summary line.

        Returns:
            A string like 'Compilation failed: 2 error(s), 1 warning(s).'
        """
        e, w = self._error_count, self._warning_count
        if e > 0:
            return f"\nCompilation failed: {e} error(s), {w} warning(s)."
        return f"\nCompilation successful: {e} error(s), {w} warning(s)."
