
from PyQt5 import QtCore, QtWidgets, QtGui

from parameters.delegates import NameDelegate, ValueDelegate


class ParameterView(QtWidgets.QTreeView):
    """
    The ParameterView widget is used to display a ParameterModel instance.
    When set to readonly-mode, the parameters can only be viewed and not
    altered. When readonly-mode is off, an appropriate editor will 
    be displayed in the left column for each value when clicking on it. 
    """
    def __init__(self, model=None, readonly=False, *args, **kwargs):
        """
        Initialize the ParameterView instance. 

        Parameters
        ----------
        model : filter_tree.parameters.model.ParameterModel
            The parameter model to show. 
        readonly : bool
            If True, the parameters cannot be edited. 
        """
        super().__init__(*args, **kwargs)
        if model: 
            self.setModel(model)
        self._readonly = readonly

        #Delegate stuff 
        self.name_delegate = nd = NameDelegate()
        self.value_delegate = vd = ValueDelegate()
        self.setItemDelegateForColumn(0, nd)
        self.setItemDelegateForColumn(1, vd)
        self.model().openPersistentEditors(self)
        self.setReadonly(readonly=readonly)

        #Visual stuff 
        self.setVerticalScrollMode(self.ScrollPerPixel)
        self.setHorizontalScrollMode(self.ScrollPerPixel)
        self.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.setEditTriggers(self.CurrentChanged|self.DoubleClicked|self.SelectedClicked|self.EditKeyPressed)
        self.setSelectionMode(self.SingleSelection)
        self.expandAll()
        self.setAlternatingRowColors(True)
    
    def clear(self):
        """ Empty the view by removing the model """
        self.setModel(None)

    def setReadonly(self, readonly=True): 
        self._readonly = readonly
        self.model().setReadonly(readonly=readonly)
        if readonly:
            self.model().closePersistentEditors(self)
        else:
            self.model().openPersistentEditors(self)
        
    def isReadOnly(self):
        return self._readonly

        