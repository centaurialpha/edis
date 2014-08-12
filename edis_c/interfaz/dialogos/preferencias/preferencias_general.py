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

# Módulos QtGui
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QGroupBox
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QCheckBox
from PyQt4.QtGui import QComboBox
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QTabWidget
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QSpacerItem
from PyQt4.QtGui import QSizePolicy

# Módulos QtCore
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QSettings

# Módulos EDIS
from edis_c import recursos
from edis_c.nucleo import configuraciones
#from edis_c.interfaz import atajos
from edis_c.nucleo import manejador_de_archivo


class TabGeneral(QWidget):

    def __init__(self, parent):
        super(TabGeneral, self).__init__()
        layoutV = QVBoxLayout(self)
        layoutV.setContentsMargins(0, 0, 0, 0)
        self.tabs = QTabWidget()
        self.configuracionGeneral = ConfiguracionGeneral(parent)
        #self.atajos = atajos.ConfiguracionAtajos()

        self.tabs.addTab(self.configuracionGeneral, self.trUtf8("General"))
        #self.tabs.addTab(self.atajos, self.trUtf8("Atajos"))

        layoutV.addWidget(self.tabs)

    def guardar(self):
        for i in range(self.tabs.count()):
            self.tabs.widget(i).guardar()


class ConfiguracionGeneral(QWidget):

    def __init__(self, parent):
        super(ConfiguracionGeneral, self).__init__(parent)
        self.dialogo = parent
        layoutV = QVBoxLayout(self)

        grupoAlInicio = QGroupBox(self.trUtf8("Al iniciar:"))
        grupoAlCerrar = QGroupBox(self.trUtf8("Al cerrar:"))
        grupoIdioma = QGroupBox(self.trUtf8("Idioma:"))
        grupoReestablecer = QGroupBox(
            self.trUtf8("Reestablecer configuraciones de EDIS:"))

        # Al iniciar EDIS
        # Check página de inicio
        grillaAlInicio = QGridLayout(grupoAlInicio)
        self.checkPaginaInicio = QCheckBox(
            self.trUtf8("Mostrar página de inicio"))
        # Reabrir archivos de la última sesión
        self.checkUltimaSesion = QCheckBox(
            self.trUtf8("Cargar archivos desde la última sesión"))
        grillaAlInicio.addWidget(self.checkPaginaInicio,
            0, 0, alignment=Qt.AlignLeft)
        grillaAlInicio.addWidget(self.checkUltimaSesion,
            0, 1, alignment=Qt.AlignLeft)

        # Al cerrar EDIS
        grillaAlCerrar = QGridLayout(grupoAlCerrar)
        # Check confirmación al cerrar
        self.checkAlCerrar = QCheckBox(self.trUtf8("Confirmación al cerrar"))
        grillaAlCerrar.addWidget(self.checkAlCerrar, 0, 0)
        # Idioma
        layoutLeng = QVBoxLayout(grupoIdioma)
        layoutLeng.addWidget(QLabel(self.tr("Selecciona el idioma:")))
        self.comboIdioma = QComboBox()
        self.comboIdioma.setEnabled(False)
        layoutLeng.addWidget(self.comboIdioma)

        # Reestablecer preferencias
        layoutReset = QVBoxLayout(grupoReestablecer)
        self.boton_reestablecer = QPushButton(
            self.trUtf8("Reestablecer preferencias"))
        layoutReset.addWidget(self.boton_reestablecer, alignment=Qt.AlignLeft)
        layoutReset.addWidget(QLabel(
            self.trUtf8("<i>Reiniciar para ver cambios.</i>")))

        # Configuraciones
        self.checkPaginaInicio.setChecked(configuraciones.PAGINA_BIENVENIDA)
        self.checkAlCerrar.setChecked(configuraciones.CONFIRMAR_AL_CERRAR)
        self.checkUltimaSesion.setChecked(configuraciones.ULTIMA_SESION)

        layoutV.addWidget(grupoAlInicio)
        layoutV.addWidget(grupoAlCerrar)
        layoutV.addWidget(grupoIdioma)
        layoutV.addWidget(grupoReestablecer)
        layoutV.addItem(QSpacerItem(0, 10, QSizePolicy.Expanding,
            QSizePolicy.Expanding))
        self.cargar_idiomas()

        # Conexión
        self.boton_reestablecer.clicked.connect(self.reestablecer)

    def cargar_idiomas(self):
        idiomas = manejador_de_archivo.archivos_desde_carpeta(
            recursos.IDIOMAS, '.qm')
        self.idiomas = [u'Español'] + \
            [manejador_de_archivo.nombre_de_modulo(idioma)
            for idioma in idiomas]
        self.comboIdioma.addItems(self.idiomas)
        if(self.comboIdioma.count() > 1):
            self.comboIdioma.setEnabled(True)
        print configuraciones.IDIOMA
        if configuraciones.IDIOMA:
            i = self.comboIdioma.findText(configuraciones.IDIOMA)
        else:
            i = 0
        self.comboIdioma.setCurrentIndex(i)

    def guardar(self):
        """ Guarda las configuraciones Generales. """

        qconfig = QSettings()
        qconfig.beginGroup('configuraciones')
        qconfig.beginGroup('general')
        qconfig.setValue('paginaInicio', self.checkPaginaInicio.isChecked())
        qconfig.setValue('confirmacionCerrar', self.checkAlCerrar.isChecked())
        configuraciones.CONFIRMAR_AL_CERRAR = self.checkAlCerrar.isChecked()
        qconfig.setValue('ultimaSesion', self.checkUltimaSesion.isChecked())
        configuraciones.ULTIMA_SESION = self.checkUltimaSesion.isChecked()
        qconfig.endGroup()
        qconfig.endGroup()

    def reestablecer(self):
        SI = QMessageBox.Yes
        NO = QMessageBox.No
        r = QMessageBox.question(self,
            self.trUtf8("Reestablecer configuraciones?"),
            self.trUtf8("Quiere reestablecer las configuraciones?"),
            SI | NO)
        if r == SI:
            QSettings().clear()
            self.dialogo.close()