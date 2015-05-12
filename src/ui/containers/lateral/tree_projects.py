# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os

from PyQt4.QtGui import (
    QTreeWidget,
    QTreeWidgetItem,
    QHeaderView,
    QMenu,
    QMessageBox,
    QDialog,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QPushButton,
    QInputDialog,
    QIcon
    )

from PyQt4.QtCore import (
    SIGNAL,
    Qt
    )

from src.ui.main import Edis
from src.core import (
    logger,
    templates,
    exceptions
    )
from src.managers import file_manager

log = logger.get_logger(__name__)
DEBUG = log.debug
ERROR = log.error


class TreeProject(QTreeWidget):

    def __init__(self):
        QTreeWidget.__init__(self)
        # Configuración QTreeWidget
        self.setAnimated(True)
        self.header().setStretchLastSection(False)
        self.header().setHidden(True)
        self.header().setResizeMode(0, QHeaderView.ResizeToContents)
        # Lista de fuentes, para la compilación
        self._sources = []
        # Proyectos abiertos
        self._projects = []

        self.setContextMenuPolicy(Qt.CustomContextMenu)

        # Conexiones
        self.connect(self, SIGNAL("customContextMenuRequested(const QPoint &)"),
                     self._menu_tree_project)
        self.connect(self, SIGNAL("itemDoubleClicked(QTreeWidgetItem*, int)"),
                     self._open_file)

        Edis.load_lateral("tree_projects", self)

    def _open_file(self, item, column):
        if item.isFile:
            filename = item.path
            editor_container = Edis.get_component("principal")
            editor_container.open_file(filename)

    def _menu_tree_project(self, point):
        item = self.itemAt(point)
        if item is None:
            return
        if isinstance(item, EdisItem):
            if item.isRoot:
                self._load_menu_for_edis_project(point)
            else:
                if item.isFile:
                    self._load_menu_for_file(point)
        else:
            if item.isRoot:
                self._load_menu_for_root(point)
            else:
                if not item.isFile:
                    self._load_menu_for_folder(point)
                    return
                self._load_menu_for_file(point)

    def _load_menu_for_root(self, point):
        """ Carga el menú para el root """

        menu = QMenu(self)
        create_file_action = menu.addAction(QIcon(":image/add"),
                                            self.tr("Add File"))
        create_folder_action = menu.addAction(QIcon(":image/new-folder"),
                                              self.tr("Add Folder"))
        menu.addSeparator()
        refresh_project_action = menu.addAction(QIcon(":image/reload"),
                                                self.tr("Refresh Project"))
        close_project_action = menu.addAction(QIcon(":image/exit"),
                                              self.tr("Close Project"))

        # Conexiones
        self.connect(create_file_action, SIGNAL("triggered()"),
                     self._create_file)
        self.connect(create_folder_action, SIGNAL("triggered()"),
                    self._create_folder)
        self.connect(refresh_project_action, SIGNAL("triggered()"),
                     self._refresh_project)
        self.connect(close_project_action, SIGNAL("triggered()"),
                    self._close_project)

        menu.exec_(self.mapToGlobal(point))

    def _load_menu_for_file(self, point):
        """ Carga el menú para un ítem archivo """

        menu = QMenu(self)
        rename_action = menu.addAction(QIcon(":image/rename"),
                                       self.tr("Rename File"))
        delete_action = menu.addAction(QIcon(":image/remove"),
                                       self.tr("Delete File"))

        self.connect(rename_action, SIGNAL("triggered()"),
                     self._rename_file)
        self.connect(delete_action, SIGNAL("triggered()"), self._delete_file)

        menu.exec_(self.mapToGlobal(point))

    def _load_menu_for_folder(self, point):
        """ Carga el menú para un ítem carpeta """

        menu = QMenu(self)
        create_file_action = menu.addAction(QIcon(":image/add"),
                                            self.tr("Add File"))
        create_folder_action = menu.addAction(QIcon(":image/new-folder"),
                                              self.tr("Add Folder"))
        menu.addSeparator()
        delete_folder_action = menu.addAction(QIcon(":image/remove"),
                                              self.tr("Delete Folder"))

        # Conexiones
        self.connect(create_file_action, SIGNAL("triggered()"),
                     self._create_file)
        self.connect(create_folder_action, SIGNAL("triggered()"),
                     self._create_folder)
        self.connect(delete_folder_action, SIGNAL("triggered()"),
                    self._delete_folder)

        menu.exec_(self.mapToGlobal(point))

    def _load_menu_for_edis_project(self, point):
        """ Carga el menú para el root (proyecto de Edis) """

        menu = QMenu(self)
        create_file_action = menu.addAction(QIcon(":image/add"),
                                            self.tr("Add file"))
        create_main_file_action = menu.addAction(self.tr("Add Main File"))
        menu.addSeparator()
        build_project_action = menu.addAction(QIcon(":image/build"),
                                              self.tr("Build Project"))
        clean_project_action = menu.addAction(self.tr("Clean"))
        menu.addSeparator()
        properties_action = menu.addAction(self.tr("Project Properties"))
        menu.addSeparator()
        close_project_action = menu.addAction(QIcon(":image/exit"),
                                              self.tr("Close Project"))

        # Conexiones
        self.connect(create_file_action, SIGNAL("triggered()"),
                     self._create_file)
        self.connect(create_main_file_action, SIGNAL("triggered()"),
                     self._create_main_file)
        self.connect(build_project_action, SIGNAL("triggered()"),
                     self._build_project)
        self.connect(clean_project_action, SIGNAL("triggered()"),
                     self._clean_project)
        self.connect(properties_action, SIGNAL("triggered()"),
                     self._project_properties)
        self.connect(close_project_action, SIGNAL("triggered()"),
                     self._close_project)

        menu.exec_(self.mapToGlobal(point))

    def _clean_project(self):
        pass

    def _refresh_project(self):
        pass

    def _project_properties(self):
        pass

    def _build_project(self):
        editor_container = Edis.get_component("principal")
        editor_container.build_source_code()

    def _create_main_file(self):
        """ Crea el archivo y la función main y lo agrega al árbol"""

        DEBUG("Creating main file...")
        current_item = self.currentItem()
        item_path = os.path.join(current_item.path, 'main.c')
        if os.path.exists(item_path):
            # El archivo ya existe
            QMessageBox.information(self, self.tr("Information"),
                                    self.tr("The <b>main.c</b> file already "
                                    "exists."), QMessageBox.Yes)
            DEBUG("File aready exists...")
            return
        # Creo el archivo
        file_manager.write_file(item_path, templates.MAIN_TEMPLATE)
        # Agrego el ítem, 0 = sources_item
        item = TreeItem(current_item.child(0), ['main.c'])
        item.path = item_path
        self._sources.append(item_path)
        # Abro el archivo
        editor_container = Edis.get_component("principal")
        editor_container.open_file(item_path)

    def _create_file(self):
        DEBUG("Creating a file...")
        dialog = NewFileDialog(self)
        data = dialog.data
        if data:
            current_item = self.currentItem()
            filename, ftype = data['filename'], data['type']
            filename = os.path.join(current_item.path, filename)
            if os.path.exists(filename):
                # El archivo ya existe
                QMessageBox.information(self, self.tr("Information"),
                                        self.tr("A file already exists with "
                                        "that name"), QMessageBox.Ok)
                DEBUG("A file already exists...")
                return
            if ftype == 1:
                # Header file
                preprocessor = os.path.splitext(os.path.basename(filename))[0]
                content = "#ifndef %s_H_\n#define %s_H\n\n#endif" % \
                          (preprocessor.upper(), preprocessor.upper())
            else:
                content = ""
                # Agrego a la lista de archivos fuente
                self._sources.append(filename)
            # Creo el archivo
            file_manager.write_file(filename, content)
            if isinstance(current_item, EdisItem):
                parent = current_item.child(ftype)
            else:
                parent = current_item
            # Agrego el ítem al árbol
            new_item = TreeItem(parent, [data['filename']])
            new_item.path = filename
            editor_container = Edis.get_component("principal")
            editor_container.open_file(filename)

    def _create_folder(self):
        DEBUG("Creating a folder...")
        current_item = self.currentItem()
        qinput = QInputDialog(self)
        qinput.setInputMode(QInputDialog.TextInput)
        qinput.setWindowTitle(self.tr("New folder"))
        qinput.setLabelText(self.tr("Name:"))
        qinput.resize(400, 100)
        ok = qinput.exec_()
        folder_name = qinput.textValue()
        if ok:
            path = os.path.join(current_item.path, folder_name)
            if os.path.exists(path):
                QMessageBox.information(self, self.tr("Information"),
                                        self.tr("The folder already exists"),
                                        QMessageBox.Yes)
                DEBUG("The folder already exists...")
                return
            # Creo la carpeta
            os.mkdir(path)
            # Agrego el ítem al árbol
            folder_item = TreeItem(current_item, [folder_name])
            folder_item.path = path
            folder_item.isFile = False
            folder_item.setExpanded(True)

    def _delete_folder(self):
        DEBUG("Deleting folder...")
        current_item = self.currentItem()
        # Elimino el item del árbol
        index = current_item.parent().indexOfChild(current_item)
        current_item.parent().takeChild(index)

    def _rename_file(self):
        """ Renombra un archivo """

        DEBUG("Renaming file...")
        current_item = self.currentItem()
        name, ok = QInputDialog.getText(self, self.tr("Rename file"),
                                        self.tr("New name:"),
                                        text=current_item.text(0))
        if ok:
            path = os.path.dirname(current_item.path)
            new_name = os.path.join(path, name)
            try:
                # Rename
                file_manager.rename_file(current_item.path, new_name)
                # FIXME: cambiar nombre en combo
                name = file_manager.get_basename(new_name)
                if isinstance(current_item, EdisItem):
                    new_item = EdisItem(current_item.parent(), [name])
                else:
                    new_item = TreeItem(current_item.parent(), [name])
                new_item.setToolTip(0, new_name)
                new_item.path = new_name
                index = current_item.parent().indexOfChild(current_item)
                new_item.parent().takeChild(index)
            except exceptions.EdisFileExistsError as reason:
                ERROR("The file already exists: {0}".format(reason.filename))
                QMessageBox.critical(self, self.tr("Error"),
                                     self.tr("The file already exists"))

    def _delete_file(self):
        """ Borra fisicamente el archivo y lo quita del árbol """

        DEBUG("Deleting file...")
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
        # Elimino el item de la lista de fuentes
        self._sources.remove(current_item.path)
        # Cierro el archivo del editor
        editor_container = Edis.get_component("principal")
        editor_container.close_file_from_project(current_item.path)
        # Elimino el item del árbol
        index = current_item.parent().indexOfChild(current_item)
        current_item.parent().takeChild(index)
        # Borro el archivo fisicamente
        os.remove(current_item.path)

    def open_project(self, data):
        structure, root, edis_project, epf_file = data
        #FIXME:esto cuando no se encuentra el proyecto (fué borrado)
        if not structure:
            return
        self._projects.append(epf_file)
        root_basename = os.path.basename(root)
        if edis_project:
            parent = EdisItem(self, [root_basename])
        else:
            parent = TreeItem(self, [root_basename])
        parent.do_root()
        parent.path = root
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
                    file_item = TreeItem(parent, [_file])
                    file_item.path = os.path.join(root, _file)
                    file_item.setToolTip(0, _file)
            if folders is not None:
                for folder in sorted(folders):
                    folder_item = TreeItem(parent, [folder])
                    folder_item.isFile = False
                    folder_item.path = os.path.join(root, folder)
                    folder_item.setToolTip(0, folder)
                    folder_item.setExpanded(True)
                    self._load_tree(structure, folder_item,
                                    os.path.join(root, folder), edis_project)
        else:
            sources_item = EdisItem(parent, [self.tr("Sources")])
            sources_item.do_edis_item()
            sources_item.setToolTip(0, self.tr("Source files"))
            sources_item.setExpanded(True)
            headers_item = EdisItem(parent, [self.tr("Headers")])
            headers_item.do_edis_item()
            headers_item.setToolTip(0, self.tr("Header files"))
            headers_item.setExpanded(True)
            if files is not None:
                for _file in sorted(files):
                    if os.path.splitext(_file)[-1] == '.c':
                        source_item = EdisItem(sources_item, [_file])
                        source_item.path = os.path.join(root, _file)
                        self._sources.append(source_item.path)
                        source_item.setToolTip(0, _file)
                    else:
                        header_item = EdisItem(headers_item, [_file])
                        header_item.setToolTip(0, _file)
                        header_item.path = os.path.join(root, _file)
                        self._sources.append(header_item.path)

    def _close_project(self):
        # Quito el ítem del árbol
        item = self.currentItem()
        index = self.indexOfTopLevelItem(item)
        self.takeTopLevelItem(index)
        # Quito el elemento de la lista
        self._projects.pop(index)
        # Elimino los archivos del editor
        editor_container = Edis.get_component("principal")
        for index in reversed(range(editor_container.editor_widget.count())):
            weditor = editor_container.editor_widget.widget(index)
            if not weditor.filename.split(item.path)[0]:
                # El archivo pertenece al proyecto
                editor_container.editor_widget.remove_widget(weditor, index)

    @property
    def sources(self):
        """ Devuelve la lista de archivos fuentes """

        return self._sources

    def get_open_projects(self):
        return self._projects


class TreeItem(QTreeWidgetItem):
    """ Custom tree item"""

    def __init__(self, parent=None, name=''):
        QTreeWidgetItem.__init__(self, parent, name)
        self.isRoot = False
        self.isClickable = True
        self.isFile = True
        self._path = ''

    def do_root(self):
        self.isRoot = True
        self.isClickable = False
        self.isFile = False

    def __get_path(self):
        return self._path

    def __set_path(self, path):
        self._path = path

    path = property(__get_path, __set_path)


class EdisItem(TreeItem):
    """ Esta clase representa a un ítem tipo EdisProject """

    def __init__(self, parent=None, name=''):
        super(EdisItem, self).__init__(parent, name)

    def do_edis_item(self):
        self.isClickable = False
        self.isFile = False


class NewFileDialog(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setMinimumWidth(400)
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
        hbox.addWidget(self._combo_type, 1)
        container.addLayout(hbox)
        # Buttons
        hbox = QHBoxLayout()
        hbox.addStretch(1)
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