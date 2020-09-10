
from PyQt5 import QtCore, QtGui, QtWidgets

from save_info.item import PathItem, Save, TypeItem


class SaveModel(QtGui.QStandardItemModel):
    """
    The `SaveModel` holds onto all the `<filter_tree.save_info.item.Save>`
    instances contained  within it and manages the `Save`'s actual 
    display items, `TypeItem` and `PathItem`. 

    Use the `getPaths()` method to return a dictionary of all
    save entries. Use `serialize()` to return a serial representation
    of the entire save model. 

    Signals
    -------
    signal_save_changed(Save):
        Emitted when a Save's path changes or a Save's active status
        changes. 
    signal_save_added(Save):
        Emitted when a `Save` is added to the model. 
    signal_save_removed:
        Emitted when a `Save` is removed from the model. 
    signal_model_change:
        Emitted when any of the above signals is emitted. 
    """
    signal_save_changed = QtCore.pyqtSignal(Save)
    signal_save_added = QtCore.pyqtSignal(Save)
    signal_save_removed = QtCore.pyqtSignal()
    signal_model_change = QtCore.pyqtSignal()

    def __init__(self, saves_list=[], *args, **kwargs):
        """
        Initialize the `SaveModel`.
        Do initialize the `SaveModel` directly. Use `createModel()`
        classmethod instead!

        Parameters
        ----------
        saves_list : list
            List of serial representations of `Save` objects to add 
            to the model. 
        """
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

    def setReadonly(self, readonly=True):
        self._readonly = readonly
        for save in self.saves: 
            save.setReadonly(readonly=readonly)

    def isReadonly(self):
        return self._readonly

    def getPaths(self, only_active=True):
        """
        Return a dictionary containing all save entries. 
        
        Parameters
        ----------
        only_active : bool
            If True, only those `Saves` that are checked/set active
            will be returned
        
        Returns
        -------
        paths : list
            List containing dictionaries with 'type' and 'path' entries
            for each `Save` in the model. 
        """
        paths = []
        for save in self.saves:
            if only_active and not save.is_active:
                continue
            save_info = {
                'type': save.type, 
                'path': save.path
            }
            paths.append(save_info)
        return paths 

    def serialize(self):
        """ Return a serialised representation of the entire model. """
        return [save.serialize() for save in self.saves]

    def addSave(self, save):
        """ 
        Add a `Save` instance to the internal saves list and adding
        the `TypeItem` and `PathItem` instances to the model. 

        Parameters 
        ----------
        save : filter_tree.save_info.item.Save
            The `Save` to add. 
        
        Raises
        ------
        TypeError:
            Raised if something other than a `Save` instance is passed. 
        """
        if not isinstance(save, Save):
            raise TypeError("Can only add saves of type filter_tree.save_info.item.Save, not {}!".format(type(save)))
        
        self.saves.append(save)
        self.appendRow([save.type_item, save.path_item])
        self.signal_save_added.emit(save)
            
    def removeSave(self, save):
        """
        Remove a specific `Save` instance from the model and the
        internal list. 

        Parameters
        ----------
        save : filter_tree.save_info.item.Save
            The `Save` to remove. 
        """
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
        """
        Create a `SaveModel` instance. 

        Parameters
        ----------
        saves_list : list
            List of serial representations of `Save` objects to add 
            to the model. 
            Each entry is a dictionary containing the following:
            - 'type': either 'disk' or 'web'
            - 'path' (optional): the save path or url
            - 'is_active' (optional): True or False 
            - 'properties' (optional)

        Returns
        -------
        obj : `SaveModel`
            The newly created `SaveModel` instance. 
        """
        obj = cls(saves_list)

        return obj

    def __repr__(self):
        return str(self.serialize())

    def __str__(self):
        return "<SaveModel>"+repr(self)
