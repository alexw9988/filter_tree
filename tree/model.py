
from PyQt5 import QtCore, QtWidgets, QtGui


class FilterModel(QtGui.QStandardItemModel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    @classmethod
    def toInstance(cls, obj):
        pass 
    