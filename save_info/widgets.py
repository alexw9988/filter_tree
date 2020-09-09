
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUiType

from save_info.delegates import PathDelegate, TypeDelegate
from save_info.item import Save
from save_info.model import SaveModel

Ui_SaveControlsWindow, QSaveControls = loadUiType('save_info/save_controls.ui')


class SaveView(QtWidgets.QTableView):
    def __init__(self, model=None, readonly=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if model: 
            self.setModel(model)
        self._readonly = readonly

        #Delegate stuff 
        self.type_delegate = td = TypeDelegate()
        self.path_delegate = pd = PathDelegate()
        self.setItemDelegateForColumn(0, td)
        self.setItemDelegateForColumn(1, pd)
        self.setReadonly(readonly=readonly)

        #Visual stuff 
        self.setVerticalScrollMode(self.ScrollPerPixel)
        self.setHorizontalScrollMode(self.ScrollPerPixel)
        self.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.verticalHeader().hide()
        self.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        self.setEditTriggers(self.CurrentChanged|self.DoubleClicked|self.SelectedClicked|self.EditKeyPressed)
        self.setAlternatingRowColors(True)
    
    def currentSave(self):
        index = self.selectionModel().selectedIndexes()
        if len(index) == 0:
            return None
        else:
            index = index[0]
        item = self.model().itemFromIndex(index)
        save = item.save
        return save

    def setReadonly(self, readonly=True): 
        self._readonly = readonly
        self.model().setReadonly(readonly=readonly)

    def isReadOnly(self):
        return self._readonly


class SaveControls(QSaveControls, Ui_SaveControlsWindow):
    def __init__(self, model=None, view=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.registerModel(model)
        self.registerView(view)

        self.pb_add_save.clicked.connect(self.onAdd)
        self.pb_remove_save.clicked.connect(self.onRemove)

    def registerModel(self, model):
        if model is None:
            self.model = None
        else: 
            if not isinstance(model, SaveModel):
                raise TypeError("Can only bind <save_info.model.SaveModel> instances to SaveControls!")
            self.model = model

    def registerView(self, view):
        if view is None:
            self.view = None
        else:
            if not isinstance(view, SaveView):
                raise TypeError("Can only bind <save_info.widgets.SaveView> instances to SaveControls!")
            self.view = view

    def onAdd(self):
        if self.model is None:
            return

        type_ = self.cb_save_to.currentText().lower().strip()
        opts = {'type': type_}
        save = Save(opts)
        self.model.addSave(save)
        
        if self.view:
            index = save.path_item.index()
            self.view.selectionModel().select(index, QtCore.QItemSelectionModel.ClearAndSelect|QtCore.QItemSelectionModel.Rows)
            self.view.repaint()
            self.view.setCurrentIndex(index)

    def onRemove(self):
        if self.view is None:
            return

        save = self.view.currentSave()
        self.view.setCurrentIndex(QtCore.QModelIndex())
        if save is None:
            return 
        self.model.removeSave(save)
