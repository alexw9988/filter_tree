

from PyQt5 import QtCore, QtGui, QtWidgets

from save_info.item import TypeItem, PathItem
from save_info.elements import DiskPathEdit, UrlPathEdit


class TypeDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self):
        super().__init__()

    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        return QtCore.QSize(size.width(), 30)

class PathDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self):
        super().__init__()

    def setEditorData(self, editor, index):
        t = index.data(TypeItem.ROLE_TYPE)
        p = index.data(PathItem.ROLE_PATH)

        if t == 'disk':
            editor.setText(p)
        elif t == 'web':
            editor.setText(p)
        else:
            super().setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        t = index.data(PathItem.ROLE_TYPE)

        if t == 'disk':
            p = editor.text()
        elif t == 'web':
            p = editor.text()
        else:
            return super().setModelData(editor, model, index)
        model.setData(index, p, PathItem.ROLE_PATH)

    def createEditor(self, parent, option, index):
        t = index.data(PathItem.ROLE_TYPE)
        p = index.data(PathItem.ROLE_PATH)
        # prop = index.data(PathItem.ROLE_PROPERTIES)

        if t == 'disk': 
            w = DiskPathEdit(parent=parent)
            w.setText(p)

        elif t == 'web':
            w = UrlPathEdit(parent=parent)
            w.setText(p)

        else:
            return super().createEditor(parent, option, index)

        return w

    