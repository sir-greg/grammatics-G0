"""Bridge between Python backend and QML frontend."""

from PySide6.QtCore import Property, QObject, Signal, Slot

from utility import Grammar


class GrammarBridge(QObject):
    """Exposes grammar data and processing logic to QML.

    Signals:
        grammarUpdated: Emitted when grammar data changes.
        stepsUpdated: Emitted when execution steps update.
        loadingChanged: Emitted when loading state changes.
        progressChanged: Emitted when progress updates.

    Properties:
        terminals (list): Terminal symbols (QML-readable).
        nonTerminals (list): Non-terminal symbols (QML-readable).
        rules (list): Grammar rules (QML-readable).
        steps (list): Execution steps (QML-readable).
        loading (bool): Loading state.
        progress (float): Processing progress (0.0-1.0).
    """

    grammarUpdated = Signal()
    stepsUpdated = Signal()
    loadingChanged = Signal()
    progressChanged = Signal()

    def __init__(self, grammar: Grammar):
        """Initiliaze grammar bridge.

        Args:
            grammar: the grammar to illustrate
        """
        super().__init__()
        self._grammar = grammar
        self._terminals = list(grammar.terminals)
        self._non_terminals = list(grammar.nonterminals)
        self._rules = [{
            "lhs": k,
            "rhs": v
        } for k, v in grammar.rules_dict.items()]
        self._steps: list[str] = []
        self.grammarUpdated.emit()
        self._loading: bool = False
        self._progress: float = 0.0

    @Property(list, notify=grammarUpdated)
    def terminals(self):
        """Show list of terminal symbols."""
        return self._terminals

    @Property(list, notify=grammarUpdated)
    def non_terminals(self):
        """Show list of non-terminal symbols."""
        return self._non_terminals

    @Property(list, notify=grammarUpdated)
    def rules(self):
        """Show list of grammar rules as dictionaries."""
        return self._rules

    @Property(list, notify=stepsUpdated)
    def steps(self):
        """Show list of execution steps."""
        return self._steps

    @Slot(str)
    def process_input(self, args: str) -> None:
        """Process input string using grammar rules.

        Args:
            args (str): Input arguments separated by spaces.
        """
        self._steps = []
        self._steps.append("Starting processing...")
        self.stepsUpdated.emit()

        for result in self._grammar.run_in_gui(args.split()):
            self._steps.append(result)
            self.stepsUpdated.emit()

        self._steps.append("Processing completed!")
        self.stepsUpdated.emit()
