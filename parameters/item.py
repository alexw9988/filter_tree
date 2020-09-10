
from PyQt5 import QtCore, QtGui, QtWidgets


class NameItem(QtGui.QStandardItem):
    """
    The name item is used to display the Parameter's full name 
    alongside a checkbox, which can be used to determine this 
    parameter's active state (unchecked means the parameter value
    will not be passed to the function). Only optional parameters
    can be unchecked.

    type, full_name, description, optional, is_active are all stored
    as part of the item's internal data structure and can be accessed
    directly as attributes. 
    """
    ROLE_TYPE = QtCore.Qt.UserRole + 1
    ROLE_FULL_NAME = QtCore.Qt.DisplayRole
    ROLE_DESCRIPTION = QtCore.Qt.ToolTipRole
    ROLE_OPTIONAL = QtCore.Qt.UserRole + 100
    ROLE_IS_ACTIVE = QtCore.Qt.CheckStateRole

    def __init__(self, param):
        """
        Initialize a NameItem instance.

        Parameters
        ----------
        param : filter_tree.parameters.item.Parameter
            The Parameter object that this NameItem belongs to
        """
        super().__init__()
        self._readonly = False

        self.param = param
        self.opts = opts = param.opts

        #Extract Parameter's opts and assign them to internal data structure
        self.type = opts['type']
        self.full_name = opts['full_name']
        self.description = opts['description']
        self.optional = opts['optional']
        self.is_active = opts['is_active']

        self.setFlags(self._getFlags())
    
    def setReadonly(self, readonly=True):
        """ Set the item's appearence to read-only """
        if readonly == self._readonly:
            return 
        else: 
            self._readonly = readonly
            self.setFlags(self._getFlags())

    def isReadonly(self):
        """ Return the item's read-only state """
        return self._readonly

    def __getattribute__(self, name):
        if name == 'type':
            return self.data(self.ROLE_TYPE)
        elif name == 'full_name':
            return self.data(self.ROLE_FULL_NAME)
        elif name == 'description':
            return self.data(self.ROLE_DESCRIPTION)
        elif name == 'optional':
            return self.data(self.ROLE_OPTIONAL)
        elif name == 'is_active':
            return self.data(self.ROLE_IS_ACTIVE)
        else:
            return super().__getattribute__(name)
    
    def __setattr__(self, name, value):
        if name == 'type':
            self.setData(value, self.ROLE_TYPE)
        elif name == 'full_name':
            self.setData(value, self.ROLE_FULL_NAME)
        elif name == 'description':
            self.setData(value, self.ROLE_DESCRIPTION)
        elif name == 'optional':
            self.setData(value, self.ROLE_OPTIONAL)
            self.setFlags(self._getFlags())
        elif name == 'is_active':
            if isinstance(value, bool): 
                setval = QtCore.Qt.Checked if value else QtCore.Qt.Unchecked
            else:
                setval = value
            self.setData(setval, self.ROLE_IS_ACTIVE)
        else:
            super().__setattr__(name, value)

    def _getFlags(self):
        flags = QtCore.Qt.ItemIsEnabled
        if self.optional:
            flags |= QtCore.Qt.ItemIsUserCheckable
        flags |= QtCore.Qt.ItemIsSelectable
        if self.isReadonly():
            flags &= ~QtCore.Qt.ItemIsEnabled 
        return flags


