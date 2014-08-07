#-*- coding: utf-8 -*-

# <Diálogo de preferencias del editor.>
# This file is part of EDIS-C.

# Copyright (C) <2014>  <Gabriel Acosta>

# EDIS-C is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# EDIS-C is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with EDIS-C. If not, see <http://www.gnu.org/licenses/>.

from PyQt4.QtGui import QWidget
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

from PyQt4.QtCore import Qt
from PyQt4.QtCore import QSettings

from edis_c import recursos
from edis_c.nucleo import configuraciones
#from edis_c.nucleo import manejador_de_archivo
from edis_c.interfaz.contenedor_principal import contenedor_principal
from edis_c.interfaz.dialogos.preferencias import creador_tema


class TabEditor(QWidget):
    """ Tab Editor """

    def __init__(self):
        super(TabEditor, self).__init__()
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)

        self.tabs = QTabWidget()
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

        grupoCaracteristicas = QGroupBox(self.trUtf8("Características"))
        grupoMiniMapa = QGroupBox(self.trUtf8("Minimapa"))
        grupoTipoDeLetra = QGroupBox(self.trUtf8("Tipo de letra"))

        grillaCaracteristicas = QGridLayout(grupoCaracteristicas)
        grillaCaracteristicas.setContentsMargins(5, 15, 5, 5)
        # Check márgen
        self.checkMargen = QCheckBox(self.trUtf8("Márgen de línea:"))
        grillaCaracteristicas.addWidget(self.checkMargen, 0, 0)
        # Spin opacidad de fondo
        self.spinOpacidadMargen = QSpinBox()
        self.spinOpacidadMargen.setSuffix(self.trUtf8("% Opacidad"))
        self.spinOpacidadMargen.setRange(0, 100)
        grillaCaracteristicas.addWidget(self.spinOpacidadMargen, 0, 3)

        # Spin márgen
        self.spinMargen = QSpinBox()
        self.spinMargen.setAlignment(Qt.AlignLeft)
        self.spinMargen.setSuffix(self.trUtf8(" Caractéres"))
        self.spinMargen.setMaximum(200)
        grillaCaracteristicas.addWidget(self.spinMargen, 0, 1)

        # Spin indentación
        self.spinInd = QSpinBox()
        self.spinInd.setSuffix(self.trUtf8(" Espacios"))
        self.spinInd.setAlignment(Qt.AlignLeft)
        self.spinInd.setMaximum(20)
        grillaCaracteristicas.addWidget(self.spinInd, 1, 1)

        # Check indentación
        self.checkInd = QCheckBox(self.trUtf8("Activar indentación"))
        grillaCaracteristicas.addWidget(self.checkInd, 1, 0)

        # Check autoindentación
        self.checkAutoInd = QCheckBox(self.trUtf8("Activar autoindentación"))
        grillaCaracteristicas.addWidget(self.checkAutoInd, 2, 0)

        # Guía indentación
        self.checkGuia = QCheckBox(self.trUtf8("Mostrar guía"))
        grillaCaracteristicas.addWidget(self.checkGuia, 3, 3)

        # Sidebar
        self.checkSideBar = QCheckBox(self.trUtf8("Mostrar números de línea"))
        grillaCaracteristicas.addWidget(self.checkSideBar, 3, 0)

        # Tabs y espacios
        self.checkTabs = QCheckBox(self.trUtf8("Mostrar tabs y espacios"))
        grillaCaracteristicas.addWidget(self.checkTabs, 1, 3)

        # Wrap mode
        self.checkWrap = QCheckBox(self.trUtf8("Modo envolver"))
        grillaCaracteristicas.addWidget(self.checkWrap, 2, 3)

        # Minimapa
        grillaMini = QGridLayout(grupoMiniMapa)
        grillaMini.setContentsMargins(5, 15, 5, 5)
        self.checkMini = QCheckBox(self.trUtf8("Activar minimapa"))
        self.spinMiniMin = QSpinBox()
        self.spinMiniMin.setRange(0, 100)
        self.spinMiniMin.setSuffix('% Min.')
        self.spinMiniMin.setAlignment(Qt.AlignLeft)
        self.spinMiniMax = QSpinBox()
        self.spinMiniMax.setRange(0, 100)
        self.spinMiniMax.setSuffix('% Max.')
        self.spinMiniMax.setAlignment(Qt.AlignLeft)
        self.spinTamanio = QSpinBox()
        self.spinTamanio.setMaximum(100)
        self.spinTamanio.setMinimum(0)
        self.spinTamanio.setSuffix(self.trUtf8('% Respecto al editor'))

        grillaMini.addWidget(self.checkMini, 0, 1)
        grillaMini.addWidget(QLabel(self.trUtf8("Opacidad:")),
            1, 0, alignment=Qt.AlignRight)
        grillaMini.addWidget(self.spinMiniMin, 1, 1)
        grillaMini.addWidget(self.spinMiniMax, 1, 2)
        grillaMini.addWidget(QLabel(self.trUtf8("Tamaño:")),
            2, 0, alignment=Qt.AlignRight)
        grillaMini.addWidget(self.spinTamanio, 2, 1)

        # Fuente
        grillaFuente = QGridLayout(grupoTipoDeLetra)
        grillaFuente.setContentsMargins(5, 15, 5, 5)
        self.botonFuente = QPushButton(', '.join([str(configuraciones.FUENTE),
            str(configuraciones.TAM_FUENTE)]))
        grillaFuente.addWidget(QLabel(self.trUtf8(
            "Fuente:")), 0, 0, Qt.AlignRight)
        grillaFuente.addWidget(self.botonFuente, 0, 1)

        # Configuraciones
        self.checkMargen.setChecked(configuraciones.MOSTRAR_MARGEN)
        self.spinOpacidadMargen.setValue(configuraciones.OPACIDAD_MARGEN)
        self.spinMargen.setValue(configuraciones.MARGEN)
        self.spinInd.setValue(configuraciones.INDENTACION)
        self.checkInd.setChecked(configuraciones.CHECK_INDENTACION)
        self.checkAutoInd.setChecked(configuraciones.CHECK_AUTO_INDENTACION)
        self.checkGuia.setChecked(configuraciones.GUIA_INDENTACION)
        self.checkTabs.setChecked(configuraciones.MOSTRAR_TABS)
        self.checkSideBar.setChecked(configuraciones.SIDEBAR)
        self.checkWrap.setChecked(configuraciones.MODO_ENVOLVER)
        self.checkMini.setChecked(configuraciones.MINIMAPA)
        self.spinMiniMin.setValue(configuraciones.OPAC_MIN * 100)
        self.spinTamanio.setValue(configuraciones.MINI_TAM * 100)
        self.spinMiniMax.setValue(configuraciones.OPAC_MAX * 100)

        layoutV.addWidget(grupoCaracteristicas)
        layoutV.addWidget(grupoMiniMapa)
        layoutV.addWidget(grupoTipoDeLetra)
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

        qconfig = QSettings()
        qconfig.beginGroup('configuraciones')
        qconfig.beginGroup('editor')
        qconfig.setValue('margenLinea', self.spinMargen.value())
        configuraciones.MARGEN = self.spinMargen.value()
        qconfig.setValue('mostrarMargen', self.checkMargen.isChecked())
        configuraciones.OPACIDAD_MARGEN = self.spinOpacidadMargen.value()
        qconfig.setValue('opacidadMargen', self.spinOpacidadMargen.value())
        configuraciones.MOSTRAR_MARGEN = self.checkMargen.isChecked()
        qconfig.setValue('checkInd', self.checkInd.isChecked())
        configuraciones.CHECK_INDENTACION = self.checkInd.isChecked()
        qconfig.setValue('guiaInd', self.checkGuia.isChecked())
        configuraciones.GUIA_INDENTACION = self.checkGuia.isChecked()
        qconfig.setValue('indentacion', self.spinInd.value())
        configuraciones.INDENTACION = self.spinInd.value()
        configuraciones.MINIMAPA = self.checkMini.isChecked()
        qconfig.setValue('mini', configuraciones.MINIMAPA)
        configuraciones.MINI_TAM = self.spinTamanio.value() / 100.0
        qconfig.setValue('miniTam', configuraciones.MINI_TAM)
        contenedor_principal.ContenedorMain().actualizar_margen_editor()
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