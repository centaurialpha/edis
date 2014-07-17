# -*- coding: utf-8 -*-

# <Diálogo de preferencias generales.>
# Copyright (C) <2014>  <Gabriel Acosta>
# This file is part of EDIS-C.

# EDIS-C is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# EDIS-C is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with EDIS-C.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QGroupBox
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QCheckBox
from PyQt4.QtGui import QComboBox

from PyQt4.QtCore import Qt

from edis_c import recursos
from edis_c.nucleo import configuraciones
from edis_c.nucleo import manejador_de_archivo


class ConfiguracionGeneral(QWidget):

    def __init__(self, parent):
        super(ConfiguracionGeneral, self).__init__(parent)

        layoutV = QVBoxLayout(self)

        grupoAlInicio = QGroupBox(self.trUtf8("Al iniciar:"))
        grupoIdioma = QGroupBox(self.trUtf8("Idioma:"))

        grillaAlInicio = QGridLayout(grupoAlInicio)
        grillaAlInicio.addWidget(QLabel(
            self.trUtf8("Página de inicio:")), 1, 0, Qt.AlignLeft)

        # Al iniciar EDIS
        self.checkPaginaInicio = QCheckBox(
            self.trUtf8("Mostrar página de inicio"))
        self.checkPaginaInicio.setChecked(configuraciones.MOSTRAR_PAGINA_INICIO)
        grillaAlInicio.addWidget(self.checkPaginaInicio,
            1, 1, alignment=Qt.AlignLeft)

        # Idioma
        layoutLeng = QVBoxLayout(grupoIdioma)
        layoutLeng.addWidget(QLabel(self.tr("Selecciona el idioma:")))
        self.comboIdioma = QComboBox()
        self.comboIdioma.setEnabled(False)
        layoutLeng.addWidget(self.comboIdioma)
        layoutV.addWidget(grupoAlInicio)
        layoutV.addWidget(grupoIdioma)

        self.cargar_idiomas()

    def cargar_idiomas(self):
        idiomas = manejador_de_archivo.archivos_desde_carpeta(
            recursos.IDIOMAS, '.qm')
        self.idiomas = [u'Español'] + \
            [manejador_de_archivo.nombre_de_modulo(idioma) for idioma in idiomas]
        self.comboIdioma.addItems(self.idiomas)
        if(self.comboIdioma.count() > 1):
            self.comboIdioma.setEnabled(True)
        print configuraciones.IDIOMA
        if configuraciones.IDIOMA:
            i = self.comboIdioma.findText(configuraciones.IDIOMA)
        else:
            i = 0
        self.comboIdioma.setCurrentIndex(i)
