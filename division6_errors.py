# ============================================================
# DATACORE LANGUAGE - DIVISION 6: ERROR HANDLER
# Assigned to: Person 6
# ============================================================
# PURPOSE:
#   Every language needs clear, friendly error messages.
#   This division defines ALL error types DataCore can raise
#   and a central ErrorHandler that formats them cleanly.
#
#   Error phases in DataCore:
#     1. LEXER errors    — unknown characters, bad strings
#     2. PARSER errors   — wrong grammar structure
#     3. TYPE errors     — wrong types before execution
#     4. RUNTIME errors  — division by zero, missing table, etc.
#
#   This module also defines a DataCoreError exception class
#   hierarchy and the ErrorHandler class which:
#     - Formats error messages with line numbers
#     - Highlights the offending line in source code
#     - Provides suggestions where possible
#     - Keeps an error log for the REPL to display
#
# RESPONSIBILITIES OF PERSON 6:
#   - Define DataCoreError base class
#   - Define specific error subclasses (LexError, ParseError, etc.)
#   - Implement ErrorHandler.report() for pretty formatting
#   - Implement error recovery hints (suggestions)
#   - Integrate with all other divisions
# ============================================================

import traceback


# ============================================================
# ERROR CLASS HIERARCHY
# ============================================================

class DataCoreError(Exception):
    """
    Base class for all DataCore language errors.
    All our custom errors inherit from this so they can be
    caught with a single except DataCoreError clause.
    
    Fields:
      message  -- human-readable description
      line     -- source code line number (or None)
      source   -- the full source string (for context display)
    """
    ERROR_TYPE = "DataCore Error"

    def __init__(self, message: str, line: int = None, source: str = None):
        self.message = message
        self.line    = line
        self.source  = source
        super().__init__(message)

    def format(self) -> str:
        """Return a formatted, multi-line error message."""
        lines = [
            f"\n{'='*60}",
            f"  ❌ {self.ERROR_TYPE}",
            f"{'='*60}",
        ]

        if self.line is not None:
            lines.append(f"  📍 Line {self.line}")

        lines.append(f"  💬 {self.message}")

        # Show the offending source line if available
        if self.source and self.line:
            src_lines = self.source.splitlines()
            idx = self.line - 1
            if 0 <= idx < len(src_lines):
                lines.append(f"\n  Source:")
                # Show one line before for context (if available)
                if idx > 0:
                    lines.append(f"  {self.line - 1:4} | {src_lines[idx-1]}")
                lines.append(f"  {self.line:4} |▶ {src_lines[idx]}  ← error here")
                if idx + 1 < len(src_lines):
                    lines.append(f"  {self.line + 1:4} | {src_lines[idx+1]}")

        hint = self._hint()
        if hint:
            lines.append(f"\n  💡 Hint: {hint}")

        lines.append(f"{'='*60}\n")
        return "\n".join(lines)

    def _hint(self) -> str:
        """
        Subclasses can override this to provide a helpful suggestion.
        """
        return ""

    def __str__(self):
        return self.format()


# ============================================================
# SPECIFIC ERROR TYPES
# ============================================================

class LexError(DataCoreError):
    """
    Raised by the Lexer when it encounters an unknown character
    or a malformed token (e.g., unterminated string).
    
    Example:
      ADD users @ name = 'Alice';
              ^--- '@' is not a valid DataCore character
    """
    ERROR_TYPE = "Lexer Error (Tokenization)"

    def _hint(self) -> str:
        msg = self.message.lower()
        if "unknown character" in msg:
            return "Check for typos. DataCore supports: letters, digits, _, quotes, common operators."
        if "unterminated string" in msg:
            return "Make sure every opening single quote ' has a matching closing single quote '."
        return ""


class ParseError(DataCoreError):
    """
    Raised by the Parser when the token sequence doesn't match
    the expected grammar.
    
    Example:
      SELECT FROM users;   ← missing column list between SELECT and FROM
    """
    ERROR_TYPE = "Parser Error (Syntax)"

    def _hint(self) -> str:
        msg = self.message.lower()
        if "expected from" in msg:
            return "SELECT syntax: SELECT col1, col2 FROM tableName WHERE condition;"
        if "expected identifier" in msg:
            return "An identifier (table name, column name, variable name) was expected here."
        if "expected =" in msg:
            return "Assignment requires '=': e.g., INT x = 5;"
        if "expected )" in msg or "expected (" in msg:
            return "Check that all parentheses are balanced and properly placed."
        return "Review DataCore syntax. Each statement must end with ';'."


class TypeError(DataCoreError):
    """
    Raised by the Type Checker when types don't match.
    This is caught BEFORE execution — static checking.
    
    Example:
      INT age = 'twenty';   ← cannot assign STRING to INT
    """
    ERROR_TYPE = "Type Error (Static Check)"

    def _hint(self) -> str:
        msg = self.message.lower()
        if "type mismatch" in msg:
            return (
                "DataCore is strongly typed. Make sure the value's type matches "
                "the declared type. INT = integer, FLOAT = decimal, "
                "STRING = 'text in quotes', BOOL = TRUE/FALSE."
            )
        if "undeclared variable" in msg:
            return "Declare variables before use: INT x = 5;  or  FLOAT score = 0.0;"
        if "already declared" in msg:
            return "Variables can only be declared once per scope. Use assignment to change a value."
        if "undefined function" in msg:
            return "Declare the function with FUNC before calling it."
        if "does not exist" in msg and "column" in msg:
            return "Check the table schema — the column may be misspelled or not defined."
        return ""


