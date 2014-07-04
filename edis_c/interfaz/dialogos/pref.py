#-*- coding: utf-8 -*-
""" Preferencias """

from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QGroupBox
from PyQt4.QtGui import QListWidget
from PyQt4.QtGui import QStackedWidget
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QListView
from PyQt4.QtGui import QListWidgetItem
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QSpinBox
from PyQt4.QtGui import QSpacerItem
from PyQt4.QtGui import QSizePolicy
from PyQt4.QtGui import QCheckBox
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QFontDialog

from PyQt4.QtCore import QSize
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QSettings

from edis_c import recursos
from edis_c.nucleo import configuraciones
from edis_c.interfaz.contenedor_principal import contenedor_principal


class ConfiguracionEditor(QWidget):

    def __init__(self, parent):
        super(ConfiguracionEditor, self).__init__(parent)

        layoutV = QVBoxLayout(self)

        grupoCaracteristicas = QGroupBox(self.trUtf8("Características"))
        grupoMiniMapa = QGroupBox(self.trUtf8("Minimapa"))
        grupoTipoDeLetra = QGroupBox(self.trUtf8("Tipo de letra"))
        grupoAutocompletado = QGroupBox(self.trUtf8("Autocompletado"))

        grillaCaracteristicas = QGridLayout(grupoCaracteristicas)
        grillaCaracteristicas.addWidget(QLabel(
            self.trUtf8("Márgen de línea: ")), 1, 0, Qt.AlignLeft)

        # Spin márgen
        self.spinMargen = QSpinBox()
        self.spinMargen.setAlignment(Qt.AlignLeft)
        self.spinMargen.setMaximum(200)
        self.spinMargen.setValue(configuraciones.MARGEN)
        grillaCaracteristicas.addWidget(self.spinMargen, 1, 1,
            alignment=Qt.AlignLeft)

        # Check márgen
        self.checkMargen = QCheckBox(self.trUtf8("Mostrar márgen"))
        self.checkMargen.setChecked(configuraciones.MOSTRAR_MARGEN)
        grillaCaracteristicas.addWidget(self.checkMargen, 1, 2,
            alignment=Qt.AlignTop)

        # Spin indentación
        self.spinInd = QSpinBox()
        self.spinInd.setAlignment(Qt.AlignLeft)
        self.spinInd.setMaximum(20)
        self.spinInd.setValue(configuraciones.INDENTACION)
        grillaCaracteristicas.addWidget(QLabel(
            self.trUtf8("Indentación: ")), 2, 0, Qt.AlignLeft)
        grillaCaracteristicas.addWidget(self.spinInd, 2, 1,
            alignment=Qt.AlignLeft)

        # Check indentación
        self.checkInd = QCheckBox(self.trUtf8("Activar indentación"))
        self.checkInd.setChecked(configuraciones.CHECK_INDENTACION)
        grillaCaracteristicas.addWidget(self.checkInd, 2, 2,
            alignment=Qt.AlignTop)

        # Check autoindentación
        self.checkAutoInd = QCheckBox(self.trUtf8("Activar autoindentación"))
        self.checkAutoInd.setChecked(
            configuraciones.CHECK_AUTO_INDENTACION)
        grillaCaracteristicas.addWidget(self.checkAutoInd, 3, 2,
            alignment=Qt.AlignLeft)

        # Sidebar
        self.checkSideBar = QCheckBox(self.trUtf8("Mostrar números de línea"))
        self.checkSideBar.setChecked(
            configuraciones.SIDEBAR)
        grillaCaracteristicas.addWidget(self.checkSideBar, 4, 2,
            alignment=Qt.AlignLeft)

        # Tabs y espacios
        self.checkTabs = QCheckBox(self.trUtf8("Mostrar tabs y espacios"))
        self.checkTabs.setChecked(configuraciones.MOSTRAR_TABS)
        grillaCaracteristicas.addWidget(self.checkTabs, 5, 2,
            alignment=Qt.AlignLeft)

        # Minimapa
        grillaMini = QGridLayout(grupoMiniMapa)
        self.checkMini = QCheckBox(self.trUtf8("Activar minimapa"))
        self.checkMini.setChecked(configuraciones.MINIMAPA)
        self.spinMiniMin = QSpinBox()
        self.spinMiniMin.setMaximum(100)
        self.spinMiniMin.setMinimum(0)
        self.spinMiniMin.setAlignment(Qt.AlignLeft)
        self.spinMiniMin.setValue(configuraciones.OPAC_MIN * 100)
        self.spinMiniMax = QSpinBox()
        self.spinMiniMax.setMaximum(100)
        self.spinMiniMax.setMinimum(0)
        self.spinMiniMax.setAlignment(Qt.AlignLeft)
        self.spinMiniMax.setValue(configuraciones.OPAC_MAX * 100)
        grillaMini.addWidget(self.checkMini, 1, 0,
            alignment=Qt.AlignLeft)
        grillaMini.addWidget(QLabel(self.trUtf8("Opacidad mínima:")),
            2, 0, alignment=Qt.AlignLeft)
        grillaMini.addWidget(self.spinMiniMin, 2, 1,
            alignment=Qt.AlignLeft)
        grillaMini.addWidget(QLabel(self.trUtf8("Opacidad máxima:")),
            3, 0, alignment=Qt.AlignLeft)
        grillaMini.addWidget(self.spinMiniMax, 3, 1,
            alignment=Qt.AlignLeft)

        # Fuente
        grillaFuente = QGridLayout(grupoTipoDeLetra)
        self.botonFuente = QPushButton(', '.join([str(configuraciones.FUENTE),
            str(configuraciones.TAM_FUENTE)]))
        grillaFuente.addWidget(QLabel(self.trUtf8(
            "Fuente:")), 0, 0, Qt.AlignLeft)
        grillaFuente.addWidget(self.botonFuente, 0, 1)

        layoutV.addWidget(grupoCaracteristicas)
        layoutV.addWidget(grupoMiniMapa)
        layoutV.addWidget(grupoTipoDeLetra)
        layoutV.addWidget(grupoAutocompletado)
        layoutV.addItem(QSpacerItem(0, 10, QSizePolicy.Expanding,
        QSizePolicy.Expanding))

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