class ValueItem(QtGui.QStandardItem):
    """
    The ValueItem is used to display the parameter's value. A custom
    delegate (i.e. <filter_tree.parameters.delegates.ValueDelegate>) can
    make use of this item to display an appropriate editor and allow
    resetting the value to default. 

    type, value, default, description, properties are all stored
    as part of the item's internal data structure and can be accessed
    directly as attributes. 
    """
    ROLE_TYPE = QtCore.Qt.UserRole + 100
    ROLE_VALUE = QtCore.Qt.DisplayRole
    ROLE_DEFAULT = QtCore.Qt.UserRole + 200
    ROLE_DESCRIPTION = QtCore.Qt.ToolTipRole
    ROLE_PROPERTIES = QtCore.Qt.UserRole + 300

    def __init__(self, param):
        """
        Initialize a ValueItem instance.

        Parameters
        ----------
        param : filter_tree.parameters.item.Parameter
            The Parameter object that this ValueItem belongs to
        """
        super().__init__()
        self.param = param 
        self.opts = opts = param.opts
        
        #Extract Parameter's opts and assign them to internal data structure
        self.type = opts['type']
        self.value = opts['value']
        self.default = opts['default']
        self.description = opts['description']
        self.properties = opts['properties']

        self._readonly = False
        self.setFlags(self._getFlags())
    
    def setReadonly(self, readonly=True):
        """ Set the item's appearence to read-only """
        if readonly == self._readonly:
            return 
        else: 
            self._readonly = readonly
            self.setFlags(self._getFlags())

    def isReadonly(self):
        """ Return the item's read-only state """
        return self._readonly

    def __getattribute__(self, name):
        if name == 'type':
            return self.data(self.ROLE_TYPE) 
        elif name == 'value':
            return self.data(self.ROLE_VALUE)
        elif name == 'default':
            return self.data(self.ROLE_DEFAULT)
        elif name == 'description':
            return self.data(self.ROLE_DESCRIPTION)
        elif name == 'properties':
            return self.data(self.ROLE_PROPERTIES)
        else:
            return super().__getattribute__(name)
    
    def __setattr__(self, name, value):
        if name == 'type':
            self.setData(value, self.ROLE_TYPE)
        elif name == 'value':
            self.setData(value, self.ROLE_VALUE)
        elif name == 'default':
            self.setData(value, self.ROLE_DEFAULT)
        elif name == 'description':
            self.setData(value, self.ROLE_DESCRIPTION)
        elif name == 'properties':
            self.setData(value, self.ROLE_PROPERTIES)
        else:
            super().__setattr__(name, value)

    def _getFlags(self):
        flags = QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable
        if self.isReadonly():
            flags &= ~QtCore.Qt.ItemIsEnabled

        return flags