class RuntimeError(DataCoreError):
    """
    Raised by the Interpreter when something goes wrong at
    execution time that the type checker couldn't predict.
    
    Example:
      Division by zero, table not found, stack overflow, etc.
    """
    ERROR_TYPE = "Runtime Error (Execution)"

    def _hint(self) -> str:
        msg = self.message.lower()
        if "division by zero" in msg:
            return "Ensure the divisor is not zero before dividing. Use an IF check."
        if "undefined variable" in msg:
            return "Declare the variable before using it: INT x = 0;"
        if "does not exist" in msg and "table" in msg:
            return "Use 'ADD TABLE tableName (col TYPE, ...);' to create the table first."
        if "stack" in msg:
            return "Check for infinite recursion — a function calling itself without a base case."
        if "already exists" in msg and "table" in msg:
            return "Table was already created. Use DROP tableName; first if you want to recreate it."
        return ""


class StackOverflowError(RuntimeError):
    """
    Raised when the call stack exceeds a safe depth limit.
    Prevents infinite recursion from crashing the interpreter.
    """
    ERROR_TYPE = "Stack Overflow Error"

    def _hint(self) -> str:
        return (
            "A function may be calling itself infinitely (infinite recursion). "
            "Add a base case that returns without making another call."
        )


class UndefinedVariableError(RuntimeError):
    """Specific error for referencing a variable not in scope."""
    ERROR_TYPE = "Undefined Variable Error"


class TableNotFoundError(RuntimeError):
    """Specific error when a table doesn't exist."""
    ERROR_TYPE = "Table Not Found Error"


class ColumnNotFoundError(RuntimeError):
    """Specific error when a column doesn't exist in a table."""
    ERROR_TYPE = "Column Not Found Error"


# ============================================================
# ERROR HANDLER CLASS
# Central error reporting, logging, and recovery
# ============================================================

class ErrorHandler:
    """
    Central error reporting hub for the DataCore interpreter.
    
    Usage:
      handler = ErrorHandler(source_code)
      try:
          ...
      except SyntaxError as e:
          handler.report_builtin(e, phase="lexer")
      except DataCoreError as e:
          handler.report(e)
    """

    # Maximum call stack depth before StackOverflow
    MAX_STACK_DEPTH = 100

    def __init__(self, source: str = ""):
        self.source    = source         # Original source code
        self.error_log = []             # All errors collected
        self.has_error = False          # Any error occurred?

    def set_source(self, source: str):
        """Update the source code (useful for REPL multi-line input)."""
        self.source = source

    def report(self, error: DataCoreError):
        """
        Record and display a DataCoreError.
        Attaches source for context display if not already set.
        """
        if not error.source:
            error.source = self.source
        self.has_error = True
        self.error_log.append(error)
        print(error.format())

    def report_builtin(self, exc: Exception, phase: str = "unknown", line: int = None):
        """
        Convert a built-in Python exception (SyntaxError, TypeError, etc.)
        into the appropriate DataCoreError and report it.
        
        This bridges our division's error system with Python's native exceptions
        which may be raised in early development.
        """
        msg = str(exc)

        # Extract line from SyntaxError if available
        if isinstance(exc, SyntaxError) and exc.lineno:
            line = exc.lineno

        if phase == "lexer":
            error = LexError(msg, line=line, source=self.source)
        elif phase == "parser":
            error = ParseError(msg, line=line, source=self.source)
        elif phase == "typecheck":
            # Note: we shadow Python's TypeError above intentionally
            error = TypeError(msg, line=line, source=self.source)
        elif phase == "runtime":
            error = RuntimeError(msg, line=line, source=self.source)
        else:
            error = DataCoreError(msg, line=line, source=self.source)

        self.report(error)

    def check_stack_depth(self, depth: int):
        """
        Call this before pushing a new call frame.
        Raises StackOverflowError if depth exceeds limit.
        """
        if depth >= self.MAX_STACK_DEPTH:
            raise StackOverflowError(
                f"Call stack depth exceeded {self.MAX_STACK_DEPTH}. "
                f"Possible infinite recursion.",
                source=self.source
            )

    def summarize(self):
        """Print a summary of all errors encountered."""
        count = len(self.error_log)
        if count == 0:
            print("✅ No errors found.")
        else:
            print(f"\n{'='*60}")
            print(f"  ⚠️  {count} error(s) encountered:")
            for i, err in enumerate(self.error_log, 1):
                line_info = f"line {err.line}" if err.line else "unknown line"
                print(f"  {i}. [{err.ERROR_TYPE}] at {line_info}: {err.message[:60]}...")
            print(f"{'='*60}\n")

    def clear(self):
        """Reset error state (useful for REPL between commands)."""
        self.error_log = []
        self.has_error = False


# ============================================================
# QUICK TEST
# ============================================================
if __name__ == "__main__":
    handler = ErrorHandler(source="ADD INTO users (age = 'hello');")

    # Simulate a type error
    err = TypeError(
        "Type mismatch in ADD INTO users.age: expected INT, got STRING.",
        line=1,
        source="ADD INTO users (age = 'hello');"
    )
    handler.report(err)

    # Simulate a parse error
    err2 = ParseError(
        "Expected FROM, got IDENTIFIER ('users')",
        line=3,
        source="SELECT users;\nINT x = 5;\nSELECT users;"
    )
    handler.report(err2)

    handler.summarize()
