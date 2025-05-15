import tempfile
from src.interpreter import interpret
from src.analizer import Analyzer
from src.utility import PointedContents, Grammar, read_contents

EXAMPLES_PATH = "tests/examples/"

def test_working_examples():
    # test working examples 
    interpret(EXAMPLES_PATH + "correct/unary_sum.g0", "11+1111", False, False)
    interpret(EXAMPLES_PATH + "correct/caster-with-lower-indexes.g0", "1111111", False, False)
    interpret(EXAMPLES_PATH + "correct/doubler.g0", "1111111", False, False)
    interpret(EXAMPLES_PATH + "correct/substring.g0", ["111", "1111111"], False, False)

def test_errors():
    # test examples with syntax errors in them
    interpret(EXAMPLES_PATH + "wrong/duplicate-symbol-in-set.g0", "", False, False)
    interpret(EXAMPLES_PATH + "wrong/left-side-has-only-terminals.g0", "", False, False)
    interpret(EXAMPLES_PATH + "wrong/left-side-has-undefined-symbols.g0", "", False, False)
    interpret(EXAMPLES_PATH + "wrong/right-side-has-undefined-symbols.g0", "", False, False)
    interpret(EXAMPLES_PATH + "wrong/wrong-terminals-def.g0", "", False, False)
    interpret(EXAMPLES_PATH + "wrong/expected-;.g0", "", False, False);

def test_verbose():
    interpret(EXAMPLES_PATH + "correct/unary_sum.g0", "11+1111", True, False)
    interpret(EXAMPLES_PATH + "correct/caster-with-lower-indexes.g0", "1111111", True, False)
    interpret(EXAMPLES_PATH + "correct/doubler.g0", "1111111", True, False)
    interpret(EXAMPLES_PATH + "correct/substring.g0", ["111", "1111111"], True, False)


def test_grammar_gui_version():
    source_file = EXAMPLES_PATH + "correct/unary_sum.g0"
    analyzer = Analyzer(PointedContents(source_file), False)
    grammar = analyzer.analyze()
    for result in grammar.runInGui(["111", "11"]):
        pass
