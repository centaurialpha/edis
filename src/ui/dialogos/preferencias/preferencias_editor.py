#-*- coding: utf-8 -*-

# <Diálogo de preferencias del editor.>
# This file is part of EDIS.

# Copyright (C) <2014>  <Gabriel Acosta>

# EDIS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# EDIS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with EDIS. If not, see <http://www.gnu.org/licenses/>.

# Módulos QtGui
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QLCDNumber
from PyQt4.QtGui import QSlider
from PyQt4.QtGui import QGroupBox
from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QSpinBox
from PyQt4.QtGui import QCheckBox
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QListWidget
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QSizePolicy
from PyQt4.QtGui import QFontDialog
from PyQt4.QtGui import QSpacerItem
from PyQt4.QtGui import QTabWidget

# Módulos QtCore
from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QSettings

# Módulos EDIS
from src import recursos
from src.helpers import configuraciones
#from src.nucleo import manejador_de_archivo
from src.ui.contenedor_principal import contenedor_principal
from src.ui.dialogos.preferencias import creador_tema


class TabEditor(QWidget):
    """ Tab Editor """

    def __init__(self):
        super(TabEditor, self).__init__()
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(3)
        self.configEditor = CaracteristicasEditor()
        self.generalEditor = GeneralEditor()
        self.creadorTema = creador_tema.CreadorDeTemaEditor(self)
        self.tabs.addTab(self.configEditor, self.trUtf8("Características"))
        self.tabs.addTab(self.generalEditor, self.trUtf8("General"))
        self.tabs.addTab(self.creadorTema, self.trUtf8("Creador de tema"))

        vbox.addWidget(self.tabs)

    def guardar(self):
        for i in range(self.tabs.count()):
            self.tabs.widget(i).guardar()


