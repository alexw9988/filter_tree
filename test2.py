
import sys 
from PyQt5 import QtCore, QtWidgets, QtGui

from parameter.widget import ParameterWidget
from parameter.model import ParameterModel


params = {
    'group1': {'full_name': 'Basic parameter data types', 'type': 'group', 'children': {
        'int1': {'full_name': 'Integer', 'type': 'int', 'default': 10},
        'float1': {'full_name': 'Float', 'type': 'float', 'default': 10.5, 'properties': {'minimum': 0, 'maximum': 100, 'single_step': 0.1}},
        'string1': {'full_name': 'String', 'type': 'str', 'default': "hi"},
        'list1': {'full_name': 'List', 'type': 'list', 'default': 2, 'properties': {'options': [1, 2, 3]}},
        'bool1': {'full_name': 'Boolean', 'type': 'bool', 'default': True, 'description': "This is a checkbox"}
    }
    }}

app = QtWidgets.QApplication(sys.argv)
mw = QtWidgets.QMainWindow()

model = ParameterModel.createModel(params)
print(model.rowCount())
central = ParameterWidget(model)
mw.setCentralWidget(central)
mw.show()
app.exec()
