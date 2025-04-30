import errors
from utility import PointedContents, Grammar

class Analyzer:

    def __init__(self, pointed_contents: PointedContents):

        self.regular_alphabet = [chr(c) for c in range(33, 127) if chr(c) not in [';', ',', '.', '{', '}', '>', '\\']]
        self.pointed_contents = pointed_contents
        self.terminals = set()
        self.nonterminals = set(["\\S", "\\E", "\\\\", "\\!"])
        self.rules_dict = dict()
        self.rules_lines_dict = dict()

    def non_empty_string(self):
        result_string = self.grammar_symbol()
        if result_string is None:
            raise errors.FalseSyntaxExpectation('a grammar symbol', self.pointed_contents.getLine(), self.pointed_contents.getCur())
        while True:
            symbol = self.grammar_symbol()
            if symbol is None:
                break
            result_string += symbol
        result_string = result_string.replace("\\E", "")
        return result_string

    def empty_string(self):
        if self.pointed_contents.getCur() == '\\' and self.pointed_contents.getAfterCur() == 'E':
            self.pointed_contents.movePtr()
            self.pointed_contents.movePtr()
            return "\\E"
        return None

    def string(self):
        if self.empty_string() is None:
            return self.non_empty_string()
        return "\\E"

    def transforms_to(self):
        if self.pointed_contents.getCur() != '>':
            raise errors.FalseSyntaxExpectation('>', self.pointed_contents.getLine(), self.pointed_contents.getCur())
        self.pointed_contents.movePtr()
        if self.pointed_contents.getCur() != '>':
            raise errors.FalseSyntaxExpectation('>', self.pointed_contents.getLine(), self.pointed_contents.getCur())
        self.pointed_contents.movePtr()

    def rule(self):
        lhs = self.non_empty_string()
        if lhs in self.rules_dict.keys():
            raise errors.RepeatedLeftSideOfRule(self.rules_lines_dict[lhs], self.pointed_contents.getLine())
        if all(c not in lhs for c in self.nonterminals):
            raise errors.LeftSideOfRuleHasOnlyTerminals(self.pointed_contents.getLine())
        if not self.is_allowed_string(lhs):
            raise errors.LeftSideOfRuleHasUndefinedSymbols(self.pointed_contents.getLine())
        self.rules_lines_dict[lhs] = self.pointed_contents.getLine()

        self.transforms_to()

        rhs = self.string()
        if not self.is_allowed_string(rhs):
            raise errors.RightSideOfRuleHasUndefinedSymbols(self.pointed_contents.getLine())
        self.rules_dict[lhs] = rhs

    def set_of_rules(self):
        while True:
            self.rule()
            if self.pointed_contents.getCur() == '.':
                self.pointed_contents.movePtr()
                break

            if self.pointed_contents.getCur() != ';':
                raise errors.FalseSyntaxExpectation('\";\"', self.pointed_contents.getLine(), self.pointed_contents.getCur())
            self.pointed_contents.movePtr()

    def is_allowed_string(self, string):
        def check(string, pos):
            if pos == len(string):
                return True
            if string[pos] == '\\':
                if pos + 1 == len(string) or string[pos + 1] not in ['E', 'S', '!', '\\']:
                    return False
                return check(string, pos + 2)
            if string[pos] not in self.terminals and string[it] not in self.nonterminals:
                return False
            return check(string, pos + 1)
        return check(string, 0)

    def regular_letter(self) -> str:
        if self.pointed_contents.getCur() not in self.regular_alphabet:
            return None
        result = self.pointed_contents.getCur()
        self.pointed_contents.movePtr()
        return result

    def special_letter(self) -> str:
        if self.pointed_contents.getCur() != '\\':
            return None
        self.pointed_contents.movePtr();
        result = "\\" + self.pointed_contents.getCur() if self.pointed_contents.getCur() in ['E', 'S', '!', '\\'] else None
        if result is None:
            raise errors.FalseSyntaxExpectation("E, S, !, or \\", self.pointed_contents.getLine(), self.pointed_contents.getCur())
        self.pointed_contents.movePtr()
        return result

    def grammar_symbol(self) -> str:
        result = self.regular_letter()
        if result is not None:
            return result
        result = self.special_letter()
        if result is not None:
            return result
        return None

    def grammar_symbol_set(self, symbol_set):
        if self.pointed_contents.getCur() != "{":
            raise errors.FalseSyntaxExpectation("{", self.pointed_contents.getLine(), self.pointed_contents.getCur())
        self.pointed_contents.movePtr()
        cur_char = self.regular_letter()
        while cur_char is not None:
            if cur_char in self.terminals:
                raise errors.SymbolIsAlreadyInSet(cur_char, self.pointed_contents.getLine(), "terminals")
            if cur_char in self.nonterminals:
                raise errors.SymbolIsAlreadyInSet(cur_char, self.pointed_contents.getLine(), "non-terminals")
            symbol_set.add(cur_char)
            if self.pointed_contents.getCur() != ',':
                break
            self.pointed_contents.movePtr()
            cur_char = self.regular_letter()
        if self.pointed_contents.getCur() != '}':
            raise errors.FalseSyntaxExpectation("}", self.pointed_contents.getLine(), self.pointed_contents.getCur())
        self.pointed_contents.movePtr()

    def named_set(self, name: str):
        if self.pointed_contents.getCur() != name:
            raise errors.FalseSyntaxExpectation(name, self.pointed_contents.getLine(), self.pointed_contents.getCur())

        self.pointed_contents.movePtr()

        if self.pointed_contents.getCur() != "=":
            raise errors.FalseSyntaxExpectation("=", self.pointed_contents.getLine(), self.pointed_contents.getCur())

        self.pointed_contents.movePtr()
        self.grammar_symbol_set(self.terminals if name == "T" else self.nonterminals)
        if self.pointed_contents.getCur() != ";":
            raise errors.FalseSyntaxExpectation(";", self.pointed_contents.getLine(), self.pointed_contents.getCur())
        self.pointed_contents.movePtr();


    def terminals_set(self):
        self.named_set("T")

    def nonterminals_set(self):
        self.named_set("N")

    def program(self):
        self.terminals_set()
        self.nonterminals_set()
        self.set_of_rules()

    def analyze(self):
        self.program()
        return Grammar(self.rules_dict)
