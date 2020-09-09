
from PyQt5 import QtCore, QtGui, QtWidgets

__all__ = ['ResettableSpinbox', 'ResettableDoubleSpinbox',
    'ResettableLineEdit', 'ResettableComboBox', 'ResettableCheckBox']


class _ResettableElement(QtWidgets.QWidget):
    def __init__(self, editor_cls, default, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.editor_cls = editor_cls
        self.default = default

        self.lay = l = QtWidgets.QHBoxLayout()
        l.setContentsMargins(0,0,6,0)
        self.setLayout(l)

        self.editor = e = editor_cls()
        l.addWidget(e)

        self.button = b = QtWidgets.QToolButton()
        b.setText("↺")
        b.clicked.connect(self.onReset)
        b.setEnabled(False)
        if self.editor_cls in [QtWidgets.QSpinBox, QtWidgets.QDoubleSpinBox]:
            e.valueChanged.connect(lambda: b.setEnabled(True))
        elif self.editor_cls in [QtWidgets.QLineEdit]:
            e.textChanged.connect(lambda: b.setEnabled(True))
        elif self.editor_cls in [QtWidgets.QComboBox]:
            e.currentTextChanged.connect(lambda: b.setEnabled(True))
        elif self.editor_cls in [QtWidgets.QCheckBox]:
            e.stateChanged.connect(lambda: b.setEnabled(True))
        
        l.addWidget(b)

    def onReset(self):
        if self.editor_cls in [QtWidgets.QSpinBox, QtWidgets.QDoubleSpinBox]:
            self.editor.setValue(self.default)
        elif self.editor_cls in [QtWidgets.QLineEdit]:
            self.editor.setText(self.default)
        elif self.editor_cls in [QtWidgets.QComboBox]:
            self.editor.setCurrentText(str(self.default))
        elif self.editor_cls in [QtWidgets.QCheckBox]:
            self.editor.setChecked(self.default)
        else:
            return
        self.editor.repaint()
        self.button.setEnabled(False)
        self.button.repaint()
        

class ResettableSpinbox(_ResettableElement):
    def __init__(self, default, *args, **kwargs):
        editor_cls = QtWidgets.QSpinBox
        super().__init__(editor_cls, default, *args, **kwargs)
        
    def setValue(self, value): self.editor.setValue(value)
    def value(self): return self.editor.value()
    def setMaximum(self, value): self.editor.setMaximum(value)
    def maximum(self): return self.editor.maximum
    def setMinimum(self, value): self.editor.setMinimum(value)
    def minimum(self): return self.editor.minimum()
    def setSingleStep(self, value): self.editor.setSingleStep(value)
    def singleStep(self): self.editor.singleStep()


class ResettableDoubleSpinbox(_ResettableElement):
    def __init__(self, default, *args, **kwargs):
        editor_cls = QtWidgets.QDoubleSpinBox
        super().__init__(editor_cls, default, *args, **kwargs)
        
    def setValue(self, value): self.editor.setValue(value)
    def value(self): return self.editor.value()
    def setMaximum(self, value): self.editor.setMaximum(value)
    def maximum(self): return self.editor.maximum
    def setMinimum(self, value): self.editor.setMinimum(value)
    def minimum(self): return self.editor.minimum()
    def setSingleStep(self, value): self.editor.setSingleStep(value)
    def singleStep(self): self.editor.singleStep()


class ResettableLineEdit(_ResettableElement):
    def __init__(self, default, *args, **kwargs):
        editor_cls = QtWidgets.QLineEdit
        super().__init__(editor_cls, default, *args, **kwargs)
        
    def setText(self, value): self.editor.setText(value)
    def text(self): return self.editor.text()


class ResettableComboBox(_ResettableElement):
    def __init__(self, default, *args, **kwargs):
        editor_cls = QtWidgets.QComboBox
        super().__init__(editor_cls, default, *args, **kwargs)
        
    def setCurrentText(self, value): self.editor.setCurrentText(value)
    def currentText(self): return self.editor.currentText()
    def addItem(self, item): self.editor.addItem(item)
    def setItemData(self, index, data, role): self.editor.setItemData(index, data, role)
    def count(self): return self.editor.count()
    def itemText(self, index): return self.editor.itemText(index)


class ResettableCheckBox(_ResettableElement):
    def __init__(self, default, delegate, *args, **kwargs):
        editor_cls = QtWidgets.QCheckBox
        super().__init__(editor_cls, default, *args, **kwargs)
        self.delegate = delegate
        self.editor.stateChanged.connect(lambda: self.delegate.commitData.emit(self))
        
    def setChecked(self, value): self.editor.setChecked(value)
    def isChecked(self): return self.editor.isChecked()
    def setTristate(self, value): self.editor.setTristate(value)
    def isTristate(self): return self.editor.isTristate()
