# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import sys

# Módulos QtGui
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QGroupBox
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QCheckBox
from PyQt4.QtGui import QComboBox
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QSizePolicy
from PyQt4.QtGui import QSpacerItem
from PyQt4.QtGui import QTabWidget
from PyQt4.QtGui import QRadioButton

# Módulos QtCore
from PyQt4.QtCore import (
    QSettings,
    )

# Módulos EDIS
from src import recursos
from src.helpers import configuraciones
from src.helpers import comprobar_terminales


class ECTab(QWidget):

    def __init__(self, parent):
        super(ECTab, self).__init__(parent)
        vbox = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(3)
        self.configCompilacion = ConfiguracionCompilacion(self)
        self.configEjecucion = ConfiguracionEjecucion(self)
        self.tabs.addTab(self.configCompilacion, self.trUtf8("Compilación"))
        self.tabs.addTab(self.configEjecucion, self.trUtf8("Ejecución"))

        vbox.addWidget(self.tabs)

    def guardar(self):
        for i in range(self.tabs.count()):
            self.tabs.widget(i).guardar()


class ConfiguracionCompilacion(QWidget):

    def __init__(self, parent):
        super(ConfiguracionCompilacion, self).__init__(parent)

        layoutV = QVBoxLayout(self)

        grupoCompilacion = QGroupBox(
            self.trUtf8("Opciones de compilación:"))

        grilla = QVBoxLayout(grupoCompilacion)

        # Checks parámetros adicionales para el compilador
        self.checkWerror = QCheckBox(
            self.trUtf8("Considerar los warnings como error."))
        self.checkOptimizacion = QCheckBox(self.trUtf8("Optimización:"))
        self.comboOptimizacion = QComboBox()
        self.comboOptimizacion.setEnabled(False)
        self.comboOptimizacion.addItems(['01', 'O2', 'O3', 'Os', 'Og'])
        self.checkEnsamblado = QCheckBox(
            self.trUtf8("Generar código Ensamblador."))
        self.checkEnsamblado.setToolTip(
            self.trUtf8("Se genera un código en lenguaje ensamblador "
                        "propio del procesador."))
        self.checkOptimizacion.toggled.connect(
            self.comboOptimizacion.setEnabled)

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
        layoutV.addItem(QSpacerItem(10, 0, QSizePolicy.Expanding,
                        QSizePolicy.Expanding))

    def guardar(self):
        qconfig = QSettings(recursos.CONFIGURACION, QSettings.IniFormat)
        qconfig.beginGroup('configuraciones')
        parametros = ''
        if self.checkEnsamblado.isChecked():
            parametros += ' -S'
        configuraciones.PARAMETROS = parametros
        qconfig.setValue('compilacion', parametros)
        qconfig.endGroup()


class ConfiguracionEjecucion(QWidget):

    def __init__(self, parent):
        super(ConfiguracionEjecucion, self).__init__(parent)

        self.layoutV = QVBoxLayout(self)
        self.check_terminal()

        self.layoutV.addItem(QSpacerItem(0, 10, QSizePolicy.Expanding,
                             QSizePolicy.Expanding))

    def check_terminal(self):
        if sys.platform != 'linux2':
            return

        grupoEjecucion = QGroupBox(
            self.trUtf8("Terminales disponibles:"))
        layout_radio = QVBoxLayout()
        grillaE = QVBoxLayout(grupoEjecucion)
        self.terminales_radio = []
        terminales = comprobar_terminales.comprobar()
        for terminal in terminales:
            self.terminales_radio.append(QRadioButton(terminal))

        b = False
        for i in self.terminales_radio:
            layout_radio.addWidget(i)
            if i.text() == configuraciones.TERMINAL:
                i.setChecked(True)
                b = True
        if not b:
            QMessageBox.warning(self, self.tr("Advertencia!"), self.trUtf8(
                "No se ha seleccionado una terminal para la ejecución!"))
        grillaE.addLayout(layout_radio)
        self.layoutV.addWidget(grupoEjecucion)

    def guardar(self):
        qconfig = QSettings(recursos.CONFIGURACION, QSettings.IniFormat)
        terminal = ""
        for i in self.terminales_radio:
            if i.isChecked():
                terminal = i.text()
        qconfig.setValue('configuraciones/ejecucion/terminal', terminal)
        configuraciones.TERMINAL = terminal