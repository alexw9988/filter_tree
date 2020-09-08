
import pyqtgraph as pg
import pyqtgraph.parametertree.parameterTypes as pTypes
from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph.parametertree import (Parameter, ParameterItem, ParameterTree,
                                     registerParameterType)


class ParameterModel(Parameter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def serialize(self):
        return self.saveState()
    
    @classmethod 
    def create(params=[]):
        return super().create(name='params', type='group', children=params)