class Parameter(QtCore.QObject):
    """
    The `Parameter` object is used to store all information associated
    with a parameter. It has two members, `name_item` and `value_item`, 
    which are used to populate a `ParameterModel`. 

    A parameter can have any number of children, which can be accessed
    via its `children` member. 
    """

    def __init__(self, name, opts):
        """
        Initialize the `Parameter` object.

        Parameters
        ----------
        name : str
            The parameter's internal name. Should be unique. 
        opts : dict
            The parameter's options dict, containing the following:
            - type: group, int, float, string, list, named_list, bool
            - full_name (optional)
            - description (optional)
            - optional (optional): if true, the parameter can be set 
              to inactive 
            - is_active (optional)
            - value (optional)
            - default (optional for type='group')
            - properties (optional): a dict containing information 
              like 'options', 'option_descriptions', 'maximum', 'minimum',
              'single_step', ...
            - children (optional): a list of all child parameters
        """
        super().__init__()
        self.name = name
        self.opts = opts = self._verifyOpts(opts)

        self.children = []
        self._appendChildren(opts['children'])

        self.name_item = NameItem(self)
        self.value_item = ValueItem(self)

        self._readonly = False

    def setReadonly(self, readonly=True):
        self._readonly = readonly
        self.name_item.setReadonly(readonly=readonly)
        self.value_item.setReadonly(readonly=readonly)
        
    def isReadonly(self):
        return self._readonly

    def serialize(self): 
        """ 
        Return a serial representation of the `Parameter` and all its 
        children.
        """
        return {
            'type': self.type, 
            'full_name': self.full_name,
            'description': self.description,
            'optional': self.optional, 
            'is_active': self.is_active,
            'value': self.value,
            'default': self.default,
            'properties': self.properties,
            'children': {child.name: child.serialize() for child in self.children}
        }

    def _appendChildren(self, children_dict):
        for child_name, child_opts in children_dict.items():
            self.children.append(Parameter(child_name, child_opts))

    def __getattribute__(self, name):
        if name == 'type':
            return self.value_item.type
        elif name == 'full_name':
            return self.name_item.full_name
        elif name == 'description':
            return self.name_item.description
        elif name == 'optional':
            return self.name_item.optional
        elif name == 'is_active':
            return self.name_item.is_active
        elif name == 'value':
            if self.type == 'named_list': 
                return self.opts['properties']['options'][self.value_item.value]
            else: 
                return self.value_item.value
        elif name == 'default':
            return self.value_item.default
        elif name == 'properties':
            return self.value_item.properties
        else:
            return super().__getattribute__(name)

    def __setattr__(self, name, value):
        if name == 'type':
            self.name_item.type = value
            self.value_item.type = value
        elif name == 'full_name':
            self.name_item.full_name = value
        elif name == 'description':
            self.name_item.description = value
            self.value_item.description = value
        elif name == 'optional':
            self.name_item.optional = value
        elif name == 'is_active':
            self.name_item.is_active = value
        elif name == 'value':
            self.value_item.value = value
        elif name == 'default':
            self.value_item.default = value
        elif name == 'properties':
            self.value_item.properties = value
        else:
            super().__setattr__(name, value)

    def _verifyOpts(self, opts):
        if not isinstance(opts, dict):
            raise TypeError("Parameter options must be passed as dict!")
        
        keys = opts.keys()

        if not 'full_name' in keys:
            opts['full_name'] = self.name
        
        if not 'description' in keys:
            opts['description'] = ''
        
        if not 'optional' in keys:
            opts['optional'] = False
        
        if not 'is_active' in keys:
            opts['is_active'] = True
        else:
            if not opts['optional']:
                opts['is_active'] = True
        
        if not 'type' in keys:
            raise KeyError("Could not find 'type' in parameter dictionary of parameter {}".format(self.name))   
        else:
            opts['type'] = self._fixupType(opts['type'])

        if opts['type'] == 'group':
            opts['default'] = None
            opts['value'] = None
        else:
            if not 'default' in keys:
                raise KeyError("Could not find 'default' in parameter dictionary of parameter {}".format(self.name))
                
            if not 'value' in keys:
                opts['value'] = opts['default']

        if 'properties' in keys:
            properties = opts['properties']
            if not isinstance(properties, dict):
                raise TypeError("Parameter properties must be a dictionary!")
            opts['properties'] = self._fixupProperties(opts['type'], properties)
        else:
            opts['properties'] = self._fixupProperties(opts['type'], {})

        if 'children' in keys:
            if not isinstance(opts['children'], dict):
                raise TypeError("Parameter children must be passed in dictionary!")
        else:
            opts['children'] = {}

        return opts 

    def _fixupType(self, t):
        if not isinstance(t, str):
            raise TypeError("Parameter type must be passed as string!")

        t = t.lower().strip()
        if t in ['int', 'integer']:
            return 'int'
        elif t in ['float']:
            return 'float'
        elif t in ['str', 'string', 'text']:
            return 'string'
        elif t in ['list', 'combobox']:
            return 'list'
        elif t in ['named_list']: 
            return 'named_list'
        elif t in ['bool', 'boolean']:
            return 'bool'
        elif t in ['group', 'folder', 'category']:
            return 'group'
        else:
            raise ValueError("Invalid parameter type: {}".format(t))

    def _fixupProperties(self, t, p):
        keys = p.keys()

        if t == 'int':
            if not 'minimum' in keys:
                p['minimum'] = 0
            if not 'maximum' in keys:
                p['maximum'] = 99
            if not 'single_step' in keys:
                p['single_step'] = 1

        elif t == 'float':
            if not 'minimum' in keys:
                p['minimum'] = 0.0
            if not 'maximum' in keys:
                p['maximum'] = 1.0
            if not 'single_step' in keys:
                p['single_step'] = 0.1
           
        elif t == 'string':
            p = {}

        elif t == 'list':
            if 'options' in keys:
                options = p['options']
                if not isinstance(options, list):
                    raise TypeError("List options must be passed as list, not {}!".format(type(options)))
                opt_count = len(options)
            else:
                p['options'] = []
                opt_count = 0
            if 'option_descriptions' in keys:
                option_descriptions = p['option_descriptions']
                if not isinstance(option_descriptions, list):
                    raise TypeError("Combobox option descriptions must be passed as list, not {}!".format(type(option_descriptions)))
            else:
                p['option_descriptions'] = ['' for _ in range(opt_count)]
            opt_desc_count = len(p['option_descriptions'])
            
            if opt_count != opt_desc_count:
                raise ValueError("List option count is {} but {} option descriptions were given!".format(opt_count, opt_desc_count))
           
        elif t == 'named_list':
            if 'options' in keys:
                options = p['options']
                if not isinstance(options, dict):
                    raise TypeError("Named list options must be passed as dict, not {}!".format(type(options)))
                opt_count = len(options.keys())
            else:
                p['options'] = {}
                opt_count = 0
            if 'option_descriptions' in keys:
                option_descriptions = p['option_descriptions']
                if not isinstance(option_descriptions, dict):
                    raise TypeError("Named list option descriptions must be passed as dict, not {}!".format(type(option_descriptions)))
            else:
                p['option_descriptions'] = {key: '' for key, _ in p['options'].items()}
            opt_desc_count = len(p['option_descriptions'].keys())
            
            if opt_count != opt_desc_count:
                raise ValueError("Named list option count is {} but {} option descriptions were given!".format(opt_count, opt_desc_count))
        
        elif t == 'bool':
            p = {}
            
        elif t == 'group':
            p = {}
            
        else:
            raise ValueError("Invalid parameter type: {}".format(t))

        return p 

    def __repr__(self):
        return str(self.serialize())

    def __str__(self):
        return "<Parameter>"+repr(self)

   