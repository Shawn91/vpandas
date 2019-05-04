from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import QSize

class TableTabWidget(QTabWidget):
    """A custom QTabWidget with size hint of (1,1) instead of the default (6,6) to make make a proper layout"""
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def sizeHint(self):
        return QSize(1,1)