
from PyQt5 import QtCore, QtWidgets, QtGui

from parameters.parameter import Parameter


class ParameterWidget(QtWidgets.QTreeWidget):
    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setModel(model)
        self.setItemDelegateForColumn(1, ValueDelegate())
        self.setVerticalScrollMode(self.ScrollPerPixel)
        self.setHorizontalScrollMode(self.ScrollPerPixel)
        self.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)