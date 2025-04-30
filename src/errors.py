class SyntaxError(Exception):
    def __init__(self, message):
        super().__init__("SyntaxError: " + message)

class FalseSyntaxExpectation(SyntaxError):
    def __init__(self, expected, line, got):
        super().__init__(f"expected {expected} in line {line}, found {got} instead")

class SemanticError(Exception):
    def __init__(self, message):
        super().__init__(f"SemanticError: " + message)

class SymbolIsAlreadyInSet(SemanticError):
    def __init__(self, symbol, line, set_name):
        super().__init__(f"symbol {symbol} in line {line} is already in the set of {set_name}")

class RepeatedLeftSideOfRule(SemanticError):
    def __init__(self, early_line, later_line):
        super().__init__(f"left side of the rule in the line {early_line} was repeated in line {later_line}")

class LeftSideOfRuleHasOnlyTerminals(SemanticError):
    def __init__(self, line):
        super().__init__(f"left side of the rule in the line {line} consists only of terminals")

class LeftSideOfRuleHasUndefinedSymbols(SemanticError):
    def __init__(self, line):
        super().__init__(f"left side of the rule in the line {line} has symbols, that weren't defined in T and N")

class RightSideOfRuleHasUndefinedSymbols(SemanticError):
    def __init__(self, line):
        super().__init__(f"right side of the rule in the line {line} has symbols, that weren't defined in T and N")
