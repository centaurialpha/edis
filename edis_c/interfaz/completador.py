from PyQt4.QtGui import QCompleter

from PyQt4.QtCore import Qt

from edis_c.interfaz.editor import sintaxis


class Completador(QCompleter):

    def __init__(self, parent=None):
        palabras = sintaxis.palabras_reservadas
        QCompleter.__init__(self, palabras, parent)
        self.setCompletionMode(QCompleter.PopupCompletion)
        self.setCaseSensitivity(Qt.CaseInsensitive)
