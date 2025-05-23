"""Custom exception classes for grammar processing errors."""


class GrammarSyntaxError(Exception):
    """Base exception for syntax-related errors in grammar definitions."""

    def __init__(self, message: str):
        """Initialize error message."""
        super().__init__("SyntaxError: " + message)


class FalseSyntaxExpectation(GrammarSyntaxError):
    """Raised when unexpected symbol is encountered during parsing.

    Args:
        expected (str): Description of expected symbol.
        line (int): Line number where error occurred.
        got (str): Actual symbol found.
    """

    def __init__(self, expected: str, line: int, got: str):
        """Initialize error message."""
        super().__init__(
            f"expected {expected} in line {line}, found {got} instead")


class GrammarSemanticError(Exception):
    """Base exception for semantic rule violations in grammar."""

    def __init__(self, message: str):
        """Initialize error message."""
        super().__init__("SemanticError: " + message)


class SymbolIsAlreadyInSet(GrammarSemanticError):
    """Raised when symbol is redefined in terminal/non-terminal set.

    Args:
        symbol (str): Duplicate symbol.
        line (int): Line number of redefinition.
        set_name (str): Name of the set (terminals/non-terminals).
    """

    def __init__(self, symbol: str, line: int, set_name: str):
        """Initialize error message."""
        super().__init__(f"symbol {symbol} in line {line} is \
                    already in the set of {set_name}")


class LeftSideOfRuleHasOnlyTerminals(GrammarSemanticError):
    """Raised when rule's LHS contains only terminal symbols.

    Args:
        line (int): Line number of invalid rule.
    """

    def __init__(self, line: int):
        """Initialize error message."""
        super().__init__(f"left side of the rule in the line {line} \
                    consists only of terminals")


class LeftSideOfRuleHasUndefinedSymbols(GrammarSemanticError):
    """Raised when rule's LHS uses undefined symbols.

    Args:
        line (int): Line number of invalid rule.
    """

    def __init__(self, line: int):
        """Initialize error message."""
        super().__init__(f"left side of the rule in the line {line} \
                    has symbols, that weren't defined in T and N")


class RightSideOfRuleHasUndefinedSymbols(GrammarSemanticError):
    """Raised when rule's RHS uses undefined symbols.

    Args:
        line (int): Line number of invalid rule.
    """

    def __init__(self, line: int):
        """Initialize error message."""
        super().__init__(f"right side of the rule in the line {line} \
                    has symbols, that weren't defined in T and N")
