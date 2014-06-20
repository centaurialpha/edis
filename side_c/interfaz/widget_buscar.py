from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QStyle
from PyQt4.QtGui import QIcon

from PyQt4.QtCore import SIGNAL

from side_c import recursos


class WidgetBuscar(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        #self.parent = parent

        layoutH = QHBoxLayout(self)
        layoutH.setContentsMargins(0, 0, 0, 0)
        layoutH.setMargin(0)

        self.lineText = QLineEdit()
        self.lineText.setMaximumWidth(200)
        #self.lineText.setAlignment(Qt.AlignRight)
        self.boton_buscar = QPushButton(QIcon(
            recursos.ICONOS['buscar']), '')
        self.boton_anterior = QPushButton(
            self.style().standardIcon(QStyle.SP_ArrowLeft), '')
        self.boton_siguiente = QPushButton(
            self.style().standardIcon(QStyle.SP_ArrowRight), '')

        layoutH.addWidget(self.boton_buscar)
        layoutH.addWidget(self.lineText)
        layoutH.addWidget(self.boton_anterior)
        layoutH.addWidget(self.boton_siguiente)

        #self.connect(self.boton_buscar, SIGNAL("clicked()"),
         #   self.buscar_texto)