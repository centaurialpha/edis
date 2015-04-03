# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os

from PyQt4.QtGui import (
    QTreeWidget,
    QTreeWidgetItem,
    QMenu,
    QMessageBox,
    QDialog,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QPushButton,
    QInputDialog
    )

from PyQt4.QtCore import (
    SIGNAL,
    Qt
    )

from src.ui.main import Edis


class TreeProject(QTreeWidget):

    def __init__(self):
        super(TreeProject, self).__init__()

        # Lista de fuentes, para la compilación
        self._sources = []

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.connect(self, SIGNAL("customContextMenuRequested(const QPoint &)"),
                     self._menu_tree_project)
        self.connect(self, SIGNAL("itemDoubleClicked(QTreeWidgetItem*, int)"),
                     self._open_file)

        Edis.load_lateral("tree_projects", self)

    def _open_file(self, item, column):
        if item.isClickeable and not item.isFolder:
            filename = item.path
            editor_container = Edis.get_component("principal")
            editor_container.open_file(filename)

    def _menu_tree_project(self, point):
        item = self.itemAt(point)
        if item is None:
            return
        if not item.isRoot:
            if not item.isFolder:
                self._load_menu_for_file(point)
            else:
                self._load_menu_for_folder(point)
        else:
            if item.isEdisProject:
                self._load_menu_for_edis_project(point)
            else:
                self._load_menu_for_root(point)

    def _load_menu_for_root(self, point):
        menu = QMenu(self)
        create_file_action = menu.addAction(self.tr("Create a file"))
        create_folder_action = menu.addAction(self.tr("Create a folder"))
        menu.addSeparator()
        close_project_action = menu.addAction(self.tr("Close project"))

        # Conexiones
        self.connect(create_file_action, SIGNAL("triggered()"),
                     self._create_file)
        self.connect(create_folder_action, SIGNAL("triggered()"),
                    self._create_folder)
        self.connect(close_project_action, SIGNAL("triggered()"),
                    self._close_project)

        menu.exec_(self.mapToGlobal(point))

    def _load_menu_for_file(self, point):
        menu = QMenu(self)
        delete_action = menu.addAction(self.tr("Delete file"))

        self.connect(delete_action, SIGNAL("triggered()"), self._delete_file)
        menu.exec_(self.mapToGlobal(point))

    def _load_menu_for_folder(self, point):
        menu = QMenu(self)
        create_file_action = menu.addAction(self.tr("Create a file"))
        create_folder_action = menu.addAction(self.tr("Create a folder"))
        menu.addSeparator()
        delete_folder_action = menu.addAction(self.tr("Delete folder"))

        # Conexiones
        self.connect(create_file_action, SIGNAL("triggered()"),
                     self._create_file)
        self.connect(create_folder_action, SIGNAL("triggered()"),
                     self._create_folder)
        self.connect(delete_folder_action, SIGNAL("triggered()"),
                    self._delete_folder)

        menu.exec_(self.mapToGlobal(point))

    def _load_menu_for_edis_project(self, point):
        menu = QMenu(self)
        create_file_action = menu.addAction(self.tr("Create source file"))

        # Conexiones
        self.connect(create_file_action, SIGNAL("triggered()"),
                     self._create_file)

        menu.exec_(self.mapToGlobal(point))

    def _create_file(self):
        dialog = NewFileDialog(self)
        data = dialog.data
        if data:
            current_item = self.currentItem()
            filename, ftype = data['filename'], data['type']
            filename = os.path.join(current_item.path, filename)
            # Agrego a la lista de archivos fuente
            self._sources.append(filename)
            if ftype == 1:
                # Header file
                preprocessor = os.path.splitext(os.path.basename(filename))[0]
                content = "#ifndef %s_H_\n#define %s_H_" % \
                          (preprocessor.upper(), preprocessor.upper())
            else:
                content = ""
            with open(filename, mode='w') as f:
                f.write(content)
            if current_item.isEdisProject:
                parent = current_item.child(ftype)
            else:
                parent = current_item
            new_item = ItemTree(parent, [data['filename']])
            new_item.path = filename

    def _create_folder(self):
        current_item = self.currentItem()
        folder_name = QInputDialog.getText(self, self.tr("New folder"),
                                           self.tr("Name:"))
        folder_item = ItemTree(current_item, [folder_name[0]])
        folder_item.path = os.path.join(current_item.path, folder_name[0])
        folder_item.isFolder = True
        folder_item.isEdisProject = False
        folder_item.setExpanded(True)

    def _delete_folder(self):
        current_item = self.currentItem()
        # Elimino el item del árbol
        index = current_item.parent().indexOfChild(current_item)
        current_item.parent().takeChild(index)

    def _delete_file(self):
        """ Borra fisicamente el archivo y lo quita del árbol """

        current_item = self.currentItem()
        # Flags
        yes = QMessageBox.Yes
        no = QMessageBox.No
        result = QMessageBox.warning(self, self.tr("Warning"),
                                     self.tr("Are you sure you want to delete "
                                     "the file?<br><br><b>{0}</b>").format(
                                      current_item.path), no | yes)
        if result == no:
            return
        # Borro el archivo
        os.remove(current_item.path)
        # Elimino el item del árbol
        index = current_item.parent().indexOfChild(current_item)
        current_item.parent().takeChild(index)
        # Elimino el item de la lista de fuentes
        self._sources.remove(current_item.path)

    def open_project(self, data):
        # Parent
        structure, root, edis_project = data
        root_basename = os.path.basename(root)
        parent = ItemTree(self, [root_basename])
        parent.isClickeable = False
        parent.path = root
        parent.isRoot = True
        if not edis_project:
            parent.isEdisProject = False
        parent.setToolTip(0, root)
        self._load_tree(structure, parent, root, edis_project)
        parent.setExpanded(True)

    def _load_tree(self, structure, parent, root, edis_project):
        """ Crea el árbol del proyecto. Si no es un proyecto de Edis
            el árbol se crea de forma recursiva generando la estructura de
            archivos y directorios.
        """

        files, folders = structure.get(root)
        if not edis_project:
            if files is not None:
                for _file in sorted(files):
                    file_item = ItemTree(parent, [_file])
                    file_item.isEdisProject = False
                    file_item.path = os.path.join(root, _file)
                    file_item.setToolTip(0, _file)
            if folders is not None:
                for folder in sorted(folders):
                    folder_item = ItemTree(parent, [folder])
                    folder_item.isFolder = True
                    folder_item.isEdisProject = False
                    folder_item.path = os.path.join(root, folder)
                    folder_item.setToolTip(0, folder)
                    folder_item.setExpanded(True)
                    self._load_tree(structure, folder_item,
                                    os.path.join(root, folder), edis_project)
        else:
            sources_item = ItemTree(parent, [self.tr("Sources")])
            sources_item.isClickeable = False
            sources_item.setToolTip(0, self.tr("Source files"))
            sources_item.setExpanded(True)
            headers_item = ItemTree(parent, [self.tr("Headers")])
            headers_item.isClickeable = False
            headers_item.setToolTip(0, self.tr("Header files"))
            headers_item.setExpanded(True)
            # FIXME: mejorar
            if files is not None:
                for _file in sorted(files):
                    if os.path.splitext(_file)[-1] == '.c':
                        source_item = ItemTree(sources_item, [_file])
                        source_item.path = os.path.join(root, _file)
                        self._sources.append(source_item.path)
                        source_item.setToolTip(0, _file)
                    else:
                        header_item = ItemTree(headers_item, [_file])
                        header_item.setToolTip(0, _file)
                        header_item.path = os.path.join(root, _file)
                        self._sources.append(header_item.path)

    def _close_project(self):
        pass

    @property
    def sources(self):
        return self._sources


