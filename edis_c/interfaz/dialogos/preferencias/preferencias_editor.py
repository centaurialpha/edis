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
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QListWidget
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QSizePolicy
from PyQt4.QtGui import QFontDialog
from PyQt4.QtGui import QSpacerItem

from PyQt4.QtCore import Qt

from edis_c.nucleo import configuraciones


class ConfiguracionEditor(QWidget):

    def __init__(self, parent):
        super(ConfiguracionEditor, self).__init__(parent)

        layoutV = QVBoxLayout(self)

        grupoCaracteristicas = QGroupBox(self.trUtf8("Características"))
        grupoMiniMapa = QGroupBox(self.trUtf8("Minimapa"))
        grupoTipoDeLetra = QGroupBox(self.trUtf8("Tipo de letra"))
        grupoEstilo = QGroupBox(self.trUtf8("Estilo de color"))

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

        # Estilo
        lista_de_estilos = QListWidget()
        lista_de_estilos.addItem(self.tr("Blanco"))
        lista_de_estilos.addItem(self.tr("Negro"))
        layout = QVBoxLayout(grupoEstilo)
        layout.addWidget(lista_de_estilos)

        layoutV.addWidget(grupoCaracteristicas)
        layoutV.addWidget(grupoMiniMapa)
        layoutV.addWidget(grupoTipoDeLetra)
        layoutV.addWidget(grupoEstilo)
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