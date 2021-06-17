
import sys
import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets

from parameters import ParameterModel
from tree.item import FilterItem
from save_info import SaveModel


app = QtWidgets.QApplication(sys.argv)

# a = np.array(((1,1,1),(2,2,2),(3,3,3)))
# param_model = ParameterModel.createModel()
# save_model = SaveModel.createModel()

# item = FilterItem()
# item.param_model = param_model
# item.save_model = save_model
# item.output = a

# print(item)
# print(item.param_model)
# print(item.save_model)
# print(item.output)

# item2 = item.clone(keep_output=True)

# print(item2)
# print(item2.param_model)
# print(item2.save_model)
# print(item2.output)

ROLE = QtCore.Qt.UserRole + 100

submodel = ParameterModel.createModel()
param_model = submodel.serialize()

param_dict = {
    'type': 'filter',
    'name': 'testitem',
    'param_model': param_model
}
item = FilterItem()

print(item.param_model)