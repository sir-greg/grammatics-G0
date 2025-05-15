"""Grammar analyzer module for parsing and validation."""

import constants
import errors
from utility import Grammar, PointedContents


def verbose_output(fun):
    """Add verbose logging to function execution.

    Args:
        fun (function): The function to wrap with logging.

    Returns:
        function: Wrapped function with verbose output capabilities.
    """

    def wrapper(self, *args, **kwargs):
        if self.is_verbose:
            print("------------------")
            print("Entered: ", fun.__name__, " in line ",
                  self.pointed_contents.get_line())
        result = fun(self, *args, **kwargs)
        if self.is_verbose:
            print(
                "Finished: ",
                fun.__name__,
                " in line ",
                self.pointed_contents.get_line(),
                " with result:",
                result,
            )
            print("------------------")
        return result

    return wrapper


class Analyzer:
    """Analyzes grammar definitions and builds a grammar structure.

    Attributes:
        pointed_contents (PointedContents): Input content navigator.
        terminals (set): Collection of terminal symbols.
        nonterminals (set): Collection of non-terminal symbols.
        rules_dict (dict): Grammar production rules (LHS → RHS).
        rules_lines_dict (dict): Line numbers for each rule definition.
        is_verbose (bool): Enables detailed debugging output.
    """

    def __init__(self, pointed_contents: PointedContents,
                 is_verbose: bool) -> None:
        """Initialize analyzer with input content and verbosity settings.

        Args:
            pointed_contents (PointedContents): Wrapper for input content.
            is_verbose (bool): Enables step-by-step analysis logging.
        """
        self.pointed_contents = pointed_contents
        self.terminals = set([constants.DELIMETER])
        self.nonterminals = set([
            constants.STARTING_SYMBOL, constants.EMPTY_STRING,
            constants.FINAL_SYMBOL
        ])
        self.rules_dict: dict[str, str] = {}
        self.rules_lines_dict: dict[str, int] = {}
        self.is_verbose = is_verbose

    @verbose_output
    def non_empty_string(self) -> str:
        """Parse a non-empty sequence of valid grammar symbols.

        Returns:
            str: string of valid symbols.

        Raises:
            FalseSyntaxExpectation: If no valid symbol is found initially.
        """
        result = self.grammar_symbol()
        if result == "":
            raise errors.FalseSyntaxExpectation(
                "a grammar symbol",
                self.pointed_contents.get_line(),
                self.pointed_contents.get_cur(),
            )
        while True:
            symbol = self.grammar_symbol()
            if symbol == "":
                break
            result += symbol
        result = result.replace(constants.EMPTY_STRING, "")
        return result

    @verbose_output
    def empty_string(self) -> str:
        """Check for empty string representation (constants.EMPTY_STRING).

        Returns:
            str: constants.EMPTY_STRING if found, otherwise "".
        """
        if (self.pointed_contents.get_cur() == "\\"
                and self.pointed_contents.get_after_cur() == "E"):
            self.pointed_contents.move_ptr()
            self.pointed_contents.move_ptr()
            return constants.EMPTY_STRING
        return ""

    @verbose_output
    def string(self) -> str:
        """Parse either an empty or non-empty grammar string.

        Returns:
            str: Parsed string (may be constants.EMPTY_STRING).
        """
        if self.empty_string() == "":
            return self.non_empty_string()
        return constants.EMPTY_STRING

    @verbose_output
    def transforms_to(self) -> None:
        """Validate the '>>' operator in rule definitions."""
        self.pointed_contents.move_if_looks_at(">")
        self.pointed_contents.move_if_looks_at(">")

    def check_for_word_in_front(self, string: str) -> bool:
        """Check if the current position matches a specific string.

        Args:
            string (str): Expected sequence of characters.

        Returns:
            bool: True if the entire string matches, False otherwise.
        """
        for c in string:
            if self.pointed_contents.get_cur() != c:
                return False
            self.pointed_contents.move_ptr()
        return True

    @verbose_output
    def rule(self) -> None:
        """Parse and validate a grammar rule.

        Raises:
            LeftSideOfRuleHasOnlyTerminals: If LHS contains only terminals.
            LeftSideOfRuleHasUndefinedSymbols: If LHS uses undefined symbols.
            RightSideOfRuleHasUndefinedSymbols: If RHS uses undefined symbols.
        """
        lhs = self.non_empty_string()

        if not self.is_allowed_string(lhs):
            raise errors.LeftSideOfRuleHasUndefinedSymbols(
                self.pointed_contents.get_line())

        if all(c not in lhs for c in self.nonterminals):
            raise errors.LeftSideOfRuleHasOnlyTerminals(
                self.pointed_contents.get_line())

        self.rules_lines_dict[lhs] = self.pointed_contents.get_line()

        self.transforms_to()

        rhs = self.string()
        if not self.is_allowed_string(rhs):
            raise errors.RightSideOfRuleHasUndefinedSymbols(
                self.pointed_contents.get_line())
        self.rules_dict[lhs] = rhs

    @verbose_output
    def set_of_rules(self) -> None:
        """Parse multiple rules separated by semicolons."""
        while True:
            self.rule()
            if self.pointed_contents.move_no_raise_if_looks_at("."):
                break

            self.pointed_contents.move_if_looks_at(";")

    @verbose_output
    def is_allowed_string(self, string: str) -> bool:
        """Validate if all symbols in a string are defined.

        Args:
            string (str): The string to validate.

        Returns:
            bool: True if all symbols are valid, False otherwise.
        """

        def check(string: str, pos: int) -> bool:
            if pos == len(string):
                return True
            if string[pos] == "\\":
                is_special_symbol = pos + 1 != len(string) and string[pos +
                                                                      1] in [
                                                                          "E",
                                                                          "S",
                                                                          "!",
                                                                          "\\",
                                                                      ]
                return check(string, pos + 2) if is_special_symbol else False
            if pos + 1 != len(string) and string[pos + 1] == "'":
                candidate = string[pos:(pos + 2)]
                is_grammar_symbol = (candidate in self.terminals
                                     or candidate in self.nonterminals)
                return check(string, pos + 2) if is_grammar_symbol else False
            if pos + 1 != len(string) and string[pos + 1] == "_":
                upto = string[pos:].find("}")
                if upto == -1:
                    raise errors.FalseSyntaxExpectation(
                        "}",
                        self.pointed_contents.get_line(),
                        self.pointed_contents.get_cur(),
                    )
                upto += pos + 1
                if upto != len(string) and string[upto] == "'":
                    upto += 1
                candidate = string[pos:upto]
                is_grammar_symbol = (candidate in self.terminals
                                     or candidate in self.nonterminals)
                return check(string, upto) if is_grammar_symbol else False
            is_grammar_symbol = (string[pos] in self.terminals
                                 or string[pos] in self.nonterminals)
            return check(string, pos + 1) if is_grammar_symbol else False

        return check(string, 0)

    @verbose_output
    def regular_letter(self) -> str:
        """Read a regular terminal symbol from input.

        Returns:
            str: The parsed symbol or "" if invalid.
        """
        if self.pointed_contents.get_cur() not in constants.REGULAR_ALPHABET:
            return ""
        result = self.pointed_contents.get_cur()
        self.pointed_contents.move_ptr()
        return result

    @verbose_output
    def special_letter(self) -> str:
        r"""Read an escaped special symbol (e.g., \S).

        Returns:
            str: The parsed symbol or "" if invalid.

        Raises:
            FalseSyntaxExpectation: For invalid escape sequences.
        """
        if not self.pointed_contents.move_no_raise_if_looks_at("\\"):
            return ""
        result = ("\\" + self.pointed_contents.get_cur()
                  if self.pointed_contents.get_cur() in ["E", "S", "!", "\\"]
                  else "")
        if result == "":
            raise errors.FalseSyntaxExpectation(
                "E, S, !, or \\",
                self.pointed_contents.get_line(),
                self.pointed_contents.get_cur(),
            )
        self.pointed_contents.move_ptr()
        return result

    @verbose_output
    def maybe_indexed_symbol(self) -> str:
        """Parse a symbol with optional subscript index.

        Returns:
            str: Symbol with index notation or "".
        """
        result = self.regular_letter()
        if result != "":
            lower_index = self.lower_index()
            if lower_index != "":
                result += "_{" + lower_index + "}"
            if self.pointed_contents.get_cur() == "'":
                result += "'"
                self.pointed_contents.move_ptr()
            return result
        return ""

    @verbose_output
    def grammar_symbol(self) -> str:
        """Parse any valid grammar symbol (regular or special).

        Returns:
            str: The parsed symbol or None if invalid.
        """
        result = self.special_letter()
        if result != "":
            return result
        result = self.maybe_indexed_symbol()
        return result

    @verbose_output
    def lower_index(self) -> str:
        """Parse subscript index notation (e.g., _{xyz}).

        Returns:
            str: The index content or "".
        """
        if not self.pointed_contents.move_no_raise_if_looks_at("_"):
            return ""
        self.pointed_contents.move_if_looks_at("{")
        lower_index = self.index_string()
        self.pointed_contents.move_if_looks_at("}")
        return lower_index

    @verbose_output
    def index_string(self) -> str:
        """Parse content inside subscript brackets.

        Returns:
            str: Index characters.

        Raises:
            FalseSyntaxExpectation: If no valid characters found.
        """
        result = self.regular_letter()
        if result == "":
            raise errors.FalseSyntaxExpectation(
                "a regular letter",
                self.pointed_contents.get_line(),
                self.pointed_contents.get_cur(),
            )
        while True:
            add = self.regular_letter()
            if add == "":
                break
            result += add
        return result

    @verbose_output
    def grammar_symbol_set(self, symbol_set: set) -> None:
        """Parse a set of symbols enclosed in curly braces.

        Args:
            symbol_set (set): Target set to populate (terminals/nonterminals).

        Raises:
            FalseSyntaxExpectation: On syntax errors.
            SymbolIsAlreadyInSet: For duplicate symbols.
        """
        self.pointed_contents.move_if_looks_at("{")
        cur_char = self.grammar_symbol()
        while cur_char != "":
            if cur_char in self.terminals:
                raise errors.SymbolIsAlreadyInSet(
                    cur_char, self.pointed_contents.get_line(), "terminals")
            if cur_char in self.nonterminals:
                raise errors.SymbolIsAlreadyInSet(
                    cur_char, self.pointed_contents.get_line(), "nonterminals")
            symbol_set.add(cur_char)
            if not self.pointed_contents.move_no_raise_if_looks_at(","):
                break
            cur_char = self.grammar_symbol()
        self.pointed_contents.move_if_looks_at("}")

    @verbose_output
    def named_set(self, name: str) -> None:
        """Parse a named symbol set declaration (T={...} or N={...}).

        Args:
            name (str): Expected set name ('T' or 'N').

        Raises:
            FalseSyntaxExpectation: On syntax errors.
        """
        self.pointed_contents.move_if_looks_at(name)
        self.pointed_contents.move_if_looks_at("=")
        self.grammar_symbol_set(self.terminals if name ==
                                "T" else self.nonterminals)
        self.pointed_contents.move_if_looks_at(";")

    @verbose_output
    def terminals_set(self) -> None:
        """Parse the terminal symbols set declaration (T={...})."""
        self.named_set("T")

    @verbose_output
    def nonterminals_set(self) -> None:
        """Parse the non-terminal symbols set declaration (N={...})."""
        self.named_set("N")

    @verbose_output
    def program(self) -> None:
        """Orchestrate full grammar parsing (sets + rules)."""
        self.terminals_set()
        self.nonterminals_set()
        self.set_of_rules()

    @verbose_output
    def analyze(self) -> Grammar:
        """Execute complete grammar analysis.

        Returns:
            Grammar: Fully parsed grammar structure.
        """
        self.program()
        return Grammar(self.rules_dict, self.is_verbose, self.terminals,
                       self.nonterminals)
