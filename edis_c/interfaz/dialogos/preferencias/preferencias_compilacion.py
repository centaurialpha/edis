#-*- coding: utf-8 -*-

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
# along with EDIS-C.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QGroupBox
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QCheckBox
from PyQt4.QtGui import QComboBox
#from PyQt4.QtGui import QLineEdit
#from PyQt4.QtGui import QLabel
#from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QTabWidget

from edis_c.nucleo import configuraciones
from edis_c.nucleo import comprobar_terminales


class ECTab(QWidget):

    def __init__(self, parent):
        super(ECTab, self).__init__(parent)
        vbox = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.configCompilacion = ConfiguracionCompilacion(self)
        self.configEjecucion = ConfiguracionEjecucion(self)
        self.tabs.addTab(self.configCompilacion,
            self.trUtf8("Compilación"))
        self.tabs.addTab(self.configEjecucion,
            self.trUtf8("Ejecución"))

        vbox.addWidget(self.tabs)

    def guardar(self):
        for i in range(self.tabs.count()):
            self.tabs.widget(i).guardar()


class ConfiguracionCompilacion(QWidget):

    def __init__(self, parent):
        super(ConfiguracionCompilacion, self).__init__(parent)

        layoutV = QVBoxLayout(self)

        grupoCompilacion = QGroupBox(
            self.trUtf8("Opciones de compilación"))

        grilla = QVBoxLayout(grupoCompilacion)

        # Checks parámetros adicionales para el compilador
        self.checkWerror = QCheckBox(
            self.trUtf8("Considerar los warnings como error."))
        self.checkOptimizacion = QCheckBox(self.trUtf8("Optimización:"))
        self.comboOptimizacion = QComboBox()
        self.comboOptimizacion.addItems(['01', 'O2', 'O3', 'Os', 'Og'])
        self.checkEnsamblado = QCheckBox(
            self.trUtf8("Generar código Ensamblador."))
        self.checkEnsamblado.setToolTip(
            self.trUtf8("Se genera un código en lenguaje ensamblador "
            "propio del procesador."))

        grilla.addWidget(self.checkWerror)
        layoutH = QHBoxLayout()
        layoutH.addWidget(self.checkOptimizacion)
        layoutH.addWidget(self.comboOptimizacion)
        grilla.addLayout(layoutH)
        grilla.addWidget(self.checkEnsamblado)

        # Configuraciones
        parametros = list(str(configuraciones.PARAMETROS).split())
        if '-Werror' in parametros:
            self.checkWerror.setChecked(True)
        if str(configuraciones.PARAMETROS).find('-O') > -1:
            self.checkOptimizacion.setChecked(True)
            i = str(configuraciones.PARAMETROS).find('-O')
            op = configuraciones.PARAMETROS[i + 2].split('.', 1)[0]
            i = self.comboOptimizacion.findText(op)
            self.comboOptimizacion.setCurrentIndex(i)
        if '-S' in parametros:
            self.checkEnsamblado.setChecked(True)

        layoutV.addWidget(grupoCompilacion)

    def guardar(self):
        pass


class ConfiguracionEjecucion(QWidget):

    def __init__(self, parent):
        super(ConfiguracionEjecucion, self).__init__(parent)

        layoutV = QVBoxLayout(self)

        grupoEjecucion = QGroupBox(
            self.trUtf8("Opciones de ejecución"))

        grillaE = QVBoxLayout(grupoEjecucion)

        #Ejecución
        layoutPath = QHBoxLayout()
        self.terminales = QComboBox()
        terminales = comprobar_terminales.comprobar()
        for terminal in terminales:
            self.terminales.addItem(terminal)

        layoutPath.addWidget(self.terminales)
        grillaE.addLayout(layoutPath)

        self.checkTiempo = QCheckBox(
            self.trUtf8("Tiempo de ejecución."))

        grillaE.addWidget(self.checkTiempo)

        layoutV.addWidget(grupoEjecucion)

    def cargar_terminal(self):
        path = QFileDialog.getOpenFileName(self,
            self.trUtf8("Seleccione la terminal"))
        if path:
            self.path_terminal.setText(path)

    def guardar(self):
        #print self.terminales.currentIndex()
        #print self.terminales.currentText()
        pass