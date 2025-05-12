"""Main module for grammar interpreter execution."""

import argparse

import errors
from analizer import Analyzer
from gui.gui import run_gui
from utility import PointedContents


def interpret(source_file: str, args: list, is_verbose: bool,
              is_gui: bool) -> None:
    """Interpret a grammar source file and execute it with given arguments.

    Args:
        source_file: Path to the grammar definition file.
        args: List of input arguments for the grammar execution.
        is_verbose: Enable verbose output for debugging.
        is_gui: Launch the GUI interface if True.

    Raises:
        Exception: Propagates any errors encountered
        during analysis or execution.
    """
    try:
        analyzer = Analyzer(PointedContents(source_file), is_verbose)
        grammar = analyzer.analyze()
        if is_gui:
            run_gui(grammar)
        else:
            grammar.run(args)
    except errors.GrammarSyntaxError as e:
        print(e)
    except errors.GrammarSemanticError as e:
        print(e)


def argument_parsing():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("source_file",
                        help="the file to interpret as grammar instructions")
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="show the inner workings of interpreter",
    )
    parser.add_argument("--gui",
                        action="store_true",
                        help="run the gui version")
    parser.add_argument("args", help="the arguments of the program", nargs="*")
    return parser.parse_args()


def main() -> None:
    """Read command-line \
            arguments and start interpretation."""
    args = argument_parsing()
    interpret(args.source_file, args.args, args.verbose, args.gui)


if __name__ == "__main__":
    main()
