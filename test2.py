import sys
from PyQt5 import QtCore, QtWidgets, QtGui

import parameters


params = {
    'group1': {'full_name': 'Basic parameter data types', 'type': 'group', 'children': {
        'int1': {'full_name': 'Integer', 'type': 'int', 'default': 10},
        'float1': {'full_name': 'Float', 'type': 'float', 'default': 10.5, 'properties': {'minimum': 0, 'maximum': 100, 'single_step': 0.1}},
        'string1': {'full_name': 'String', 'type': 'str', 'default': "hi"},
        'list1': {'full_name': 'List', 'type': 'list', 'default': 2, 'properties': {'options': [1, 2, 3], 'option_descriptions': ['the first', 'the second', 'the third']}},
        'bool1': {'full_name': 'Boolean', 'type': 'bool', 'default': False, 'description': "This is a checkbox", 'optional':True, 'is_active': True}
    }
    }}

app = QtWidgets.QApplication(sys.argv)
mw = QtWidgets.QMainWindow()

model = parameters.ParameterModel.createModel(params)
model.signal_parameter_changed.connect(lambda param: print("parameter changed:",param.name))
model.signal_parameter_enabled.connect(lambda param: print("parameter enabled:",param.name))
state = model.serialize()
model = parameters.ParameterModel.createModel(state)
print(model.getValues())
central = parameters.ParameterWidget(model, readonly=False)
central.setReadonly(readonly=False)
mw.setCentralWidget(central)
mw.show()
app.exec()
