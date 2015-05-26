# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from collections import OrderedDict

from PyQt4.QtGui import (
    QTabWidget,
    QGroupBox,
    QVBoxLayout,
    QGridLayout,
    QCheckBox,
    QWidget,
    QSpacerItem,
    QSizePolicy
    )

from src.ui.main import Edis
from src.core import settings


class CompilerConfiguration(QTabWidget):

    __TABS = OrderedDict()

    def __init__(self):
        super(CompilerConfiguration, self).__init__()
        self.flags = FlagsSection()
        preferences = Edis.get_component("preferences")
        preferences.install_section(self)

    @classmethod
    def install_widget(cls, name, obj):
        cls.__TABS[name] = obj

    def get_tabs(self):
        return self.__TABS

    def install_tab(self, obj, name):
        self.addTab(obj, name)

    def save(self):
        for index in range(self.count()):
            self.widget(index).save()


class FlagsSection(QWidget):

    def __init__(self):
        super(FlagsSection, self).__init__()
        container = QVBoxLayout(self)

        group_flags = QGroupBox(self.tr("Flags:"))
        box = QGridLayout(group_flags)
        box.setContentsMargins(20, 5, 20, 5)
        compiler_flags = settings.COMPILER_FLAGS.split()
        # -Wall
        self.check_wall = QCheckBox(
            self.tr("Habilitar todas las advertencias comunes [-Wall]"))
        if '-Wall' in compiler_flags:
            self.check_wall.setChecked(True)
        box.addWidget(self.check_wall, 0, 0)
        # -Wextra
        self.check_wextra = QCheckBox(
            self.tr("Habilitar advertencias extras [-Wextra]"))
        if '-Wextra' in compiler_flags:
            self.check_wextra.setChecked(True)
        box.addWidget(self.check_wextra, 0, 1)
        # -Wfatal-errors
        self.check_wfatal_error = QCheckBox(
            self.tr("Frenar compilación después del primer error "
                    "[-Wfatal-errors]"))
        if '-Wfatal-erros' in compiler_flags:
            self.check_wfatal_error.setChecked(True)
        box.addWidget(self.check_wfatal_error, 1, 0)
        # -w
        self.check_w = QCheckBox(
            self.tr("Inhibir todos los mensajes de advertencia [-w]"))
        if '-w' in compiler_flags:
            self.check_w.setChecked(True)
        box.addWidget(self.check_w, 1, 1)

        group_optimization = QGroupBox(self.tr("Optimización:"))
        box = QGridLayout(group_optimization)
        box.setContentsMargins(20, 5, 20, 5)
        # -O
        self.check_o = QCheckBox(
            self.tr("Optimizar código para velocidad [-O]"))
        if '-O' in compiler_flags:
            self.check_o.setChecked(True)
        box.addWidget(self.check_o, 0, 0)
        # -O1
        self.check_o1 = QCheckBox(
            self.tr("Optimizar más el código para velocidad [-O1]"))
        if '-O1' in compiler_flags:
            self.check_o1.setChecked(True)
        box.addWidget(self.check_o1, 0, 1)
        # -O2
        self.check_o2 = QCheckBox(
            self.tr("Optimizar aún más el código para velocidad [-O2]"))
        if '-O2' in compiler_flags:
            self.check_o2.setChecked(True)
        box.addWidget(self.check_o2, 1, 0)
        # -O3
        self.check_o3 = QCheckBox(
            self.tr("Optimizar totalmente el código para velocidad [-O3]"))
        if '-O3' in compiler_flags:
            self.check_o3.setChecked(True)
        box.addWidget(self.check_o3, 1, 1)
        # -Os
        self.check_os = QCheckBox(
            self.tr("Optimizar el código para tamaño [-Os]"))
        if '-Os' in compiler_flags:
            self.check_os.setChecked(True)
        box.addWidget(self.check_os, 2, 0)

        container.addWidget(group_flags)
        container.addWidget(group_optimization)
        container.addItem(QSpacerItem(0, 0,
                          QSizePolicy.Expanding, QSizePolicy.Expanding))

        CompilerConfiguration.install_widget(
            self.tr("Opciones del Compilador"), self)

    def save(self):
        """  Se guardan los parámetros adicionales para el compilador.
        NOTA: no persisten en una nueva sesión, es decir, no se guardan
        en el archivo de configuración. """

        for setting in dir(self):
            if setting.startswith('check'):
                atr = getattr(self, setting)
                if atr.isChecked():
                    flag = atr.text().split('[')[-1][:-1]
                    if flag not in settings.COMPILER_FLAGS:
                        settings.COMPILER_FLAGS += ' ' + flag


compiler_configuration = CompilerConfiguration()