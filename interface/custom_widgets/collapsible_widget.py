from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QPropertyAnimation, QSize

class CollapsibleWidget(QWidget):
    def __init__(self, parent=None):
        self.parent = parent
        super().__init__(parent=parent)
        self.init_animation()


    def init_animation(self, start_width=None, start_height=None, end_width=None, end_height=None):
        if start_width is None:
            start_width = self.width()
        if start_height is None:
            start_height = 0
        if end_width is None:
            end_width= self.width()
        if end_height is None:
            end_height = self.height()

        print(start_width, start_height, end_width, end_height)

        animation = QPropertyAnimation(self.parent)
        animation.setTargetObject(self)
        animation.setPropertyName(b"size")

        animation.setStartValue(QSize(351, 0))
        animation.setEndValue(QSize(351, 80))
        # self.animation = animation
        animation.setDuration(3000)
        animation.start()
