"""GUI implementation using PySide6 for grammar interpreter."""

import sys

from gui.grammar_bridge import GrammarBridge
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout

from utility import Grammar


class MainForm(QDialog):
    """Deprecated GUI form (retained for backward compatibility).

    Attributes:
        terminals_label (QLabel): Display terminal symbols.
        nonterminals_label (QLabel): Display non-terminal symbols.
    """

    def __init__(self, parent=None):
        """Initialize main form."""
        super(MainForm, self).__init__(parent)
        self.setWindowTitle("My window")
        self.terminals_label = QLabel("The set of terminals: ")
        self.nonterminals_label = QLabel("The set of nonterminals: ")
        layout = QVBoxLayout(self)
        layout.addWidget(self.terminals_label)
        layout.addWidget(self.nonterminals_label)


def run_gui(grammar: Grammar) -> None:
    """Launch QML-based GUI for grammar visualization.

    Args:
        grammar (Grammar): Parsed grammar rules and symbols.
    """
    app = QGuiApplication()
    bridge = GrammarBridge(grammar)
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("bridge", bridge)
    engine.load("src/gui.qml")
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
