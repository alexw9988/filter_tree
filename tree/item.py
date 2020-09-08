
import time
from collections.abc import MutableMapping

from PyQt5 import QtCore, QtGui, QtWidgets

from parameter.model import ParameterModel


class FilterItem(QtGui.QStandardItem):
    """
    The FilterStep class used for all filter tree steps. 
    The step can take any of the following types:
    - Generic Item
    - Input Item
    - Filter Item
    - Group Item
    - Modifier Item

    All except the Generic Item type can be automatically created using the
    respective factory methods. 

    All Item data is stored in the data structure of `QStandardItem` and
    can be accessed directly as attributes of the `Item` instance. 
    """

    #TYPE constants
    TYPE_GENERIC = QtGui.QStandardItem.UserType + 0
    TYPE_FILTER = QtGui.QStandardItem.UserType + 1
    TYPE_MODIFIER = QtGui.QStandardItem.UserType + 2
    TYPE_GROUP = QtGui.QStandardItem.UserType + 3
    TYPE_INPUT = QtGui.QStandardItem.UserType + 10
    TYPE_OUTPUT = QtGui.QStandardItem.UserType + 11

    #DATA ROLE constants: use with setData(value, role) or data(role)
    ROLE_TYPE = QtCore.Qt.UserRole + 100
    ROLE_NAME = QtCore.Qt.UserRole + 200
    ROLE_FULL_NAME = QtCore.Qt.DisplayRole
    ROLE_DESCRIPTION = QtCore.Qt.ToolTipRole
    ROLE_IS_ACTIVE = QtCore.Qt.CheckStateRole
    ROLE_IS_PROCESSED = QtCore.Qt.UserRole + 500
    ROLE_HAS_PROCESSING_ERROR = QtCore.Qt.UserRole + 501
    ROLE_STATUS_MESSAGE = QtCore.Qt.UserRole + 502
    ROLE_OUTPUT = QtCore.Qt.UserRole + 600
    ROLE_FN = QtCore.Qt.UserRole + 700
    ROLE_PARAMS = QtCore.Qt.UserRole + 701
    ROLE_SAVE_INFO = QtCore.Qt.UserRole + 800
    ROLE_ID = QtCore.Qt.UserRole + 900
    ROLE_ICON = QtCore.Qt.DecorationRole
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.type = self.TYPE_GENERIC
        self.name = ""
        self.full_name = ""
        self.description = ""
        self.is_active = True
        self.is_processed = False
        self.has_processing_error = False
        self.status_message = "Not processed"
        self.output = None
        self.fn = None
        self.params = None
        self.save_info = None
        self.id = str(time.time()) #Item id is the current time, converted to string. This ensures uniqueness
        
    def __getattribute__(self, name):
        if name == 'type':
            return self.data(self.ROLE_TYPE)
        elif name == 'name':
            return self.data(self.ROLE_NAME)
        elif name == 'full_name':
            return self.data(self.ROLE_FULL_NAME)
        elif name == 'description':
            return self.data(self.ROLE_DESCRIPTION)
        elif name == 'is_active':
            value = self.data(self.ROLE_IS_ACTIVE)
            return True if value == QtCore.Qt.Checked else False
        elif name == 'is_processed':
            return self.data(self.ROLE_IS_PROCESSED)
        elif name == 'has_processing_error':
            return self.data(self.ROLE_HAS_PROCESSING_ERROR)
        elif name == 'status_message':
            return self.data(self.ROLE_STATUS_MESSAGE)
        elif name == 'output':
            return self.data(self.ROLE_OUTPUT)
        elif name == 'fn':
            return self.data(self.ROLE_FN)
        elif name == 'params':
            return self.data(self.ROLE_PARAMS)
        elif name == 'save_info':
            return self.data(self.ROLE_SAVE_INFO)
        elif name == 'id':
            return self.data(self.ROLE_ID)
        elif name == 'icon':
            return self.data(self.ROLE_ICON)
        else:
            return super().__getattribute__(name)

    def __setattr__(self, name, value):
        if name == 'name':
            self.setData(value, self.ROLE_NAME)
        elif name == 'full_name':
            self.setData(value, self.ROLE_FULL_NAME)
        elif name == 'description':
            self.setData(value, self.ROLE_DESCRIPTION)
        elif name == 'is_active':
            if type(value) == bool:
                value = QtCore.Qt.Checked if value else QtCore.Qt.Unchecked
            self.setData(value, self.ROLE_IS_ACTIVE)
        elif name == 'is_processed':
            self.setData(value, self.ROLE_IS_PROCESSED)
        elif name == 'has_processing_error':
            self.setData(value, self.ROLE_HAS_PROCESSING_ERROR)
        elif name == 'status_message':
            self.setData(value, self.ROLE_STATUS_MESSAGE)
        elif name == 'output':
            self.setData(value, self.ROLE_OUTPUT)
        elif name == 'fn':
            self.setData(value, self.ROLE_FN)
        elif name == 'params':
            self.setData(value, self.ROLE_PARAMS)
        elif name == 'save_info':
            self.setData(value, self.ROLE_SAVE_INFO)
        elif name == 'id':
            self.setData(value, self.ROLE_ID)
        elif name == 'type':
            self.setData(value, self.ROLE_TYPE)
            self.icon = self._getIcon() #Icon is directly associated with type
        elif name == 'icon':
            self.setData(value, self.ROLE_ICON)
        else:
            super().__setattr__(name, value) 
    
    def __repr__(self):
        return str(self.serialize())

    __str__ = __repr__ 
    
    def children(self):
        child_count = self.rowCount()
        for child_i in range(child_count):
            yield self.child(child_i)

    def clone(self, keep_output=False, keep_children='all',keep_children_output=True):
        pass 

    def serialize(self):
        return {
            'type': self.type,
            'name': self.name,
            'full_name': self.full_name,
            'description': self.description,
            'is_active': self.is_active,
            'fn': self.fn,
            'params': self.params,
            'save_info': self.save_info,
            'children': [child.serialize() for child in self.children()]
        } 

    def _getIcon(self):

        if self.type() == self.TYPE_FILTER:
            return QtGui.QIcon('resources/filter.png')
        elif self.type() == self.TYPE_MODIFIER:
            return QtGui.QIcon('resources/modifier.png')
        elif self.type() == self.TYPE_GROUP:
            return QtGui.QIcon('resources/folder.png')
        elif self.type() == self.TYPE_INPUT:
            return QtGui.QIcon('resources/input.png')
        elif self.type() == self.TYPE_OUTPUT:
            return QtGui.QIcon()
        else:
            return QtGui.QIcon()

    @classmethod
    def create(self):
        pass

    @classmethod
    def toInstance(cls, ob):
        if not isinstance(ob, MutableMapping):
            raise TypeError("Items must be passed as dict-like objects, not as {}!".format(type(ob)))
            
        keys = ob.keys()
        obj = cls()

        #Check required arguments
        if 'type' in keys:
            type_ = ob['type']
            if isinstance(type_, int):
                obj.type = type_
            elif isinstance(type_, str):
                type_ = type_.lower().strip()
                if type_ in ['generic', 'default', 'none']:
                    obj.type = cls.TYPE_GENERIC
                elif type_ in ['filter']:
                    obj.type = cls.TYPE_FILTER
                elif type_ in ['modifier']:
                    obj.type = cls.TYPE_MODIFIER
                elif type_ in ['group', 'folder']:
                    obj.type = cls.TYPE_GROUP
                elif type_ in ['input', 'in']:
                    obj.type = cls.TYPE_INPUT
                elif type_ in ['output', 'out']:
                    obj.type = cls.TYPE_OUTPUT
                else:
                    raise ValueError("Item type string invalid! Only GENERIC, FILTER, MODIFIER, GROUP, INPUT, OUTPUT allowed!")
            else:
                raise TypeError("Item type must be passed either as int or string!")
        else:
            raise KeyError("Could not find 'type' in item dictionary!")
        if 'name' in keys:
            obj.name = name = ob['name']
        else: 
            raise KeyError("Could not find 'name' in item dictionary!")

        #Check optional arguments
        obj.full_name = ob['full_name'] if 'full_name' in keys else name
        obj.description = ob['description'] if 'description' in keys else ''
        obj.is_active = ob['is_ative'] if 'is_ative' in keys else True
        obj.fn = ob['fn'] if 'fn' in keys else None
        obj.params = ob['params'] if 'params' in keys else []
        obj.save_info = ob['save_info'] if 'save_info' in keys else []
        if 'children' in keys:
            children = ob['children']
            if not isinstance(children, list):
                raise TypeError("Children must be passed in list, not {}".format(type(children)))
            for child in children: 
                obj.appendRow(FilterItem.toInstance(child))
