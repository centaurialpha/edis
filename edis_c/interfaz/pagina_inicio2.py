import os

from PyQt4 import QtGui
from PyQt4.QtCore import QDir
from PyQt4.QtCore import QUrl
from PyQt4.QtCore import SIGNAL
from PyQt4.QtDeclarative import QDeclarativeView

import edis_c
from edis_c import recursos


class PaginaDeInicio(QtGui.QWidget):

    def __init__(self, parent=None):
        super(PaginaDeInicio, self).__init__(parent)
        self._id = edis_c.__nombre__
        vbox = QtGui.QVBoxLayout(self)
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        self.ver = QDeclarativeView()
        self.ver.setMinimumWidth(400)
        self.ver.setResizeMode(QDeclarativeView.SizeRootObjectToView)
        qml = QDir.fromNativeSeparators(os.path.join(
            recursos.PAGINA_INICIO, "pagina_de_inicio.qml"))
        self.ver.setSource(QUrl(qml))
        self.root = self.ver.rootObject()
        vbox.addWidget(self.ver)

        self.connect(self.root, SIGNAL("nuevoArchivo()"),
            lambda: self.emit(SIGNAL("nuevoArchivo()")))
        self.connect(self.root, SIGNAL("abrirArchivo()"),
            lambda: self.emit(SIGNAL("abrirArchivo()")))