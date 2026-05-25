from antlr4.error.ErrorListener import ErrorListener
from src.errors import ErrorReporter


class RegiaScriptErrorListener(ErrorListener):
    """
    Replaces ANTLR's default error listener.
    Intercepts raw syntax errors and forwards them to ErrorReporter
    with human-readable messages.
    """

    def __init__(self, reporter: ErrorReporter):
        super().__init__()
        self.reporter = reporter

    def syntaxError(
        self, recognizer, offendingSymbol, line, column, msg, e
    ):
        text   = offendingSymbol.text if offendingSymbol else "?"
        length = len(text) if text != "<EOF>" else 1

        message, hint = self._humanise(msg, text)
        self.reporter.error(line, column, length, message, hint)

    # ── Message humaniser ────────────────────────────────────────────────────

    def _humanise(self, antlr_msg: str, text: str) -> tuple[str, str]:
        """
        Converts ANTLR's raw error messages into plain English.
        Returns (message, hint).
        """

        if "mismatched input" in antlr_msg and "expecting" in antlr_msg:
            raw_expected = antlr_msg.split("expecting")[-1].strip()
            expected     = self._friendly_token(raw_expected)
            return (
                f"Unexpected '{text}' found here.",
                f"Expected {expected}.",
            )

        if "missing" in antlr_msg and "at" in antlr_msg:
            raw_expected = antlr_msg.split("missing")[-1].split("at")[0].strip()
            expected     = self._friendly_token(raw_expected)
            return (
                f"Something is missing before '{text}'.",
                f"Expected {expected} here.",
            )

        if "extraneous input" in antlr_msg and "expecting" in antlr_msg:
            raw_expected = antlr_msg.split("expecting")[-1].strip()
            expected     = self._friendly_token(raw_expected)
            return (
                f"Extra text '{text}' is not valid here.",
                f"Remove it, or check that {expected} follows.",
            )

        if "no viable alternative" in antlr_msg:
            return (
                f"'{text}' is not valid in this position.",
                "Check the surrounding syntax for a missing keyword or punctuation.",
            )

        if "rule" in antlr_msg and "missing" in antlr_msg:
            return (
                f"Incomplete statement ending at '{text}'.",
                "Check that this line is complete.",
            )

        # Fallback — clean up ANTLR's raw message minimally
        return (antlr_msg, "")

    def _friendly_token(self, raw: str) -> str:
        """
        Translates ANTLR token names into plain English descriptions.
        """
        mapping = {
            "ID"          : "a name (e.g. 'run', 'enemy_spotted')",
            "NUMBER"      : "a whole number (e.g. '1', '2')",
            "PERIOD"      : "a period '.'",
            "COLON"       : "a colon ':'",
            "COMMA"       : "a comma ','",
            "DURING"      : "the keyword 'DURING'",
            "WHEN"        : "the keyword 'WHEN'",
            "IF"          : "the keyword 'IF'",
            "DO"          : "the keyword 'DO'",
            "PRIORITY"    : "the keyword 'PRIORITY'",
            "ALWAYS"      : "the keyword 'ALWAYS' or a story name",
            "ENVIRONMENT" : "an origin tag: ENVIRONMENT, DIRECTOR, or MYSELF",
            "DIRECTOR"    : "an origin tag: ENVIRONMENT, DIRECTOR, or MYSELF",
            "MYSELF"      : "an origin tag: ENVIRONMENT, DIRECTOR, or MYSELF",
            "EOF"         : "the end of file",
        }
        for key, val in mapping.items():
            if key in raw:
                return val
        return raw