# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os

# Módulos QtGui
from PyQt4.QtGui import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QGroupBox,
    QCheckBox,
    QPushButton,
    QMessageBox,
    QSizePolicy,
    QSpacerItem,
    QComboBox,
    QLineEdit,
    QLabel,
    QTabWidget,
    QApplication
    )

from PyQt4.QtCore import (
    QSettings,
    Qt,
    SIGNAL
    )
from src.core import (
    paths,
    settings
    )


class EnvironmentConfiguration(QTabWidget):

    def __init__(self, parent=None):
        super(EnvironmentConfiguration, self).__init__()
        self.parent = parent
        self.general_section = GeneralSection()
        self.addTab(self.general_section, self.tr("General"))
        self.shortcut_section = ShortcutSection()
        self.addTab(self.shortcut_section, self.tr("Shortcuts"))

    def guardar(self):
        pass


class GeneralSection(QWidget):

    def __init__(self):
        super(GeneralSection, self).__init__()
        container = QVBoxLayout(self)

        # Inicio
        group_on_start = QGroupBox(self.tr("On start:"))
        box = QVBoxLayout(group_on_start)
        self.check_splash = QCheckBox(self.tr("Show Splash Screen"))
        self.check_splash.setChecked(
            settings.get_setting('general/show-splash'))
        box.addWidget(self.check_splash)
        self.check_on_start = QCheckBox(self.tr("Show Start Page"))
        show_start_page = settings.get_setting('general/show-start-page')
        self.check_on_start.setChecked(show_start_page)
        box.addWidget(self.check_on_start)
        self.check_load_files = QCheckBox(self.tr("Load files from the last "
                                          "session"))
        load_files = settings.get_setting('general/load-files')
        self.check_load_files.setChecked(load_files)
        box.addWidget(self.check_load_files)
        container.addWidget(group_on_start)

        # Al salir
        group_on_exit = QGroupBox(self.tr("On close:"))
        box = QVBoxLayout(group_on_exit)
        self.check_on_exit = QCheckBox(self.tr("Confirm exit"))
        self.check_on_exit.setChecked(
            settings.get_setting('general/confirm-exit'))
        box.addWidget(self.check_on_exit)
        self.check_geometry = QCheckBox(self.tr(
            "Save window position and geometry"))
        self.check_geometry.setChecked(
            settings.get_setting('window/store-size'))
        box.addWidget(self.check_geometry)
        container.addWidget(group_on_exit)

        # Notificaciones
        group_notifications = QGroupBox(self.tr("Notifications:"))
        box = QVBoxLayout(group_notifications)
        self.check_updates = QCheckBox(self.tr("Check updates"))
        self.check_updates.setChecked(
            settings.get_setting('general/check-updates'))
        box.addWidget(self.check_updates)
        container.addWidget(group_notifications)

        # Sistema
        if settings.IS_LINUX:
            group_terminal = QGroupBox(self.tr("System:"))
            box = QHBoxLayout(group_terminal)
            box.addWidget(QLabel(self.tr("Execute program with:")))
            self.line_terminal = QLineEdit()
            self.line_terminal.setAlignment(Qt.AlignLeft)
            self.line_terminal.setFixedWidth(300)
            self.line_terminal.setText(settings.get_setting('terminal'))
            box.addWidget(self.line_terminal, 1, Qt.AlignLeft)
            container.addWidget(group_terminal)

        # User Interface
        group_ui = QGroupBox(self.tr("User Interface:"))
        box = QGridLayout(group_ui)
        box.addWidget(QLabel(self.tr("Theme:")), 0, 0)
        self.combo_theme = QComboBox()
        self.combo_theme.setFixedWidth(200)
        self._update_combo()
        index = self.combo_theme.findText(
            settings.get_setting('window/style-sheet'))
        self.combo_theme.setCurrentIndex(index)
        box.addWidget(self.combo_theme, 0, 1)

        self.combo_lang = QComboBox()
        self.combo_lang.setFixedWidth(200)
        box.addWidget(QLabel(self.tr("Language:")), 1, 0)
        box.addWidget(self.combo_lang, 1, 1)
        langs = os.listdir(os.path.join(paths.PATH, "extras", "i18n"))
        self.combo_lang.addItems(["English"] + [lang[:-3] for lang in langs])
        lang = settings.get_setting('general/language')
        index = 0 if not lang else self.combo_lang.findText(lang)
        self.combo_lang.setCurrentIndex(index)
        container.addWidget(group_ui)
        box.setAlignment(Qt.AlignLeft)

        # Reestablecer
        group_restart = QGroupBox(self.tr("Restart:"))
        box = QHBoxLayout(group_restart)
        btn_restart = QPushButton(self.tr("Restart Edis configurations"))
        btn_restart.setObjectName("custom")
        box.addWidget(btn_restart)
        box.addStretch(1)
        container.addWidget(group_restart)

        container.addItem(QSpacerItem(0, 0,
                          QSizePolicy.Expanding, QSizePolicy.Expanding))

        # Conexiones
        self.connect(btn_restart, SIGNAL("clicked()"),
                     self._restart_configurations)
        self.connect(self.combo_theme, SIGNAL("currentIndexChanged(int)"),
                     self._change_style_sheet)

    def _update_combo(self):
        self.combo_theme.addItems(['Default', 'Edark'])
        list_dir = os.listdir(paths.EDIS)
        list_styles = [i.split('.')[0]for i
                       in list_dir
                       if os.path.splitext(i)[-1] == '.qss']
        self.combo_theme.insertItems(2, list_styles)

    def _change_style_sheet(self, index):
        style_sheet = None
        path = None
        if index == 1:
            path = os.path.join(paths.PATH, "extras",
                                "theme", "edark.qss")
        elif index != 0:
            style = self.combo_styles.currentText() + '.qss'
            path = os.path.join(paths.EDIS, style)
        if path is not None:
            with open(path, mode='r') as f:
                style_sheet = f.read()
        QApplication.instance().setStyleSheet(style_sheet)

    def _restart_configurations(self):
        flags = QMessageBox.Cancel
        flags |= QMessageBox.Yes

        result = QMessageBox.question(self, self.tr("Warning!"),
                                      self.tr("Are you sure you want to "
                                              "reset your configurations?"),
                                      flags)
        if result == QMessageBox.Cancel:
            return
        elif result == QMessageBox.Yes:
            QSettings(paths.CONFIGURACION, QSettings.IniFormat).clear()
        #FIXME: cerrar dialogo

    #def guardar(self):
        #""" Guarda las configuraciones Generales. """

        #settings.set_setting('general/show-splash',
                             #self.check_splash.isChecked())
        #show_start_page = self.check_on_start.isChecked()
        #settings.set_setting('general/show-start-page', show_start_page)
        #settings.set_setting('ventana/store-size',
                             #self.check_geometry.isChecked())
        #settings.set_setting('general/confirm-exit',
                             #self.check_on_exit.isChecked())
        #settings.set_setting('general/check-updates',
                             #self.check_updates.isChecked())
        #load_files = self.check_load_files.isChecked()
        #settings.set_setting('general/load-files', load_files)
        #lang = self.combo_lang.currentText()
        #settings.set_setting('general/language', lang)
        #if settings.IS_LINUX:
            #settings.set_setting('terminal', self.line_terminal.text())
#


class ShortcutSection(QWidget):

    def __init__(self):
        super(ShortcutSection, self).__init__()
