from dataclasses import dataclass, field
from enum import Enum, auto

## This file has the role of only displaying errors and warnings in a consistent format, 
# with the ability to show the offending line of source code and a caret pointing to the 
# location of the issue. It also keeps track of the number of errors and warnings for 
# summary reporting at the end of compilation.


class Severity(Enum):
    """
    Defines the severity levels for compiler messages.
    """
    WARNING = auto()
    ERROR   = auto()


@dataclass
class CompilerMessage:
    """
    Represents a single compiler message, which can be either an error or a warning.
    """ 
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
        # get lines of the file for later display (1-indexed)
        self._lines:    list[str]             = source.splitlines()
        # store errors and warnings in a list for later sorting and display
        # TODO: this is accessed by compiler.py, maybe expose an iterator instead of the raw list?
        self._messages: list[CompilerMessage] = []

    # == Public reporting API =================================================

    # API for adding errors and warnings with all necessary information for later display
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

    # == Queries ==============================================================

    # check if any errors have been reported (useful for deciding whether to proceed with compilation)
    def has_errors(self) -> bool:
        return any(m.severity == Severity.ERROR for m in self._messages)

    # get counts of errors for summary reporting
    def error_count(self) -> int:
        return sum(1 for m in self._messages if m.severity == Severity.ERROR)

    # get counts of warnings for summary reporting
    def warning_count(self) -> int:
        return sum(1 for m in self._messages if m.severity == Severity.WARNING)

    # == Output ===============================================================

    def print_all(self):
        # Sort by line number so messages appear in source order
        sorted_messages = sorted(self._messages, key=lambda m: m.line)
        for msg in sorted_messages:
            self._print_message(msg)
        self._print_summary()

    def print_summary(self):
        self._print_summary()

    # == Internal =============================================================

    # add an error or warning with all necessary information for later display
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
        # append the message to the list with all details for later display
        self._messages.append(CompilerMessage(
            severity    = severity,
            line        = line,
            column      = column,
            length      = max(length, 1),
            message     = message,
            hint        = hint,
            source_line = source_line,
        ))

    # print individual messages, with line number, column, message text, 
    # hint, and the offending line of source code with a caret pointing to the issue
    def _print_message(self, msg: CompilerMessage):

        # == Header ===========================================================
        divider = "=" * 60
        label   = "ERROR" if msg.severity == Severity.ERROR else "WARNING"
        print(f"\n{divider}")
        print(f" {label}  line {msg.line}, column {msg.column}")

        # == Message and hint =================================================
        print(f" {msg.message}")
        if msg.hint:
            print(f" Hint: {msg.hint}")

        # == Source line with caret ============================================
        if msg.source_line:
            print()
            print(f"    {msg.source_line}")
            caret = " " * (4 + msg.column) + "^" * msg.length
            print(caret)

        print(divider)

    # print a summary of the compilation results, showing the total number 
    # of errors and warnings, and whether compilation was successful or failed 
    # based on the presence of errors.
    def _print_summary(self):
        e = self.error_count()
        w = self.warning_count()
        print()
        if e > 0:
            print(f"Compilation failed: {e} error(s), {w} warning(s).")
        else:
            print(f"Compilation successful: {e} error(s), {w} warning(s).")