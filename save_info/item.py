
from PyQt5 import QtCore, QtGui, QtWidgets


class TypeItem(QtGui.QStandardItem):
    ROLE_TYPE = QtCore.Qt.DisplayRole
    ROLE_IS_ACTIVE = QtCore.Qt.CheckStateRole

    def __init__(self, save, opts, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._readonly = False

        self.save = save
        self.opts = opts

        self.type = opts['type']
        self.is_active = opts['is_active']

        self.setFlags(self._getFlags())
    
    def setReadonly(self, readonly=True):
        if readonly == self._readonly:
            return 
        else: 
            self._readonly = readonly
            self.setFlags(self._getFlags())

    def isReadonly(self):
        return self._readonly

    def __getattribute__(self, name):
        if name == 'type':
            return self.data(self.ROLE_TYPE)
        elif name == 'is_active':
            return self.data(self.ROLE_IS_ACTIVE)
        else:
            return super().__getattribute__(name)
    
    def __setattr__(self, name, value):
        if name == 'type':
            self.setData(value, self.ROLE_TYPE)
        elif name == 'is_active':
            if isinstance(value, bool): 
                setval = QtCore.Qt.Checked if value else QtCore.Qt.Unchecked
            else:
                setval = value
            self.setData(setval, self.ROLE_IS_ACTIVE)
        else:
            super().__setattr__(name, value)

    def _getFlags(self):
        flags = QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsSelectable
        if self.isReadonly():
            flags &= ~QtCore.Qt.ItemIsEnabled 
        return flags


class PathItem(QtGui.QStandardItem):
    ROLE_TYPE = QtCore.Qt.UserRole + 100
    ROLE_PATH = QtCore.Qt.DisplayRole
    ROLE_PROPERTIES = QtCore.Qt.UserRole + 200

    def __init__(self, save, opts, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.save = save 
        self.opts = opts
        
        self.type = opts['type']
        self.path = opts['path']
        self.properties = opts['properties']

        self._readonly = False
        self.setFlags(self._getFlags())
    
    def setReadonly(self, readonly=True):
        if readonly == self._readonly:
            return 
        else: 
            self._readonly = readonly
            self.setFlags(self._getFlags())

    def isReadonly(self):
        return self._readonly

    def __getattribute__(self, name):
        if name == 'type':
            return self.data(self.ROLE_TYPE) 
        elif name == 'path':
            return self.data(self.ROLE_PATH)
        elif name == 'properties':
            return self.data(self.ROLE_PROPERTIES)
        else:
            return super().__getattribute__(name)
    
    def __setattr__(self, name, value):
        if name == 'type':
            self.setData(value, self.ROLE_TYPE)
        elif name == 'path':
            self.setData(value, self.ROLE_PATH)
        elif name == 'properties':
            self.setData(value, self.ROLE_PROPERTIES)
        else:
            super().__setattr__(name, value)

    def _getFlags(self):
        flags = QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable
        if self.isReadonly():
            flags &= ~QtCore.Qt.ItemIsEnabled

        return flags


class Save(QtCore.QObject):
    """
    The `Save` object is used to store all information associated
    with a save entry. It has two members, `type_item` and `path_item`, 
    which are used to populate a `SaveModel`. 
    """
    def __init__(self, opts):
        """
        Initialize the `Parameter` object.

        Parameters
        ----------
        opts : dict
            The save's options dict, containing the following:
            - 'type': either 'disk' or 'web'
            - 'path' (optional): the save path or url
            - 'is_active' (optional): True or False 
            - 'properties' (optional)
        """
        super().__init__()
        self.opts = opts = self._verifyOpts(opts)

        self.type_item = TypeItem(self, opts)
        self.path_item = PathItem(self, opts)

        self._readonly = False

    def setReadonly(self, readonly=True):
        self._readonly = readonly
        self.type_item.setReadonly(readonly=readonly)
        self.path_item.setReadonly(readonly=readonly)
        
    def isReadonly(self):
        return self._readonly

    def serialize(self): 
        """ Return a serial representation of the `Save`. """
        return {
            'type': self.type, 
            'path': self.path,
            'is_active': self.is_active,
            'properties': self.properties
            }

    def __getattribute__(self, name):
        if name == 'type':
            return self.type_item.type
        elif name == 'path':
            return self.path_item.path
        elif name == 'is_active':
            return self.type_item.is_active
        elif name == 'properties':
            return self.path_item.properties
        else:
            return super().__getattribute__(name)

    def __setattr__(self, name, value):
        if name == 'type':
            self.type_item.type = value
            self.path_item.type = value 
        elif name == 'path':
            self.path_item.path = values
        elif name == 'is_active':
            self.type_item.is_active = value
        elif name == 'properties':
            self.path_item.properties = value
        else:
            super().__setattr__(name, value)

    def _verifyOpts(self, opts):
        if not isinstance(opts, dict):
            raise TypeError("Save options must be passed as dict!")
        
        keys = opts.keys()

        if not 'type' in keys:
            raise AttributeError("Could not find type in save options!")
        else:
            opts['type'] = self._fixupType(opts['type'])

        if not 'is_active' in keys:
            opts['is_active'] = True
        
        if not 'path' in keys:
            opts['path'] = ''

        if 'properties' in keys:
            properties = opts['properties']
            if not isinstance(properties, dict):
                raise TypeError("Save properties must be a dictionary!")
            opts['properties'] = self._fixupProperties(opts['type'], properties)
        else:
            opts['properties'] = self._fixupProperties(opts['type'], {})

        return opts 

    def _fixupType(self, t):
        if not isinstance(t, str):
            raise TypeError("Save type must be passed as string!")

        t = t.lower().strip()
        if t in ['disk', 'file', 'local']:
            return 'disk'
        elif t in ['web', 'internet', 'remote']:
            return 'web'
        else:
            raise ValueError("Invalid parameter type: {}".format(t))

    def _fixupProperties(self, t, p):
        keys = p.keys()

        if t == 'disk':
            p = {}
        elif t == 'web':
            p = {}
        else:
            raise ValueError("Invalid parameter type: {}".format(t))

        return p 

    def __repr__(self):
        return str(self.serialize())

    def __str__(self):
        return "<Save>"+repr(self)

   