
from PyQt5 import QtCore, QtGui, QtWidgets

from save_info.item import Save, TypeItem, PathItem


class SaveModel(QtGui.QStandardItemModel):
    signal_save_changed = QtCore.pyqtSignal(Save)
    signal_save_added = QtCore.pyqtSignal(Save)
    signal_save_removed = QtCore.pyqtSignal()
    signal_model_change = QtCore.pyqtSignal()

    def __init__(self, saves_list, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setColumnCount(2)
        self.setHeaderData(0, QtCore.Qt.Horizontal, "Location")
        self.setHeaderData(1, QtCore.Qt.Horizontal, "Path")
        
        self.saves = []
        self._loadItems(saves_list)

        self.signal_save_changed.connect(self.signal_model_change.emit)
        self.signal_save_added.connect(self.signal_model_change.emit)
        self.signal_save_removed.connect(self.signal_model_change.emit)
        self.itemChanged.connect(self._onItemChange)

        self._readonly = False
        
    def registerView(self, view):
        self.view = view

    def setReadonly(self, readonly=True):
        self._readonly = readonly
        for save in self.saves: 
            save.setReadonly(readonly=readonly)

    def isReadonly(self):
        return self._readonly

    def getPaths(self, only_enabled=True):
        retval = []
        for save in self.saves:
            if only_enabled and not save.is_active:
                continue
            save_info = {
                'type': save.type, 
                'path': save.path
            }
        retval.append(save_info)

    def serialize(self):
        return [save.serialize() for save in self.saves]

    def addSave(self, save):
        if not isinstance(save, Save):
            raise TypeError("Can only add saves of type filter_tree.save_info.item.Save, not {}!".format(type(save)))
        
        self.saves.append(save)
        self.appendRow([save.type_item, save.path_item])
        self.signal_save_added.emit(save)
            
    def removeSave(self, save):
        for idx, curr_save in enumerate(self.saves):
            if curr_save == save:
                self.saves.pop(idx)
                break
        
        row = save.type_item.row()
        self.takeRow(row)
        self.signal_save_removed.emit()

    def _onItemChange(self, item):
        self.signal_save_changed.emit(item.save)

    def _loadItems(self, saves_list):
        for save_opts in saves_list:
            save = Save(save_opts)
            self.addSave(save)

    @classmethod 
    def createModel(cls, saves_list=[]):
        obj = cls(saves_list)

        return obj

    
