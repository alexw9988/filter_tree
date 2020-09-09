
from PyQt5 import QtCore, QtGui, QtWidgets

from parameters.item import NameItem, ValueItem
from parameters.elements import *


class NameDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self):
        super().__init__()

    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        return QtCore.QSize(size.width(), 30)

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        if index.data(NameItem.ROLE_TYPE) == 'group':
            option.features &= ~QtWidgets.QStyleOptionViewItem.HasCheckIndicator


class ValueDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self):
        super().__init__()

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        if index.data(ValueItem.ROLE_TYPE) == 'group':
            option.features &= ~QtWidgets.QStyleOptionViewItem.HasDisplay
        elif index.data(ValueItem.ROLE_TYPE) == 'bool':
            if index.data(ValueItem.ROLE_VALUE):
                option.text = "✓"
            else:
                option.text = "☓"

    def setEditorData(self, editor, index):
        t = index.data(ValueItem.ROLE_TYPE)
        v = index.data(ValueItem.ROLE_VALUE)

        if t == 'int':
            editor.setValue(v)
        elif t == 'float':
            editor.setValue(v)
        elif t == 'string':
            editor.setText(v)
        elif t == 'list':
            editor.setCurrentText(str(v))
        elif t == 'named_list':
            editor.setCurrentText(v)
        elif t == 'bool':
            editor.setChecked(v)
        else:
            super().setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        t = index.data(ValueItem.ROLE_TYPE)

        if t == 'int':
            v = editor.value()
        elif t == 'float':
            v = editor.value()
        elif t == 'string':
            v = editor.text()
        elif t == 'list':
            v = editor.currentText()
        elif t == 'named_list':
            v = editor.currentText()
        elif t == 'bool':
            v = editor.isChecked()
        else:
            return super().setModelData(editor, model, index)
        model.setData(index, v, ValueItem.ROLE_VALUE)

    def createEditor(self, parent, option, index):
        t = index.data(ValueItem.ROLE_TYPE)
        v = index.data(ValueItem.ROLE_VALUE)
        dv = index.data(ValueItem.ROLE_DEFAULT)
        p = index.data(ValueItem.ROLE_PROPERTIES)

        if t == 'int': 
            w = ResettableSpinbox(dv, parent=parent)
            w.setMaximum(p['maximum'])
            w.setMinimum(p['minimum'])
            w.setSingleStep(p['single_step'])
            w.setValue(v)

        elif t == 'float':
            w = ResettableDoubleSpinbox(dv, parent=parent)
            w.setMaximum(p['maximum'])
            w.setMinimum(p['minimum'])
            w.setSingleStep(p['single_step'])
            w.setValue(v)

        elif t == 'string':
            w = ResettableLineEdit(dv, parent=parent)
            w.setText(v)

        elif t == 'list':
            w = ResettableComboBox(dv, parent=parent)
            for option in p['options']:
                w.addItem(str(option))
            for idx in range(w.count()):
                w.setItemData(idx, p['option_descriptions'][idx], QtCore.Qt.ToolTipRole) 
            w.setCurrentText(str(v))

        elif t == 'named_list':
            w = ResettableComboBox(dv, parent=parent)
            w.addItems(p['options'].keys())
            for key in p['options'].keys():
                for idx in range(w.count()):
                    if w.itemText(idx) == key: 
                        w.setItemData(idx, p['option_descriptions'][key], QtCore.Qt.ToolTipRole) 
            w.setCurrentText(v)

        elif t == 'bool':
            w = ResettableCheckBox(dv, self, parent=parent)
            w.setTristate(False)
            w.setChecked(v)

        elif t == 'group':
            w = QtWidgets.QWidget(parent=parent)

        else:
            return super().createEditor(parent, option, index)

        return w

    