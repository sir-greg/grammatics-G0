"""Utilities for file handling and grammar processing."""

import constants
from errors import FalseSyntaxExpectation


def read_contents(source_file: str) -> str:
    """Read and returns the contents of a file.

    Args:
        file: Path to the file.

    Returns:
        File content as a string.

    Note:
        Prints error messages for common exceptions but does not raise them.
    """
    with open(source_file, "r", encoding="utf-8") as file:
        content = file.read()
    return content


class PointedContents:
    """Manages traversal and line tracking of input content.

    Attributes:
        contents: Full content of the input file.
        ptr: Current position pointer.
        line_count: Current line number being processed.
    """

    def __init__(self, source_file: str) -> None:
        """Initialize with content from a file.

        Args:
            source_file: Path to the input file.
        """
        self.contents = read_contents(source_file)
        self.ptr = 0
        self.line_count = 1

    def get_cur(self) -> str:
        """Return the current character under the pointer.

        Raises:
            FalseSyntaxExpectation: If the pointer is at the EOF.
        """
        if self.ptr == len(self.contents):
            raise FalseSyntaxExpectation("a valid lexem", self.line_count,
                                         "EOF")
        return self.contents[self.ptr]

    def move_if_looks_at(self, symbol: str):
        """Move the pointer if the current character matches the symbol.

        Args:
            symbol: Expected character to match.

        Raises:
            FalseSyntaxExpectation: If the current character does not match.
        """
        if not self.move_no_raise_if_looks_at(symbol):
            raise FalseSyntaxExpectation(symbol, self.get_line(),
                                         self.get_cur())

    def move_no_raise_if_looks_at(self, symbol: str) -> bool:
        """Conditionally moves the pointer if the current character matches.

        Args:
            symbol: Character to check.

        Returns:
            True if moved, False otherwise.
        """
        if self.get_cur() != symbol:
            return False
        self.move_ptr()
        return True

    def get_after_cur(self) -> str:
        """Find the next non-whitespace character after the current position.

        Returns:
            The next character or "" if end of content.
        """
        cur_ptr = self.ptr + 1
        while cur_ptr < len(
                self.contents) and self.contents[cur_ptr].isspace():
            cur_ptr += 1
        return "" if cur_ptr == len(self.contents) else self.contents[cur_ptr]

    def move_ptr(self) -> None:
        """Advances the pointer, skipping whitespace and counting lines."""
        self.ptr += 1
        while self.ptr < len(
                self.contents) and self.contents[self.ptr].isspace():
            if self.contents[self.ptr] == "\n":
                self.line_count += 1
            self.ptr += 1

    def get_line(self) -> int:
        """Return the current line number being processed."""
        return self.line_count


class Grammar:
    """Represents a grammar and applies its rules to transform input strings.

    Attributes:
        rules_dict: Dictionary of replacement rules (LHS -> RHS).
        is_verbose: Whether to print the execution process.
        terminals: Set of terminal symbols.
        nonterminals: Set of non-terminal symbols.
    """

    def __init__(self, rules_dict: dict, is_verbose: bool, terminals: set,
                 nonterminals: set) -> None:
        """Initialize with a set of grammar rules.

        Args:
            rules_dict: Grammar rules as a dictionary.
            is_verbose: Verbosity flag.
            terminals: Set of terminal symbols.
            nonterminals: Set of non-terminal symbols.
        """
        self.rules_dict = rules_dict
        self.terminals = terminals
        self.nonterminals = nonterminals
        self.is_verbose = is_verbose
        self.input_string = ""

    def make_iteration(self) -> bool:
        """Apply the first applicable rule to the input string.

        Returns:
            True if a replacement was made, False otherwise.
        """
        for lhs, rhs in self.rules_dict.items():
            if lhs in self.input_string:
                if self.is_verbose:
                    print(lhs + " -> " + rhs)
                pos = self.input_string.index(lhs)

                # if lhs breaks a lower_index, or leaves an
                # unused apostrophe, than it would be a
                # wrong substitution
                if pos + len(lhs) < len(self.input_string) and (
                        self.input_string[pos + len(lhs)] == "'"
                        or self.input_string[pos + len(lhs)] == "_"):
                    continue

                self.input_string = self.input_string.replace(lhs, rhs, 1)
                return True
        return False

    def make_input_string(self, args: list) -> str:
        """Make input string from the arguments.

        Args:
            args: Input arguments to process.

        Returns:
            the resulting input string
        """
        return (constants.STARTING_SYMBOL + constants.DELIMETER.join(args) +
                constants.FINAL_SYMBOL)

    def run(self, args: list) -> None:
        """Execute the grammar transformation on given arguments.

        Args:
            args: Input arguments to process.
        """
        self.input_string = self.make_input_string(args)
        while self.make_iteration():
            pass
        self.input_string = self.input_string.replace(constants.EMPTY_STRING,
                                                      "")
        print(self.input_string)

    def run_in_gui(self, args: list):
        """Generate execution steps for GUI.

        Args:
            args: Input arguments to process.

        Yields:
            The current state of the input string after each transformation.
        """
        self.input_string = self.make_input_string(args)
        yield self.input_string
        while self.make_iteration():
            self.input_string = self.input_string.replace(
                constants.EMPTY_STRING, "")
            yield self.input_string
