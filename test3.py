import sys
from PyQt5 import QtCore, QtWidgets, QtGui

import save_info


saves_list = [
    {'type': 'disk', 'path': 'data/test'},
    {'type': 'disk', 'path': 'data/test2'},
    {'type': 'disk', 'path': 'data/test3'},
    {'type': 'disk', 'path': 'data/test4'}
]

app = QtWidgets.QApplication(sys.argv)
mw = QtWidgets.QMainWindow()

model = save_info.SaveModel.createModel(saves_list=saves_list)
print(model.saves[0])
# model = parameters.ParameterModel.createModel(params)
# model.signal_parameter_changed.connect(lambda param: print("parameter changed:",param.name))
# model.signal_parameter_enabled.connect(lambda param: print("parameter enabled:",param.name))
# state = model.serialize()
# model = parameters.ParameterModel.createModel(state)
# print(model.getValues())

central = QtWidgets.QWidget()
lay = QtWidgets.QVBoxLayout()
central.setLayout(lay)

view = save_info.SaveView(model=model, readonly=False)
controls = save_info.SaveControls(model=model, view=view)
lay.addWidget(view)
lay.addWidget(controls)

model.signal_model_change.connect(lambda: print("model changed"))
model.signal_save_added.connect(lambda save: print("save added", save.type))
model.signal_save_removed.connect(lambda: print("save removed"))
model.signal_save_changed.connect(lambda save: print("save changed", save.type))

mw.setCentralWidget(central)
mw.show()
app.exec()
