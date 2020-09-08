
import json

from PyQt5 import QtCore, QtGui, QtWidgets


class NameItem(QtGui.QStandardItem):
    ROLE_TYPE = QtCore.Qt.UserRole + 1
    ROLE_FULL_NAME = QtCore.Qt.DisplayRole
    ROLE_DESCRIPTION = QtCore.Qt.ToolTipRole
    ROLE_OPTIONAL = QtCore.Qt.UserRole + 100
    ROLE_IS_ACTIVE = QtCore.Qt.CheckStateRole

    def __init__(self, opts, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opts = opts

        self.type = opts['type']
        self.full_name = opts['full_name']
        self.description = opts['description']
        self.optional = opts['optional']
        self.is_active = opts['is_active']

        self.setFlags(self._getFlags())

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
        if self.type == 'group':
            flags = QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsAutoTristate
        else:
            flags = QtCore.Qt.ItemIsEnabled
        if self.optional:
            flags |= QtCore.Qt.ItemIsUserCheckable
        flags |= QtCore.Qt.ItemIsSelectable
        return flags

class ValueItem(QtGui.QStandardItem):
    ROLE_TYPE = QtCore.Qt.UserRole + 1
    ROLE_VALUE = QtCore.Qt.DisplayRole
    ROLE_DEFAULT = QtCore.Qt.UserRole + 100
    ROLE_DESCRIPTION = QtCore.Qt.ToolTipRole
    ROLE_PROPERTIES = QtCore.Qt.UserRole + 200

    def __init__(self, opts, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opts = opts
        
        self.type = opts['type']
        self.value = opts['value']
        self.default = opts['default']
        self.description = opts['description']
        self.properties = opts['properties']

        self.setFlags(self._getFlags())
        
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
        if self.type == 'group':
            flags = QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsAutoTristate
        else:
            flags = QtCore.Qt.ItemIsEnabled
        flags |= QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable
        return flags


class Parameter(QtCore.QObject):
    def __init__(self, name, opts):
        super().__init__()
        self.name = name
        self.opts = opts = self._verifyOpts(opts)

        self.children = {}
        self._appendChildren(opts['children'])

        self.name_item = NameItem(opts)
        self.value_item = ValueItem(opts)

    def _appendChildren(self, children_dict):
        for child_name, child_opts in children_dict.items():
            self.children[child_name] = Parameter(child_name, child_opts)

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
            return self.value_item.value
        elif name == 'default':
            return self.value_item.default
        elif name == 'properties':
            return self.value_item.properties
        else:
            return super().__getattribute__(name)

    def __setattr__(self, name, value):
        if name == 'type':
            self.value_item.type = value
        elif name == 'full_name':
            self.name_item.full_name = value
        elif name == 'description':
            self.name_item.description = value
        elif name == 'optional':
            self.name_item.optional = value
        elif name == 'is_active':
            self.name_item.is_active = value
        elif name == 'value':
            self.value_item.value = value
        elif name == 'default':
            self.value_item.default = value
        elif name == 'properties':
            self.value_item.properties
        else:
            super().__setattr__(name, value)

    def _verifyOpts(self, opts):
        if not isinstance(opts, dict):
            raise TypeError("Parameter options must be passed as dict!")
        
        print("verifying opts:",opts)
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

    # def __repr__(self):
    #     return json.dumps(self.serialize())

    # __str__ = __repr__

    # def clone(self):
    #     ob = self.serialize()
    #     return ParameterItem.createInstance(ob)
    
    # def serialize(self):
    #     return {
    #         'name': self.name,
    #         'full_name': self.full_name,
    #         'description': self.description,
    #         'optional': self.optional,
    #         'wtype': self.wtype,
    #         'dtype': self._convertDTypeToString(self.dtype),
    #         'value': self.value,
    #         'default': self.default,
    #         'properties': self.properties
    #     }

   