# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os
import json

from PyQt4.QtGui import (
    QWizard,
    QWizardPage,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QRadioButton,
    QButtonGroup,
    QListWidget,
    QPixmap,
    QFileDialog,
    QMessageBox
    )

from PyQt4.QtCore import (
    SIGNAL,
    Qt
    )

from src.core import (
    paths,
    templates
    )
from src.ui.main import Edis
from src.ui.containers.lateral import edis_project


class NewProjectDialog(QWizard):

    def __init__(self, parent=None):
        QWizard.__init__(self, parent)
        self.data = {}
        self.setWindowTitle(self.tr("New Edis Project"))
        pixmap = QPixmap(":image/edis")
        self.setPixmap(QWizard.LogoPixmap, pixmap.scaled(56, 56,
                       Qt.IgnoreAspectRatio, Qt.FastTransformation))
        # Páginas
        self._intro = IntroductionPage()
        self.addPage(self._intro)
        self._finish = FinishPage()
        self.addPage(self._finish)

        # Posición de botones
        self.setButtonLayout([
            QWizard.BackButton,
            QWizard.Stretch,
            QWizard.NextButton,
            QWizard.FinishButton])

    def done(self, result):
        if result == 0:
            super(NewProjectDialog, self).done(result)
            return
        name = self._intro.line_name.text()
        location = self._intro.line_location.text()
        template = self._finish.template
        full_path = os.path.join(location, name)

        self.data = {
            'name': name,
            'location': location,
            'template': template,
            'path': full_path
            }
        # Objeto EdisProject
        project = edis_project.EdisProject(self.data)
        project.name = name
        # Crea el directorio de proyectos si no existe
        if not os.path.isdir(paths.PROJECT_DIR):
            os.mkdir(paths.PROJECT_DIR)
        if os.path.exists(project.project_path):
            flags = QMessageBox.No | QMessageBox.Yes
            result = QMessageBox.information(self, self.tr("Warning"),
                                             self.tr("The project already "
                                             "exists in that location with "
                                             "that name.\nYou want to replace "
                                             "it?"), flags)
            if result == QMessageBox.No:
                return
            # Elimina los archivos del directorio
            for _file in os.listdir(project.project_path):
                os.remove(os.path.join(project.project_path, _file))
        else:
            os.mkdir(project.project_path)
        # Creo el archivo .epf
        json.dump(self.data, open(project.project_file, "w"))

        editor_container = Edis.get_component("principal")
        if project.template == 1:
            main_file = os.path.join(project.project_path, "main.c")
            with open(main_file, mode='w') as f:
                f.write(templates.MAIN_TEMPLATE)
            # Abro el archivo
            editor_container.open_file(main_file)
        # Cargo el projecto
        editor_container.open_project(project.project_file)
        super(NewProjectDialog, self).done(result)


class IntroductionPage(QWizardPage):

    def __init__(self):
        super(IntroductionPage, self).__init__()
        self.setTitle(self.tr("Creation Project"))
        self.setSubTitle(self.tr("Basic project information"))
        container = QVBoxLayout(self)
        hbox = QHBoxLayout()
        # Nombre
        hbox.addWidget(QLabel(self.tr("Name of the project:")))
        self.line_name = QLineEdit()
        hbox.addWidget(self.line_name)
        container.addLayout(hbox)
        # Ubicación
        group = QGroupBox(self.tr("Location:"))
        box = QVBoxLayout(group)
        button_group = QButtonGroup(self)
        radio_buttons = [
            self.tr("Project folder"),
            self.tr("Other")
            ]
        for _id, radiob in enumerate(radio_buttons):
            radio_button = QRadioButton(radiob)
            button_group.addButton(radio_button, _id)
            box.addWidget(radio_button)
            if _id == 0:
                # El primero checked por defecto
                radio_button.setChecked(True)
        container.addWidget(group)

        self.line_location = QLineEdit()
        container.addWidget(self.line_location)

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(self.tr("Filename: ")))
        self._project_filename = QLineEdit()
        hbox.addWidget(self._project_filename)
        container.addLayout(hbox)

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(self.tr("Resulting filename: ")))
        self._resulting_filename = QLineEdit()
        hbox.addWidget(self._resulting_filename)
        container.addLayout(hbox)

        # Conexiones
        self.connect(button_group, SIGNAL("buttonClicked(int)"),
                     self._update_location)
        self.connect(self.line_name, SIGNAL("textChanged(const QString&)"),
                     self._on_project_name_changed)
        self.connect(self.line_name, SIGNAL("textChanged(const QString&)"),
                     lambda: self.emit(SIGNAL("completeChanged()")))

        self._update_location(0)

    def isComplete(self):
        """ Reimplemetación """

        return len(self.line_name.text()) > 0

    def _update_location(self, button_id):
        if button_id == 0:
            path = paths.PROJECT_DIR
        elif button_id == 2:
            path = QFileDialog.getExistingDirectory(
                self, self.tr("Choose a directory"), os.path.expanduser("~"))
            if not path:
                path = paths.PROJECT_DIR
        self.line_location.setText(path)

    def _on_project_name_changed(self, text):
        found = True if text else False
        project_filename = text + '.epf' if found else ""
        self._project_filename.setText(project_filename)
        resulting_filename = self.line_location.text() + '/' + project_filename
        result = resulting_filename if found else ""
        self._resulting_filename.setText(result)


class FinishPage(QWizardPage):

    def __init__(self):
        super(FinishPage, self).__init__()
        container = QVBoxLayout(self)
        self.setSubTitle(self.tr("Choose a template"))
        self.list_template = QListWidget()
        self.list_template.addItem(self.tr("Blank Project"))
        self.list_template.addItem(self.tr("Include file and main function"))
        container.addWidget(self.list_template)

    @property
    def template(self):
        selection = self.list_template.selectedItems()
        if not selection:
            self.list_template.currentItem().setSelected(True)
        return self.list_template.row(self.list_template.selectedItems()[0])