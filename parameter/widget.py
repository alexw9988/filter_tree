
from PyQt5 import QtCore, QtWidgets, QtGui

from parameter.delegates import ValueDelegate


class ParameterWidget(QtWidgets.QTreeView):
    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setModel(model)
        self.setItemDelegateForColumn(1, ValueDelegate())
        self.setVerticalScrollMode(self.ScrollPerPixel)
        self.setHorizontalScrollMode(self.ScrollPerPixel)
        self.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)