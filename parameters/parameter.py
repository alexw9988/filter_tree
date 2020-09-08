
from PyQt5 import QtCore, QtGui, QtWidgets

from parameters.item import NameWidget, ValueWidget


class Parameter(QtCore.QObject):

    value_changed_signal = QtCore.pyqtSignal(int)


    def __init__(self, parent, name, opts):
        super().__init__()
        self._parent = parent

        self._name_widget = NameWidget(opts)
        self._value_widget = ValueWidget(opts)

    def nameWidget(self):
        return self._name_widget
    
    def valueWidget(self):
        return self._value_widget