class ItemTree(QTreeWidgetItem):

    def __init__(self, parent, name):
        super(ItemTree, self).__init__(parent, name)
        self.isEdisProject = True
        self.isClickeable = True
        self.isRoot = False
        self.isFolder = False
        self._path = ''

    def __set_path(self, path):
        self._path = path

    def __get_path(self):
        return self._path

    path = property(__get_path, __set_path)


class NewFileDialog(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle(self.tr("New file"))
        self._data = {}
        container = QVBoxLayout(self)
        # Filename
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(self.tr("Name:")))
        self._line_filename = QLineEdit()
        hbox.addWidget(self._line_filename)
        container.addLayout(hbox)
        # Type
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(self.tr("Type:")))
        self._combo_type = QComboBox()
        self._combo_type.addItems([
            self.tr("Source file"),
            self.tr("Header file")
            ])
        hbox.addWidget(self._combo_type)
        container.addLayout(hbox)
        # Buttons
        hbox = QHBoxLayout()
        btn_ok = QPushButton(self.tr("Ok"))
        hbox.addWidget(btn_ok)
        btn_cancel = QPushButton(self.tr("Cancel"))
        hbox.addWidget(btn_cancel)
        container.addLayout(hbox)

        # Conexiones
        self.connect(btn_ok, SIGNAL("clicked()"), self._save_data)
        self.connect(btn_cancel, SIGNAL("clicked()"), self.close)

        self.exec_()

    def _save_data(self):
        filename = self._line_filename.text()
        file_type = self._combo_type.currentIndex()
        if file_type == 0:
            filename += '.c'
        else:
            filename += '.h'
        self._data = {'filename': filename, 'type': file_type}
        self.close()

    @property
    def data(self):
        return self._data


tree_project = TreeProject()