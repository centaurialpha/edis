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
        self.check_wall = QCheckBox(
            self.tr("Enable all common compiler warnings [-Wall]"))
        box.addWidget(self.check_wall, 0, 0)
        self.check_wextra = QCheckBox(
            self.tr("Enable extra compiler warnings [-Wextra]"))
        box.addWidget(self.check_wextra, 0, 1)
        self.check_wfatal_error = QCheckBox(
            self.tr("Stop compiling after first error [-Wfatal-errors]"))
        box.addWidget(self.check_wfatal_error, 1, 0)
        self.check_w = QCheckBox(
            self.tr("Inhibit all warning messages [-w]"))
        box.addWidget(self.check_w, 1, 1)

        group_optimization = QGroupBox(self.tr("Optimization:"))
        box = QGridLayout(group_optimization)
        box.setContentsMargins(20, 5, 20, 5)
        self.check_o = QCheckBox(
            self.tr("Optimize generated code for speed [-O]"))
        box.addWidget(self.check_o, 0, 0)
        self.check_o1 = QCheckBox(
            self.tr("Optimize more for speed [-O1]"))
        box.addWidget(self.check_o1, 0, 1)
        self.check_o2 = QCheckBox(
            self.tr("Optimize even more for speed [-O2]"))
        box.addWidget(self.check_o2, 1, 0)
        self.check_o3 = QCheckBox(
            self.tr("Optimize fully for speed [-O3]"))
        box.addWidget(self.check_o3, 1, 1)
        self.check_os = QCheckBox(
            self.tr("Optimize generated code for size [-Os]"))
        box.addWidget(self.check_os, 2, 0)

        container.addWidget(group_flags)
        container.addWidget(group_optimization)
        container.addItem(QSpacerItem(0, 0,
                          QSizePolicy.Expanding, QSizePolicy.Expanding))

        CompilerConfiguration.install_widget(self.tr("Compiler Flags"), self)

    def save(self):
        pass


compiler_configuration = CompilerConfiguration()