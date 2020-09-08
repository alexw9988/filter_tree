
from PyQt5 import QtCore, QtWidgets, QtGui

from parameters.delegates import NameDelegate, ValueDelegate


class ParameterWidget(QtWidgets.QTreeView):
    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setModel(model)
        self.name_delegate = nd = NameDelegate()
        self.value_delegate = vd = ValueDelegate()
        self.setItemDelegateForColumn(0, nd)
        self.setItemDelegateForColumn(1, vd)
        self.setVerticalScrollMode(self.ScrollPerPixel)
        self.setHorizontalScrollMode(self.ScrollPerPixel)
        self.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.setEditTriggers(self.CurrentChanged|self.DoubleClicked|self.SelectedClicked|self.EditKeyPressed)
        self.expandAll()
        self.setAlternatingRowColors(True)
    
    
        