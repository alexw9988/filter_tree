
from PyQt5 import QtCore, QtGui, QtWidgets

from parameters.item import Parameter, NameItem, ValueItem


class ParameterModel(QtGui.QStandardItemModel):
    """
    The ParameterModel holds onto all the 
    <filter_tree.parameters.item.Parameter> instances contained 
    within it and manages adding of the parameter's actual display 
    items, `NameItem` and `ValueItem`. 

    Use the `getValues()` method to return a dictionary of all
    parameter values. Use `serialize()` to return a serial
    representation of the entire parameter model. 

    Signals
    -------
    signal_parameter_changed(Parameter):
        Emitted when a parameter value changes. 
    signal_parameter_toggled(Parameter):
        Emitted when a parameter's active status changes. 
    signal_model_change:
        Emitted when either of the above signals is emitted. 
    """
    signal_parameter_changed = QtCore.pyqtSignal(Parameter)
    signal_parameter_toggled = QtCore.pyqtSignal(Parameter)
    signal_model_change = QtCore.pyqtSignal()

    def __init__(self, root_param, *args, **kwargs):
        """
        Initialize the ParameterModel.
        Do initialize the ParameterModel directly. Use `createModel()`
        classmethod instead!

        Parameters
        ----------
        root_param : filter_tree.parameters.item.Parameter
            The top-level root-parameter. All actual groups/parameters
            are children of this parameter
        """
        super().__init__(*args, **kwargs)
        self.root_param = rp = root_param
        self.setColumnCount(2)
        self.setHeaderData(0, QtCore.Qt.Horizontal, "Parameter")
        self.setHeaderData(1, QtCore.Qt.Horizontal, "Value")
        
        self.params = []
        self._loadItems(rp)

        self.signal_parameter_changed.connect(self.signal_model_change.emit)
        self.signal_parameter_toggled.connect(self.signal_model_change.emit)

        self.itemChanged.connect(self._onItemChange)

        self._readonly = False

    @classmethod 
    def createModel(cls, params={}):
        """
        Create a new ParameterModel instance.

        Parameters
        ----------
        params : dict
            Dictionary containing all top level parameters/groups as
            name:param_opts pairs. All children are contained in 
            the param_opts, alongside all other required attributes. 
            See <filter_tree.parameters.item.Parameter> documentation
            for a list of these attributes. 
            Parameter names must be unique throughout the entire 
            tree structure! 

        Returns
        -------
        obj : ParameterModel
            The newly created instance. 

        Raises
        ------
        ValueError
            Raised if there are doubled keys in the param dict. 
        """
        opts = {'type': 'group', 'children': params}
        root_param = Parameter('root', opts)
        cls._verifyRoot(root_param)
        obj = cls(root_param)

        print("created param_model",obj)
        return obj
    
    def getValues(self, only_active=True):
        """
        Return a dictionary containing all parameter values.
        
        Parameters
        ----------
        only_active : bool
            If True, only those parameters that are checked/set active
            will be returned
        
        Returns
        -------
        values : dict
            Dict containing all parameters as name:value pairs. 
        """
        if only_active:
            return {param.name: param.value for param in self.params if param.is_active and not param.type == 'group'}
        else:
            return {param.name: param.value for param in self.params if not param.type == 'group'}

    def serialize(self):
        """ Return a serialised representation of the entire model. """
        retval = self.root_param.serialize()['children']
        return retval

    def setReadonly(self, readonly=True):
        self._readonly = readonly
        for param in self.params: 
            param.setReadonly(readonly=readonly)

    def isReadonly(self):
        return self._readonly

    def openPersistentEditors(self, view):
        """ Open persistent editors for all boolean parameters. """
        for param in self.params:
            if param.type == 'bool':
                view.openPersistentEditor(param.value_item.index())

    def closePersistentEditors(self, view):
        """ Close persistent editors for all boolean parameters. """
        for param in self.params:
            if param.type == 'bool':
                view.closePersistentEditor(param.value_item.index())

    def _onItemChange(self, item):
        if isinstance(item, NameItem): 
            self.signal_parameter_toggled.emit(item.param)
        elif isinstance(item, ValueItem):
            self.signal_parameter_changed.emit(item.param)

    def _loadItems(self, param):
        """
        Recursively load all parameters and their children, 
        appending them to `self.params` list and adding
        their `NameItems` and `ValueItems` to the model.  
        """
        self.params.append(param)
        if param.name == 'root':
            parent = self.invisibleRootItem()
        else:
            parent = param.name_item
        
        for child in param.children:
            parent.appendRow([child.name_item, child.value_item])
            self._loadItems(child)

    @staticmethod
    def _verifyRoot(root):
        """
        Ensure that among all parameters and their children, 
        all internal names are unique (i.e. all parameter dict-keys).

        Raises
        ------
        ValueError
            Raised if at least one double found
        """
        def iterateChildren(param): 
            # yield the parameter and all its children (recursively)
            yield param
            for child in param.children:
                yield from iterateChildren(child)
        
        name_list = []
        for param in iterateChildren(root):
            name = param.name
            if name in name_list:
                raise ValueError("Parameter/Group names must be unique within parameter model! {} is double!".format(name))
            else:
                name_list.append(name)


    def __repr__(self):
        return str(self.serialize())

    def __str__(self):
        return "<ParameterModel>"+repr(self)


    
