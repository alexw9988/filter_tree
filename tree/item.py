
import time
from collections.abc import MutableMapping

from PyQt5 import QtCore, QtGui, QtWidgets

from parameters import ParameterModel
from save_info import SaveModel


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
    TYPE_FILTER = QtGui.QStandardItem.UserType + 10
    TYPE_MODIFIER = QtGui.QStandardItem.UserType + 20
    TYPE_GROUP = QtGui.QStandardItem.UserType + 30
    TYPE_INPUT = QtGui.QStandardItem.UserType + 40
    TYPE_OUTPUT = QtGui.QStandardItem.UserType + 50

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
    ROLE_PARAM_MODEL = QtCore.Qt.UserRole + 701
    ROLE_SAVE_MODEL = QtCore.Qt.UserRole + 800
    ROLE_ID = QtCore.Qt.UserRole + 900
    ROLE_ICON = QtCore.Qt.DecorationRole
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        print("initializing item")
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
        print("creating param_model")
        param_model = ParameterModel.createModel()
        print("param_model", param_model)
        self.param_model = param_model
        print("param_model", self.param_model)
        self.save_model = SaveModel.createModel()
        print("save_model", self.save_model)
        self.id = str(time.time()) #Item id is the current time, converted to string. This ensures uniqueness
        print("initializing item done")
        
        
        print("self",self)

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
        elif name == 'param_model':
            return self.data(self.ROLE_PARAM_MODEL)
        elif name == 'save_model':
            return self.data(self.ROLE_SAVE_MODEL)
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
        elif name == 'param_model':
            self.setData(value, self.ROLE_PARAM_MODEL)
        elif name == 'save_model':
            self.setData(value, self.ROLE_SAVE_MODEL)
        elif name == 'id':
            self.setData(value, self.ROLE_ID)
        elif name == 'type':
            self.setData(value, self.ROLE_TYPE)
            self.icon = self._getIcon() #Icon is directly associated with type
        elif name == 'icon':
            self.setData(value, self.ROLE_ICON)
        else:
            super().__setattr__(name, value) 
    
    def appendChild(self, item):
        if not isinstance(item, FilterItem):
            raise TypeError("Can only append <FilterItems> as children, not {}".format(type(item)))
        if not self.type in [self.TYPE_GROUP, self.TYPE_MODIFIER, self.TYPE_OUTPUT]:
            raise Exception("Only groups, modifiers or outputs can have children!")
        self.appendRow(item)

    def removeChild(self, item=None, row=None):
        if item:
            if not isinstance(item, FilterItem):
                raise TypeError("Can only remove <FilterItems> from children, not {}".format(type(item)))
            for child in self.children():
                if item is child:
                    take_row = item.row()
                    self.takeRow(take_row)
                    return
            raise Exception("Cannot remove item that isn't a child!")
        elif row:
            if 0 > row > self.rowCount()-1:
                raise Exception("Cannot remove child. Invalid row number!")
            else:
                self.takeRow(row)
        
    def children(self):
        for child_i in range(self.rowCount()):
            yield self.child(child_i)

    def clone(self, keep_output=False, keep_children='all', keep_children_output=False):
        print("starting clone")
        obj = FilterItem.createItem(self.serialize(include_children=False))
        if keep_output:
            obj.output = self.output
            print("cloned output")
        if keep_children == 'all':
            for child in self.children():
                obj.appendChild(
                    child.clone(
                        keep_output=keep_children_output, 
                        keep_children='all', 
                        keep_children_output=keep_children_output
                    )
                )
        elif keep_children == 'first':
            for child in self.children():
                obj.appendChild(
                    child.clone(
                        keep_output=keep_children_output,
                        keep_children='none'
                    )
                )
        
        print("returning clone",obj)
        return obj

    def serialize(self, include_children=True):
        retval = {
            'type': self.type,
            'name': self.name,
            'full_name': self.full_name,
            'description': self.description,
            'is_active': self.is_active,
            'fn': self.fn,
            'param_model': self.param_model.serialize(),
            'save_model': self.save_model.serialize()
        } 
        if include_children:
            retval['children'] = [child.serialize() for child in self.children()]
        return retval

    def _getIcon(self):

        if self.type == self.TYPE_FILTER:
            return QtGui.QIcon('resources/filter.png')
        elif self.type == self.TYPE_MODIFIER:
            return QtGui.QIcon('resources/modifier.png')
        elif self.type == self.TYPE_GROUP:
            return QtGui.QIcon('resources/folder.png')
        elif self.type == self.TYPE_INPUT:
            return QtGui.QIcon('resources/input.png')
        elif self.type == self.TYPE_OUTPUT:
            return QtGui.QIcon()
        else:
            return QtGui.QIcon()

    @classmethod
    def createItem(cls, item_dict):
        if not isinstance(item_dict, MutableMapping):
            raise TypeError("Items must be passed as dict-like objects, not as {}!".format(type(item_dict)))
        
        keys = item_dict.keys()
        print("creating item")
        obj = cls()
        print("created item1",obj)

        #Check required arguments
        if 'type' in keys:
            obj.type = cls._fixupType(item_dict['type'])
        else:
            raise KeyError("Could not find 'type' in item dictionary!")
        if 'name' in keys:
            obj.name = name = item_dict['name']
        else: 
            raise KeyError("Could not find 'name' in item dictionary!")

        #Check optional arguments
        obj.full_name = item_dict['full_name'] if 'full_name' in keys else name
        obj.description = item_dict['description'] if 'description' in keys else ''
        obj.is_active = item_dict['is_ative'] if 'is_ative' in keys else True
        obj.fn = item_dict['fn'] if 'fn' in keys else None
        if 'param_model' in keys:
            obj.param_model = ParameterModel.createModel(params=item_dict['param_model'])
        else:
            obj.param_model = ParameterModel.createModel()
        if 'save_model' in keys:
            obj.save_model = SaveModel.createModel(saves_list=item_dict['save_model']) 
        else:
            obj.save_model = SaveModel.createModel()
        if 'children' in keys:
            children = item_dict['children']
            if not isinstance(children, list):
                raise TypeError("Children must be passed in list, not {}".format(type(children)))
            for child in children: 
                obj.appendRow(FilterItem.createItem(child))

        print("created item20",obj)
        return obj

    @classmethod
    def _fixupType(cls, t):
        if isinstance(t, int):
            return t
        elif isinstance(t, str):
            t = t.lower().strip()
            if t in ['generic', 'default', 'none']:
                return cls.TYPE_GENERIC
            elif t in ['filter']:
                return cls.TYPE_FILTER
            elif t in ['modifier']:
                return cls.TYPE_MODIFIER
            elif t in ['group', 'folder']:
                return cls.TYPE_GROUP
            elif t in ['input', 'in']:
                return cls.TYPE_INPUT
            elif t in ['output', 'out']:
                return cls.TYPE_OUTPUT
            else:
                raise ValueError("Item type string invalid! Only GENERIC, FILTER, MODIFIER, GROUP, INPUT, OUTPUT allowed!")
        else:
            raise TypeError("Item type must be passed either as int or string!")

    def __repr__(self):
        return str(self.serialize())

    def __str__(self):
        return "<FilterItem>"+repr(self)
