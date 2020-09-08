
from PyQt5 import QtCore, QtGui, QtWidgets

from parameter.item import ValueItem


class ValueDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def createEditor(self, parent, option, index):
        t = index.data(ValueItem.ROLE_TYPE)
        v = index.data(ValueItem.ROLE_VALUE)
        p = index.data(ValueItem.ROLE_PROPERTIES)

        if t == 'int': 
            w = QtWidgets.QSpinBox(parent=parent)
            w.setMaximum(p['maximum'])
            w.setMinimum(p['minimum'])
            w.setSingleStep(p['single_step'])
            w.setValue(v)

        elif t == 'float':
            w = QtWidgets.QDoubleSpinBox(parent=parent)
            w.setMaximum(p['maximum'])
            w.setMinimum(p['minimum'])
            w.setSingleStep(p['single_step'])
            w.setValue(v)

        elif t == 'string':
            w = QtWidgets.QLineEdit(parent=parent)
            w.setText(v)

        elif t == 'list':
            w = QtWidgets.QComboBox(parent=parent)
            for option in p['options']:
                w.addItem(str(option))
            for idx in range(w.count()):
                w.setItemData(idx, p['option_descriptions'][idx], QtCore.Qt.ToolTipRole) 
            w.setCurrentText(str(v))

        elif t == 'named_list':
            w = QtWidgets.QComboBox(parent=parent)
            w.addItems(p['options'].keys())
            for key in p['options'].keys():
                for idx in range(w.count()):
                    if w.itemText(idx) == key: 
                        w.setItemData(idx, p['option_descriptions'][key], QtCore.Qt.ToolTipRole) 
            w.setCurrentText(v)

        elif t == 'bool':
            w = QtWidgets.QCheckBox(parent=parent)
            w.setText("active")
            w.setCheckState(v)

        elif t == 'group':
            w = QtWidgets.QWidget(parent=parent)

        else:
            return super().createEditor(parent, option, index)

        return w