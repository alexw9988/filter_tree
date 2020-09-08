
from PyQt5 import QtCore, QtWidgets, QtGui


class PreProcessedDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PostProcessedDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

class SavingDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        