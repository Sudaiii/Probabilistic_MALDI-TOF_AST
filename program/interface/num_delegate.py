from PyQt5.QtWidgets import QStyledItemDelegate, QLineEdit
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator


class NumDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = super().createEditor(parent, option, index)
        if isinstance(editor, QLineEdit):
            # No decimals
            # reg_ex = QRegExp("^\d+$")
            # 2 decimals
            reg_ex = QRegExp("^[0-9]*(\.[0-9]{0,2})?$")
            validator = QRegExpValidator(reg_ex, editor)
            editor.setValidator(validator)
        return editor
