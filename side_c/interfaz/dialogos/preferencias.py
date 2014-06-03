#-*- coding: utf-8 -*-

from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QTabWidget
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QSpinBox
from PyQt4.QtGui import QCheckBox
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QListWidget
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QSpacerItem
from PyQt4.QtGui import QSizePolicy
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QGroupBox
from PyQt4.QtGui import QFontDialog
from PyQt4.QtGui import QFont

from PyQt4.QtCore import QSize
from PyQt4.QtCore import Qt
#from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QSettings

from side_c import recursos
from side_c.nucleo import configuraciones
from side_c.interfaz import contenedor_principal


class Configuraciones(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        #self.ide = ide
        self.setWindowTitle(self.trUtf8("SIDE - Configuración"))
        self.setMaximumSize(QSize(0, 0))

        vbox = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.configEditor = ConfiguracionEditor(self)
        #self.configGeneral = General(self)
        self.configTema = CambiarTema()

        #self.tabs.addTab(self.configGeneral, self.trUtf8("General"))
        self.tabs.addTab(self.configEditor, self.trUtf8("Editor"))
        self.tabs.addTab(self.configTema, self.trUtf8("Tema"))

        self.tabs.setMovable(False)
        self.tabs.setTabsClosable(False)

        #vbox.setMargin(0)

        hbox = QHBoxLayout()
        self.botonGuardar = QPushButton(self.trUtf8("Guardar"))
        self.botonCancelar = QPushButton(self.trUtf8("Cancelar"))
        hbox.addWidget(self.botonGuardar)
        hbox.addWidget(self.botonCancelar)

        grilla = QGridLayout()
        grilla.addLayout(hbox, 0, 0, Qt.AlignRight)

        vbox.addWidget(self.tabs)
        vbox.addLayout(grilla)

        self.botonGuardar.clicked.connect(self._guardar)
        self.botonCancelar.clicked.connect(self._cancelar)

    def _cancelar(self):
        editorW = contenedor_principal.ContenedorMain().devolver_editor_actual()
        if editorW is None:
            self.close()

    def _guardar(self):
        self.configEditor.guardar()
        self.close()


class ConfiguracionEditor(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)

        v_layout = QVBoxLayout(self)

        grupoCaracteristicas = QGroupBox(self.trUtf8("Características"))
        grupoEstiloFuente = QGroupBox(self.trUtf8("Tipo de letra"))
        grillaCaracteristicas = QGridLayout(grupoCaracteristicas)
        grillaCaracteristicas.addWidget(QLabel(
            self.trUtf8("Márgen de línea: ")), 1, 0, Qt.AlignRight)

        # Spin márgen
        self.spinMargen = QSpinBox()
        self.spinMargen.setAlignment(Qt.AlignRight)
        self.spinMargen.setMaximum(200)
        self.spinMargen.setValue(configuraciones.MARGEN)
        grillaCaracteristicas.addWidget(self.spinMargen, 1, 1,
            alignment=Qt.AlignLeft)

        # Check márgen
        self.checkMargen = QCheckBox(self.trUtf8("Mostrar márgen"))
        self.checkMargen.setChecked(configuraciones.MOSTRAR_MARGEN)
        grillaCaracteristicas.addWidget(self.checkMargen, 1, 2,
            alignment=Qt.AlignRight)

        # Fuente
        grillaFuente = QGridLayout(grupoEstiloFuente)
        self.botonFuente = QPushButton(', '.join([configuraciones.FUENTE,
            str(configuraciones.TAM_FUENTE)]))
        grillaFuente.addWidget(QLabel(self.trUtf8(
            "Fuente:")), 0, 0, Qt.AlignLeft)
        grillaFuente.addWidget(self.botonFuente, 0, 1)

        v_layout.addWidget(grupoCaracteristicas)
        v_layout.addWidget(grupoEstiloFuente)
        v_layout.addItem(QSpacerItem(0, 10, QSizePolicy.Expanding,
            QSizePolicy.Expanding))

        # Conexión
        self.botonFuente.clicked.connect(self.cargar_fuente)

    def cargar_fuente(self):
        """ Se coloca el nombre y tamaño de la fuente, como texto del boton """

        fuente = self._cargar_fuente(self.obtener_texto_fuente(
            self.botonFuente.text()), self)

        self.botonFuente.setText(fuente)

    def obtener_texto_fuente(self, fuente):
        """
        Recibe el texto del botón,
        se crea una lista.
        1er elemento = Fuente
        2do elemento = Tamaño
        Se retorna QFont(Fuente, Tamaño)

        """

        if fuente:
            lista = fuente.split(',')

            f = str(lista[0]).strip()
            t = str(lista[1]).strip()

            fuente = QFont(f, int(t))
        else:
            fuente = QFont(configuraciones.FUENTE, configuraciones.TAM_FUENTE)

        return fuente

    def _cargar_fuente(self, f, parent=0):
        """ Se elige la fuente """

        fuente, ok = QFontDialog.getFont(f, parent)

        if not ok:
            n_fuente = f.toString().split(',')
        else:
            n_fuente = fuente.toString().split(',')

        nuevaFuente = n_fuente[0] + ', ' + n_fuente[1]
        return nuevaFuente

    def guardar(self):
        """ Guardar configuraciones """

        e = contenedor_principal.ContenedorMain().devolver_editor_actual()
        qsettings = QSettings()
        qsettings.beginGroup('configuraciones')
        qsettings.beginGroup('editor')

        # Márgen
        margen_linea = self.spinMargen.value()
        qsettings.setValue('margenLinea', margen_linea)
        configuraciones.MARGEN = margen_linea

        qsettings.setValue('mostrarMargen', self.checkMargen.isChecked())
        configuraciones.MOSTRAR_MARGEN = self.checkMargen.isChecked()

        # Tipo de letra
        textoFuente = self.botonFuente.text().replace(' ', '')
        configuraciones.FUENTE = textoFuente.split(',')[0]
        configuraciones.TAM_FUENTE = int(textoFuente.split(',')[1])
        qsettings.setValue('fuente', configuraciones.FUENTE)
        qsettings.setValue('fuenteTam', configuraciones.TAM_FUENTE)
        if e:
            e._cargar_fuente(configuraciones.FUENTE, configuraciones.TAM_FUENTE)
        qsettings.endGroup()
        qsettings.endGroup()

        contenedor_principal.ContenedorMain().actualizar_margen_editor()


class CambiarTema(QWidget):

    def __init__(self):
        super(CambiarTema, self).__init__()
        self.setWindowTitle(self.trUtf8("Cambiar tema"))
        self.tema_por_defecto = 0
        self.tema_side = 1
        self.tema_black_side = 2

        vbox = QVBoxLayout(self)

        label = QLabel("Elige un tema:")

        self.lista_temas = QListWidget()
        self.lista_temas.addItem("Default")
        self.lista_temas.addItem("SIDE")
        self.lista_temas.addItem("Black SIDE")

        boton_cambiar = QPushButton(self.trUtf8("Cambiar"))

        hbox = QHBoxLayout()
        hbox.addWidget(boton_cambiar)
        hbox.addSpacerItem(QSpacerItem(10, 0, QSizePolicy.Expanding,
            QSizePolicy.Fixed))

        vbox.addWidget(label)
        vbox.addWidget(self.lista_temas)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        boton_cambiar.clicked.connect(self._cambiar_tema)

    def _cambiar_tema(self):
        if self.lista_temas.currentRow() == self.tema_por_defecto:
            tema = recursos.TEMA_POR_DEFECTO
        elif self.lista_temas.currentRow() == self.tema_side:
            tema = recursos.TEMA_SIDE
        elif self.lista_temas.currentRow() == self.tema_black_side:
            tema = recursos.TEMA_BLACK_SIDE

        with open(tema, 'r') as archivo:
            t = archivo.read()
        QApplication.instance().setStyleSheet(t)
