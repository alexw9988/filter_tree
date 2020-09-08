
from PyQt5 import QtCore, QtGui, QtWidgets

from parameter.item import Parameter


class ParameterModel(QtGui.QStandardItemModel):
    def __init__(self, root_param, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root_param = rp = root_param
        self.setColumnCount(2)
        self.setHeaderData(0, QtCore.Qt.Horizontal, "Parameter")
        self.setHeaderData(1, QtCore.Qt.Horizontal, "Value")
        
        self._loadItems(rp)

    def _loadItems(self, param):
        if param.name == 'root':
            parent = self.invisibleRootItem()
        else:
            parent = param.name_item
        
        for child in param.children.values():
            parent.appendRow([child.name_item, child.value_item])
            self._loadItems(child)

    @classmethod 
    def createModel(cls, params):
        opts = {}
        opts['type'] = 'group'
        opts['children'] = params
        root_param = Parameter('root', opts)
        obj = cls(root_param)

        return obj

    
