
from PyQt5 import QtCore, QtGui, QtWidgets


class _PathEdit(QtWidgets.QWidget):
    def __init__(self, editor_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.editor_type = editor_type
        if 'parent' in kwargs.keys():
            self.parent = kwargs['parent']
        else:
            self.parent = None

        self.lay = l = QtWidgets.QHBoxLayout()
        l.setContentsMargins(0,0,6,0)
        self.setLayout(l)

        self.editor = e = QtWidgets.QLineEdit()
        l.addWidget(e)

        self.button = b = QtWidgets.QToolButton()
        if self.editor_type == 'disk':
            b.setText('📁')
        elif self.editor_type == 'url':
            b.setText('🔗')
        b.clicked.connect(self.onOpen)
        l.addWidget(b)
        
    def onOpen(self): # reimplement in subclass 
        pass 
    
    def setText(self, value): self.editor.setText(value)
    def text(self): return self.editor.text()


class DiskPathEdit(_PathEdit):
    def __init__(self, *args, **kwargs):
        editor_type = 'disk'
        super().__init__(editor_type, *args, **kwargs)
        
    def onOpen(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(
            self.parent, "Choose save directory", self.text())
        if path != "": 
            self.setText(path)


class UrlPathEdit(_PathEdit):
    def __init__(self, *args, **kwargs):
        editor_type = 'url'
        super().__init__(editor_type, *args, **kwargs)

    def onOpen(self):
        path = QtWidgets.QFileDialog.getExistingDirectoryUrl(
            self.parent, "Choose save url", QtCore.QUrl(self.text()))
        if path.isValid(): 
            self.setText(path.toString())
