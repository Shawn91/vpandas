from PyQt5 import QtWidgets, QtCore

class InLineEditDelegate(QtWidgets.QItemDelegate):
    """Make table cells show content when double clicked for editing.
    """
    def createEditor(self, parent, option, index):
        return super().createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        text = index.data(QtCore.Qt.EditRole) or index.data(QtCore.Qt.DisplayRole)
        editor.setText(str(text))