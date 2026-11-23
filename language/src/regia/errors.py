"""
Error reporting for the Regia compiler.

Collects, formats, and displays compiler messages (errors and warnings).
"""

from dataclasses import dataclass
from enum        import Enum, auto
from typing      import Dict, List, Callable, Optional

StyleFunc = Callable[..., str]

def _default_style(text: str, **kwargs) -> str:
    return text


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
        filename:    Name of the source file (empty for single-file).
    """

    severity:    Severity
    line:        int
    column:      int
    length:      int
    message:     str
    hint:        str = ""
    source_line: str = ""
    filename:    str = ""



def format_message(msg: CompilerMessage, style_func: Optional[StyleFunc] = None) -> str:
    """Format a single message with header, text, hint, and caret.

    Args:
        msg: The compiler message to format.
        style_func: Optional function to style text (e.g., click.style).

    Returns:
        A formatted multi-line string for this diagnostic.
    """
    style = style_func or _default_style
    divider = "=" * 60
    
    label = "ERROR" if msg.severity == Severity.ERROR else "WARNING"
    if msg.severity == Severity.ERROR:
        label = style(label, fg="red", bold=True)
    else:
        label = style(label, fg="yellow", bold=True)

    if msg.filename:
        colored_name = style(msg.filename, fg="blue")
        location = f"{colored_name}:{msg.line}, col {msg.column}"
    else:
        location = f"line {msg.line}, col {msg.column}"

    parts: List[str] = [
        f"\n{divider}",
        f" {label}  {location}",
        f" {msg.message}",
    ]
    if msg.hint:
        parts.append(f" Hint: {msg.hint}")
    if msg.source_line:
        parts.append("")
        parts.append(f"    {msg.source_line}")
        caret = style("^" * msg.length, fg="red", bold=True)
        parts.append(" " * (4 + msg.column) + caret)
    parts.append(divider)
    return "\n".join(parts)


# == Error reporter ============================================================

class ErrorReporter:
    """Central error and warning collector for the Regia compiler.

    Manages a registry of source texts keyed by filename, so it
    can display the offending line with a caret for diagnostics
    from any file. Counters are maintained incrementally for O(1)
    queries.
    """

    def __init__(self, source: str = "") -> None:
        """Initialise the reporter, optionally with a single source text.

        Args:
            source: The complete source code string for single-file
                    compilation. For multi-file, call register_source()
                    for each file instead.
        """
        self._source_registry: Dict[str, List[str]]  = {}
        self._messages:        List[CompilerMessage] = []
        self._error_count:     int                   = 0
        self._warning_count:   int                   = 0

        # Backwards compatibility: if a source string is provided,
        # register it under the empty filename key.
        if source:
            self.register_source("", source)

    # == Source registry =======================================================

    def register_source(self, filename: str, source: str) -> None:
        """Register the source text for a file.

        Args:
            filename: The name of the source file (used to look up
                      lines when formatting diagnostics).
            source:   The complete source code string for this file.
        """
        self._source_registry[filename] = source.splitlines()

    # == Public reporting API ==================================================

    def error(
        self,
        line:     int,
        column:   int,
        length:   int,
        message:  str,
        hint:     str = "",
        filename: str = "",
    ) -> None:
        """Record an error diagnostic.

        Args:
            line:     1-based line number of the issue.
            column:   0-based column offset within the line.
            length:   Length of the offending span (for caret width).
            message:  Human-readable description of the error.
            hint:     Optional suggestion for how to fix it.
            filename: The source file this error originates from.
        """
        self._add(Severity.ERROR, line, column, length, message, hint,
                  filename)

    def warning(
        self,
        line:     int,
        column:   int,
        length:   int,
        message:  str,
        hint:     str = "",
        filename: str = "",
    ) -> None:
        """Record a warning diagnostic.

        Args:
            line:     1-based line number of the issue.
            column:   0-based column offset within the line.
            length:   Length of the offending span (for caret width).
            message:  Human-readable description of the warning.
            hint:     Optional suggestion for how to address it.
            filename: The source file this warning originates from.
        """
        self._add(Severity.WARNING, line, column, length, message, hint,
                  filename)

    # == Queries ===============================================================

    def has_errors(self) -> bool:
        """Check whether any errors have been recorded.

        Returns:
            True if at least one ERROR-severity message exists.
        """
        return self._error_count > 0

    @property
    def messages(self) -> List[CompilerMessage]:
        """Return a copy of all collected messages."""
        return list(self._messages)

    @property
    def error_count(self) -> int:
        """The total number of recorded errors."""
        return self._error_count

    @property
    def warning_count(self) -> int:
        """The total number of recorded warnings."""
        return self._warning_count

    # == Formatted output ======================================================

    def format_all(self, style_func: Optional[StyleFunc] = None, quiet: bool = False) -> str:
        """Return all messages as a formatted string, sorted by filename and line.

        Returns:
            A multi-line string containing all diagnostics with carets
            and a final summary line.
        """
        parts: List[str] = []
        for msg in sorted(self._messages, key=lambda m: (m.filename, m.line)):
            if quiet and msg.severity != Severity.ERROR:
                continue
            parts.append(format_message(msg, style_func))
        if not quiet or self._error_count > 0:
            parts.append(self._format_summary())
        return "\n".join(parts)

    # == Internal ==============================================================

    def _get_source_line(self, filename: str, line: int) -> str:
        """Look up a source line from the registry.

        Args:
            filename: The source file name.
            line:     The 1-based line number.

        Returns:
            The source line text, or empty string if not found.
        """
        lines = self._source_registry.get(filename, [])
        if 1 <= line <= len(lines):
            return lines[line - 1]
        return ""

    def _add(
        self,
        severity: Severity,
        line:     int,
        column:   int,
        length:   int,
        message:  str,
        hint:     str,
        filename: str = "",
    ) -> None:
        """Create a CompilerMessage and append it to the internal list.

        Args:
            severity: ERROR or WARNING.
            line:     1-based line number.
            column:   0-based column offset.
            length:   Offending span length.
            message:  Description text.
            hint:     Optional fix suggestion.
            filename: The source file this message originates from.
        """
        source_line = self._get_source_line(filename, line)

        self._messages.append(CompilerMessage(
            severity    = severity,
            line        = line,
            column      = column,
            length      = max(length, 1),
            message     = message,
            hint        = hint,
            source_line = source_line,
            filename    = filename,
        ))

        if severity == Severity.ERROR:
            self._error_count += 1
        else:
            self._warning_count += 1

    def _format_summary(self) -> str:
        """Format the final compilation summary line.

        Returns:
            A string like 'Compilation failed: 2 error(s), 1 warning(s).'
        """
        e, w = self._error_count, self._warning_count
        if e > 0:
            return f"\nCompilation failed: {e} error(s), {w} warning(s)."
        return f"\nCompilation successful: {e} error(s), {w} warning(s)."
