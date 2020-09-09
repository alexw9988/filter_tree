
from PyQt5 import QtCore, QtGui, QtWidgets

from parameters.item import Parameter, NameItem, ValueItem


class ParameterModel(QtGui.QStandardItemModel):
    signal_parameter_changed = QtCore.pyqtSignal(Parameter)
    signal_parameter_enabled = QtCore.pyqtSignal(Parameter)
    signal_model_change = QtCore.pyqtSignal()

    def __init__(self, root_param, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root_param = rp = root_param
        self.setColumnCount(2)
        self.setHeaderData(0, QtCore.Qt.Horizontal, "Parameter")
        self.setHeaderData(1, QtCore.Qt.Horizontal, "Value")
        
        self.params = []
        self._loadItems(rp)

        self.signal_parameter_changed.connect(self.signal_model_change.emit)
        self.signal_parameter_enabled.connect(self.signal_model_change.emit)

        self.itemChanged.connect(self._onItemChange)

        self._readonly = False

    def setReadonly(self, readonly=True):
        self._readonly = readonly
        for param in self.params: 
            param.setReadonly(readonly=readonly)

    def isReadonly(self):
        return self._readonly

    def getValues(self, only_enabled=True):
        if only_enabled:
            return {param.name: param.value for param in self.params if param.is_active and not param.type == 'group'}
        else:
            return {param.name: param.value for param in self.params if not param.type == 'group'}

    def serialize(self):
        return self.root_param.serialize()['children']

    def openPersistentEditors(self, view):
        for param in self.params:
            if param.type == 'bool':
                view.openPersistentEditor(param.value_item.index())

    def closePersistentEditors(self, view):
        for param in self.params:
            if param.type == 'bool':
                view.closePersistentEditor(param.value_item.index())

    def _onItemChange(self, item):
        if isinstance(item, NameItem): 
            self.signal_parameter_enabled.emit(item.param)
        elif isinstance(item, ValueItem):
            self.signal_parameter_changed.emit(item.param)

    def _loadItems(self, param):
        self.params.append(param)
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

    