class CaracteristicasEditor(QWidget):
    """ Clase Configuracion Editor """

    def __init__(self):
        super(CaracteristicasEditor, self).__init__()
        layoutV = QVBoxLayout(self)

        grupoMargen = QGroupBox(self.trUtf8("Márgen de línea:"))
        grupoIndentacion = QGroupBox(self.trUtf8("Indentación:"))
        grupoMinimapa = QGroupBox(self.trUtf8("Minimapa:"))
        grupoExtras = QGroupBox(self.trUtf8("Extras:"))
        grupoTipoDeLetra = QGroupBox(self.trUtf8("Tipo de letra:"))
        grupoAutocompletado = QGroupBox(self.trUtf8("Autocompletado:"))

        # Márgen
        boxMargen = QHBoxLayout(grupoMargen)
        boxMargen.setContentsMargins(5, 5, 5, 0)
        # Check
        self.checkMargen = QCheckBox(self.trUtf8("Márgen: "))
        boxMargen.addWidget(self.checkMargen)
        # Spin opacidad de fondo
        self.spinOpacidadMargen = QSpinBox()
        self.spinOpacidadMargen.setSuffix(self.trUtf8("% Opacidad"))
        self.spinOpacidadMargen.setRange(0, 100)
        boxMargen.addWidget(self.spinOpacidadMargen)
        # Slide márgen
        self.slideMargen = QSlider(Qt.Horizontal)
        self.slideMargen.setMaximum(200)
        boxMargen.addWidget(self.slideMargen)
        self.connect(self.slideMargen, SIGNAL("valueChanged(int)"),
            lambda v: self.lcdMargen.display(v))
        # LCD márgen
        self.lcdMargen = QLCDNumber()
        boxMargen.addWidget(self.lcdMargen)

        # Indentación
        boxIndentacion = QGridLayout(grupoIndentacion)
        boxIndentacion.setContentsMargins(0, 0, 0, 0)
        # Check indentación
        self.checkInd = QCheckBox(self.trUtf8("Activar indentación"))
        boxIndentacion.addWidget(self.checkInd, 1, 0)
        self.sliderInd = QSlider(Qt.Horizontal)
        self.sliderInd.setMaximum(20)
        boxIndentacion.addWidget(self.sliderInd, 1, 1)
        self.connect(self.sliderInd, SIGNAL("valueChanged(int)"),
            lambda v: self.lcdInd.display(v))
        self.lcdInd = QLCDNumber()
        boxIndentacion.addWidget(self.lcdInd, 1, 2)
        # Check autoindentación
        self.checkAutoInd = QCheckBox(self.trUtf8("Activar autoindentación"))
        boxIndentacion.addWidget(self.checkAutoInd, 2, 0)
        # Guía indentación
        self.checkGuia = QCheckBox(self.trUtf8("Mostrar guía"))
        boxIndentacion.addWidget(self.checkGuia, 2, 1)

        # Extras
        boxExtras = QGridLayout(grupoExtras)
        boxExtras.setContentsMargins(0, 5, 0, 0)
        self.checkSideBar = QCheckBox(self.trUtf8("Mostrar números de línea"))
        boxExtras.addWidget(self.checkSideBar, 4, 0)

        # Tabs y espacios
        self.checkTabs = QCheckBox(self.trUtf8("Mostrar tabs y espacios"))
        boxExtras.addWidget(self.checkTabs, 4, 1)

        # Wrap mode
        self.checkWrap = QCheckBox(self.trUtf8("Modo envolver"))
        boxExtras.addWidget(self.checkWrap, 5, 0)

        # Minimapa
        grillaMini = QGridLayout(grupoMinimapa)
        grillaMini.setContentsMargins(5, 15, 5, 5)
        self.checkMini = QCheckBox(self.trUtf8("Activar minimapa"))
        self.spinMiniMin = QSpinBox()
        self.spinMiniMin.setRange(0, 100)
        self.spinMiniMin.setPrefix('Opacidad Min: ')
        self.spinMiniMin.setSuffix(' %')
        self.spinMiniMin.setAlignment(Qt.AlignLeft)
        self.spinMiniMax = QSpinBox()
        self.spinMiniMax.setRange(0, 100)
        self.spinMiniMax.setPrefix('Opacidad Max: ')
        self.spinMiniMax.setSuffix(' %')
        self.spinMiniMax.setAlignment(Qt.AlignLeft)
        self.spinTamanio = QSpinBox()
        self.spinTamanio.setPrefix(self.trUtf8('Tamaño: '))
        self.spinTamanio.setSuffix(self.tr(' %'))
        self.spinTamanio.setMaximum(100)
        self.spinTamanio.setMinimum(0)

        grillaMini.addWidget(self.checkMini, 0, 2)
        grillaMini.addWidget(self.spinMiniMin, 1, 1)
        grillaMini.addWidget(self.spinMiniMax, 1, 2)
        grillaMini.addWidget(self.spinTamanio, 1, 3)

        # Fuente
        grillaFuente = QGridLayout(grupoTipoDeLetra)
        grillaFuente.setContentsMargins(0, 0, 0, 0)
        self.botonFuente = QPushButton(', '.join([str(configuraciones.FUENTE),
            str(configuraciones.TAM_FUENTE)]))
        grillaFuente.addWidget(self.botonFuente, 0, 0)

        # Autocompletado
        grillaAutocompletado = QGridLayout(grupoAutocompletado)
        grillaAutocompletado.setContentsMargins(0, 5, 0, 0)
        self.checkComillasSimples = QCheckBox(self.trUtf8("Comillas simples"))
        self.checkComillasDobles = QCheckBox(self.trUtf8("Comillas dobles"))
        grillaAutocompletado.addWidget(self.checkComillasSimples, 0, 0)
        grillaAutocompletado.addWidget(self.checkComillasDobles, 1, 0)
        self.checkParentesis = QCheckBox(self.trUtf8("Paréntesis"))
        grillaAutocompletado.addWidget(self.checkParentesis, 0, 1)
        self.checkCorchetes = QCheckBox(self.trUtf8("Corchetes"))
        grillaAutocompletado.addWidget(self.checkCorchetes, 1, 1)
        self.checkLlaves = QCheckBox(self.trUtf8("Llaves"))
        grillaAutocompletado.addWidget(self.checkLlaves, 0, 2)

        # Configuraciones
        self.checkMargen.setChecked(configuraciones.MOSTRAR_MARGEN)
        self.spinOpacidadMargen.setValue(configuraciones.OPACIDAD_MARGEN)
        self.slideMargen.setValue(configuraciones.MARGEN)
        self.sliderInd.setValue(configuraciones.INDENTACION)
        self.checkInd.setChecked(configuraciones.CHECK_INDENTACION)
        self.checkAutoInd.setChecked(configuraciones.CHECK_AUTOINDENTACION)
        self.checkGuia.setChecked(configuraciones.GUIA_INDENTACION)
        self.checkTabs.setChecked(configuraciones.MOSTRAR_TABS)
        self.checkSideBar.setChecked(configuraciones.SIDEBAR)
        self.checkWrap.setChecked(configuraciones.MODO_ENVOLVER)
        self.checkMini.setChecked(configuraciones.MINIMAPA)
        self.spinMiniMin.setValue(configuraciones.OPAC_MIN * 100)
        self.spinTamanio.setValue(configuraciones.MINI_TAM * 100)
        self.spinMiniMax.setValue(configuraciones.OPAC_MAX * 100)
        self.checkComillasSimples.setChecked("'" in configuraciones.COMILLAS)
        self.checkComillasDobles.setChecked('"' in configuraciones.COMILLAS)
        self.checkLlaves.setChecked("{" in configuraciones.BRACES)
        self.checkCorchetes.setChecked("[" in configuraciones.BRACES)
        self.checkParentesis.setChecked("(" in configuraciones.BRACES)

        hbox = QHBoxLayout()
        layoutV.addWidget(grupoMargen)
        layoutV.addWidget(grupoIndentacion)
        layoutV.addWidget(grupoMinimapa)
        hbox.addWidget(grupoExtras)
        hbox.addWidget(grupoTipoDeLetra)
        layoutV.addLayout(hbox)
        layoutV.addWidget(grupoAutocompletado)
        layoutV.addItem(QSpacerItem(0, 10, QSizePolicy.Expanding,
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

    def previsualizar_estilo(self):
        tema = self.lista_de_estilos.currentItem().text()
        if tema == self.current_tema:
            return
        Weditor = contenedor_principal.ContenedorMain().devolver_editor_actual()
        if Weditor is not None:
            recursos.NUEVO_TEMA = self.temas.get(tema, recursos.TEMA_EDITOR)
            Weditor.estilo_editor()
        self.current_tema = tema

    def guardar(self):
        """ Guarda las configuraciones del Editor. """

        contenedor_principal_ = contenedor_principal.ContenedorMain()
        qconfig = QSettings(recursos.CONFIGURACION, QSettings.IniFormat)
        qconfig.beginGroup('configuraciones')
        qconfig.beginGroup('editor')
        qconfig.setValue('margenLinea', self.slideMargen.value())
        configuraciones.MARGEN = self.slideMargen.value()
        qconfig.setValue('mostrarMargen', self.checkMargen.isChecked())
        configuraciones.MOSTRAR_MARGEN = self.checkMargen.isChecked()
        configuraciones.OPACIDAD_MARGEN = self.spinOpacidadMargen.value()
        qconfig.setValue('opacidadMargen', self.spinOpacidadMargen.value())
        qconfig.setValue('checkInd', self.checkInd.isChecked())
        configuraciones.CHECK_INDENTACION = self.checkInd.isChecked()
        qconfig.setValue('guiaInd', self.checkGuia.isChecked())
        configuraciones.GUIA_INDENTACION = self.checkGuia.isChecked()
        qconfig.setValue('indentacion', self.sliderInd.value())
        configuraciones.INDENTACION = self.sliderInd.value()
        qconfig.setValue('autoInd', self.checkAutoInd.isChecked())
        configuraciones.CHECK_AUTOINDENTACION = self.checkAutoInd.isChecked()
        qconfig.setValue('tabs', self.checkTabs.isChecked())
        configuraciones.MOSTRAR_TABS = self.checkTabs.isChecked()
        qconfig.setValue('envolver', self.checkWrap.isChecked())
        configuraciones.MODO_ENVOLVER = self.checkWrap.isChecked()
        qconfig.setValue('sidebar', self.checkSideBar.isChecked())
        configuraciones.SIDEBAR = self.checkSideBar.isChecked()
        qconfig.setValue('configuraciones/editor/mini',
            self.checkMini.isChecked())
        configuraciones.MINIMAPA = self.checkMini.isChecked()
        configuraciones.MINI_TAM = self.spinTamanio.value() / 100.0
        qconfig.setValue('miniTam', configuraciones.MINI_TAM)
        qconfig.setValue('opac_min', configuraciones.OPAC_MIN)
        configuraciones.OPAC_MIN = self.spinMiniMin.value() / 100.0
        qconfig.setValue('opac_max', configuraciones.OPAC_MAX)
        configuraciones.OPAC_MAX = self.spinMiniMax.value() / 100.0
        fuente = unicode(self.botonFuente.text().replace(' ', ''))
        configuraciones.FUENTE = fuente.split(',')[0]
        configuraciones.TAM_FUENTE = int(fuente.split(',')[1])
        qconfig.setValue('fuente', configuraciones.FUENTE)
        qconfig.setValue('fuenteTam', configuraciones.TAM_FUENTE)
        qconfig.setValue('comillasS', self.checkComillasSimples.isChecked())
        qconfig.setValue('comillasD', self.checkComillasDobles.isChecked())
        qconfig.setValue('llaves', self.checkLlaves.isChecked())
        qconfig.setValue('corchetes', self.checkCorchetes.isChecked())
        qconfig.setValue('parentesis', self.checkParentesis.isChecked())
        if self.checkComillasSimples.isChecked():
            configuraciones.COMILLAS["'"] = "'"
        elif ("'") in configuraciones.COMILLAS:
            del configuraciones.COMILLAS["'"]
        if self.checkComillasDobles.isChecked():
            configuraciones.COMILLAS['"'] = '"'
        elif ('"') in configuraciones.COMILLAS:
            del configuraciones.COMILLAS['"']
        if self.checkLlaves.isChecked():
            configuraciones.BRACES['{'] = '}'
        elif ("{") in configuraciones.BRACES:
            del configuraciones.BRACES['{']
        if self.checkCorchetes.isChecked():
            configuraciones.BRACES['['] = ']'
        elif ("[") in configuraciones.BRACES:
            del configuraciones.BRACES["["]
        if self.checkParentesis.isChecked():
            configuraciones.BRACES['('] = ')'
        elif ("(") in configuraciones.BRACES:
            del configuraciones.BRACES['(']
        contenedor_principal_.actualizar_margen_editor()
        contenedor_principal_.resetear_flags_editor()
        Weditor = contenedor_principal_.devolver_editor_actual()
        if Weditor is not None:
            Weditor._cargar_fuente(
                configuraciones.FUENTE, configuraciones.TAM_FUENTE)
        qconfig.endGroup()
        qconfig.endGroup()


class GeneralEditor(QWidget):

    def __init__(self):
        super(GeneralEditor, self).__init__()
        layoutV = QVBoxLayout(self)

        grupoEstilo = QGroupBox(self.trUtf8("Estilo de color"))

        # Estilo
        self.lista_de_estilos = QListWidget()
        self.lista_de_estilos.addItem(self.tr("Default"))

        layoutH = QHBoxLayout(grupoEstilo)
        layoutH.addWidget(self.lista_de_estilos)
        layoutV.addWidget(grupoEstilo)

    def guardar(self):
        pass