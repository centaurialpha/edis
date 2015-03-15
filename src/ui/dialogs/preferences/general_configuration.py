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
    QGroupBox,
    QCheckBox,
    QPushButton,
    QMessageBox,
    QSizePolicy,
    QSpacerItem,
    QComboBox
    )

from src import paths
from src.helpers.configurations import ESettings


class GeneralConfiguration(QWidget):

    def __init__(self, parent):
        super(GeneralConfiguration, self).__init__(parent)
        self.parent = parent
        container = QVBoxLayout(self)

        # Inicio
        group_on_start = QGroupBox(self.tr("On start:"))
        box = QVBoxLayout(group_on_start)
        self.check_splash = QCheckBox(self.tr("Show Splash Screen"))
        self.check_splash.setChecked(ESettings.get('general/show-splash'))
        box.addWidget(self.check_splash)
        self.check_on_start = QCheckBox(self.tr("Show Start Page"))
        self.check_on_start.setChecked(ESettings.get('general/show-start-page'))
        box.addWidget(self.check_on_start)
        self.check_load_files = QCheckBox(self.tr("Load files from the last "
                                          "session"))
        self.check_load_files.setChecked(ESettings.get('general/load-files'))
        box.addWidget(self.check_load_files)

        # Al salir
        group_on_exit = QGroupBox(self.tr("On close:"))
        box = QVBoxLayout(group_on_exit)
        self.check_on_exit = QCheckBox(self.tr("Confirm exit"))
        self.check_on_exit.setChecked(
            ESettings.get('general/confirm-exit'))
        box.addWidget(self.check_on_exit)
        self.check_geometry = QCheckBox(self.tr(
            "Save window position and geometry"))
        self.check_geometry.setChecked(
            ESettings.get('ventana/store-size'))
        box.addWidget(self.check_geometry)

        # Notificaciones
        group_notifications = QGroupBox(self.tr("Notifications:"))
        box = QVBoxLayout(group_notifications)
        self.check_updates = QCheckBox(self.tr("Check updates"))
        self.check_updates.setChecked(ESettings.get('general/check-updates'))
        box.addWidget(self.check_updates)

        # Idioma
        group_language = QGroupBox(self.tr("Language:"))
        box = QVBoxLayout(group_language)
        self.combo_lang = QComboBox()
        langs = os.listdir(os.path.join(paths.PATH, "extras", "i18n"))
        self.combo_lang.addItems(["English"] + [lang[:-3] for lang in langs])
        lang = ESettings.get('general/language')
        index = 0 if not lang else self.combo_lang.findText(lang)
        self.combo_lang.setCurrentIndex(index)
        box.addWidget(self.combo_lang)

        # Reestablecer
        group_restart = QGroupBox(self.tr("Restart:"))
        box = QHBoxLayout(group_restart)
        btn_reestablecer = QPushButton(self.tr("Restart Edis configurations"))
        btn_reestablecer.setObjectName("custom")
        box.addWidget(btn_reestablecer)
        box.addStretch(1)

        container.addWidget(group_on_start)
        container.addWidget(group_on_exit)
        container.addWidget(group_notifications)
        container.addWidget(group_language)
        container.addWidget(group_restart)
        container.addItem(QSpacerItem(0, 10, QSizePolicy.Expanding,
                           QSizePolicy.Expanding))
        btn_reestablecer.clicked.connect(self._restart_configurations)

    def _restart_configurations(self):
        flags = QMessageBox.Cancel
        flags |= QMessageBox.Yes

        result = QMessageBox.question(self, self.tr("Warning!"),
                                         self.tr("Are you sure you want to "
                                         "reset your configurations?"), flags)
        if result == QMessageBox.Cancel:
            return
        elif result == QMessageBox.Yes:
            ESettings.clear()
            self.parent.close()

    def guardar(self):
        """ Guarda las configuraciones Generales. """

        ESettings.set('general/show-splash', self.check_splash.isChecked())
        ESettings.set('general/show-start-page',
                      self.check_on_start.isChecked())
        ESettings.set('ventana/store-size',
                      self.check_geometry.isChecked())
        ESettings.set('general/confirm-exit',
                      self.check_on_exit.isChecked())
        ESettings.set('general/check-updates', self.check_updates.isChecked())
        ESettings.set('general/load-files', self.check_load_files.isChecked())
        lang = self.combo_lang.currentText()
        ESettings.set('general/language', lang)