class ConfiguracionTema(QWidget):

    def __init__(self, parent):
        super(ConfiguracionTema, self).__init__(parent)

        layoutV = QVBoxLayout(self)

        self.lista_temas = QListWidget()
        self.lista_temas.addItem("Por defecto")
        self.lista_temas.addItem("Black SIDE")

        label = QLabel(self.trUtf8("Elige un tema:"))

        layoutV.addWidget(label)
        layoutV.addWidget(self.lista_temas)


class DialogoConfiguracion(QDialog):

    def __init__(self, parent=None):
        super(DialogoConfiguracion, self).__init__(parent)
        self.setWindowTitle(self.trUtf8("SIDE-C Preferencias"))
        layoutH = QHBoxLayout()

        self.editorConf = ConfiguracionEditor(self)
        self.temaConf = ConfiguracionTema(self)

        self.contenidos = QListWidget()
        self.contenidos.setViewMode(QListView.IconMode)
        self.contenidos.setIconSize(QSize(96, 84))
        self.contenidos.setMovement(QListView.Static)
        self.contenidos.setMaximumWidth(102)
        self.contenidos.setSpacing(5)

        self.stack = QStackedWidget()
        self.stack.addWidget(self.editorConf)
        self.stack.addWidget(self.temaConf)

        boton_guardar = QPushButton(self.trUtf8("Guardar"))
        boton_cerrar = QPushButton(self.trUtf8("Cerrar"))

        self.iconos()
        self.contenidos.setCurrentRow(0)

        layoutH.addWidget(self.contenidos)
        layoutH.addWidget(self.stack, 1)

        layoutBoton = QHBoxLayout()
        layoutBoton.addStretch(1)
        layoutBoton.addWidget(boton_guardar)
        layoutBoton.addWidget(boton_cerrar)

        layoutPrincipal = QVBoxLayout()
        layoutPrincipal.addLayout(layoutH)
        layoutPrincipal.addStretch(1)
        layoutPrincipal.addSpacing(10)
        layoutPrincipal.addLayout(layoutBoton)

        self.setLayout(layoutPrincipal)

        boton_guardar.clicked.connect(self.guardar)
        boton_cerrar.clicked.connect(self.close)

    def cambiar(self, actual, anterior):
        if not actual:
            actual = anterior

        self.stack.setCurrentIndex(self.contenidos.row(actual))

    def guardar(self):
        qsettings = QSettings()
        qsettings.beginGroup('editor')
        e = contenedor_principal.ContenedorMain().devolver_editor_actual()

        # Márgen
        margen_linea = self.editorConf.spinMargen.value()
        qsettings.setValue('margenLinea', margen_linea)
        configuraciones.MARGEN = margen_linea

        qsettings.setValue('mostrarMargen',
            self.editorConf.checkMargen.isChecked())
        configuraciones.MOSTRAR_MARGEN = self.editorConf.checkMargen.isChecked()

         # Indentación
        qsettings.setValue('indentacion', self.editorConf.spinInd.value())
        configuraciones.INDENTACION = self.editorConf.spinInd.value()

        qsettings.setValue('checkInd', self.editorConf.checkInd.isChecked())
        configuraciones.CHECK_INDENTACION = self.editorConf.checkInd.isChecked()

        # Tipo de letra
        textoFuente = self.editorConf.botonFuente.text().replace(' ', '')
        configuraciones.FUENTE = textoFuente.split(',')[0]
        configuraciones.TAM_FUENTE = int(textoFuente.split(',')[1])
        qsettings.setValue('fuente', configuraciones.FUENTE)
        qsettings.setValue('fuenteTam', configuraciones.TAM_FUENTE)
        if e:
            e._cargar_fuente(configuraciones.FUENTE, configuraciones.TAM_FUENTE)

        # Sidebar
        qsettings.setValue('sidebar', self.editorConf.checkSideBar.isChecked())
        configuraciones.SIDEBAR = self.editorConf.checkSideBar.isChecked()

        # Tabs y espacios
        qsettings.setValue('tabs', self.editorConf.checkTabs.isChecked())
        configuraciones.MOSTRAR_TABS = self.editorConf.checkTabs.isChecked()

        # Minimapa
        qsettings.setValue('mini', self.editorConf.checkMini.isChecked())
        configuraciones.MINIMAPA = self.editorConf.checkMini.isChecked()
        configuraciones.OPAC_MIN = self.editorConf.spinMiniMin.value() / 100.0
        qsettings.setValue('opac_min', configuraciones.OPAC_MIN)
        configuraciones.OPAC_MAX = self.editorConf.spinMiniMax.value() / 100.0
        qsettings.setValue('opac_max', configuraciones.OPAC_MAX)

        qsettings.endGroup()
        contenedor_principal.ContenedorMain().actualizar_margen_editor()

        self.close()

    def iconos(self):
        configEditor = QListWidgetItem(self.contenidos)
        configEditor.setIcon(QIcon(recursos.ICONOS['editor']))
        configEditor.setText(self.trUtf8("Editor"))
        configEditor.setTextAlignment(Qt.AlignHCenter)
        configEditor.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        configTema = QListWidgetItem(self.contenidos)
        configTema.setIcon(QIcon(recursos.ICONOS['tema']))
        configTema.setText(self.trUtf8("Tema"))
        configTema.setTextAlignment(Qt.AlignHCenter)
        configTema.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        self.contenidos.currentItemChanged.connect(self.cambiar)