from PyQt5.QtWidgets import QStackedWidget

class InfoStackedWidget(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)