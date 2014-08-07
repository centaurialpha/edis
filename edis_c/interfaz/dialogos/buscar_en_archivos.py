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
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QComboBox
from PyQt4.QtGui import QSizePolicy
from PyQt4.QtGui import QDesktopServices
from PyQt4.QtGui import QTableWidget
from PyQt4.QtGui import QAbstractItemView
from PyQt4.QtGui import QHeaderView
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QProgressDialog
from PyQt4.QtGui import qApp
from PyQt4.QtGui import QTableWidgetItem
from PyQt4.QtGui import QShortcut
from PyQt4.QtGui import QKeySequence

from PyQt4.QtCore import QTextStream
from PyQt4.QtCore import QDir
from PyQt4.QtCore import QUrl
from PyQt4.QtCore import QFile
from PyQt4.QtCore import QIODevice
from PyQt4.QtCore import QFileInfo
from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL

from edis_c.interfaz.contenedor_principal import contenedor_principal

_Instancia = None


def WidgetBuscarEnArchivos(*args, **kw):
    global _Instancia
    if _Instancia is None:
        _Instancia = _WidgetBuscarEnArchivos(*args, **kw)
    return _Instancia


class _WidgetBuscarEnArchivos(QWidget):

    def __init__(self, parent=None):
        super(_WidgetBuscarEnArchivos, self).__init__(parent)
        layoutH = QHBoxLayout()
        layoutH.addStretch()

        boton_browse = QPushButton(self.trUtf8("Browse"))
        boton_browse.clicked.connect(self.browse)
        boton_buscar = QPushButton(self.trUtf8("Buscar"))
        boton_buscar.clicked.connect(self.buscar)
        self.combo_box_archivo = self.crear_combo("*")
        self.combo_box_texto = self.crear_combo()
        self.combo_box_directorio = self.crear_combo(QDir.currentPath())

        archivo_label = QLabel(self.trUtf8("Nombre:"))
        texto_label = QLabel(self.trUtf8("Texto contenido:"))
        directorio_label = QLabel(self.trUtf8("Directorio:"))
        self.archivos_label = QLabel()
        self.crear_tabla_de_archivos()

        layoutH.addWidget(boton_buscar)
        layout = QGridLayout()
        layout.addWidget(archivo_label, 0, 0)
        layout.addWidget(self.combo_box_archivo, 0, 1, 1, 2)
        layout.addWidget(texto_label, 1, 0)
        layout.addWidget(self.combo_box_texto, 1, 1, 1, 2)
        layout.addWidget(directorio_label, 2, 0)
        layout.addWidget(self.combo_box_directorio, 2, 1)
        layout.addWidget(boton_browse, 2, 2)
        layout.addWidget(self.tabla_archivos, 3, 0, 1, 3)
        layout.addWidget(self.archivos_label, 4, 0)
        layout.addLayout(layoutH, 5, 0, 1, 3)
        self.setLayout(layout)

        self.tecla_escape = QShortcut(QKeySequence(Qt.Key_Escape), self)

        self.connect(self.tecla_escape, SIGNAL("activated()"), self.ocultar)

    def ocultar(self):
        self.hide()
        self.setVisible(True)
        widget = contenedor_principal.ContenedorMain().devolver_widget_actual()
        if widget is not None:
            widget.setFocus()

    def crear_combo(self, texto=''):
        combo = QComboBox()
        combo.setEditable(True)
        combo.addItem(texto)
        combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        return combo

    def browse(self):
        directorio = QFileDialog.getExistingDirectory(self,
            self.trUtf8("Buscar archivos"), QDir.currentPath())

        if directorio:
            if self.combo_box_directorio.findText(directorio) == -1:
                self.combo_box_directorio.addItem(directorio)
            self.combo_box_directorio.setCurrentIndex(
                self.combo_box_directorio.findText(directorio))

    @staticmethod
    def actualizar_combo(combo):
        if combo.findText(combo.currentText()) == -1:
            combo.addItem(combo.currentText())

    def buscar(self):
        self.tabla_archivos.setRowCount(0)
        nombre_archivo = self.combo_box_archivo.currentText()
        texto = self.combo_box_texto.currentText()
        path = self.combo_box_directorio.currentText()

        self.actualizar_combo(self.combo_box_archivo)
        self.actualizar_combo(self.combo_box_texto)
        self.actualizar_combo(self.combo_box_directorio)

        self.directorio_actual = QDir(path)

        if not nombre_archivo:
            nombre_archivo = "*"
        archivos = self.directorio_actual.entryList([nombre_archivo],
            QDir.Files | QDir.NoSymLinks)

        if texto:
            archivos = self.buscar_archivos(archivos, texto)
        self.mostrar_archivos(archivos)

    def buscar_archivos(self, archivos, texto):
        dialogo_progreso = QProgressDialog(self)
        dialogo_progreso.setCancelButtonText(self.trUtf8("Cancelar"))
        dialogo_progreso.setRange(0, archivos.count())

        archivos_encontrados = []

        for i in range(archivos.count()):
            dialogo_progreso.setValue(i)
            dialogo_progreso.setLabelText(
                self.trUtf8("Buscando archivo número %d de %d " %
                (i, archivos.count())))
            qApp.processEvents()

            if dialogo_progreso.wasCanceled():
                break

            en_archivo = QFile(self.directorio_actual.absoluteFilePath(
                archivos[i]))
            if en_archivo.open(QIODevice.ReadOnly):
                flujo = QTextStream(en_archivo)
                while not flujo.atEnd():
                    if dialogo_progreso.wasCanceled():
                        break
                    linea = flujo.readLine()
                    if texto in linea:
                        archivos_encontrados.append(archivos[i])
        dialogo_progreso.close()

        return archivos_encontrados

    def mostrar_archivos(self, archivos):
        for f in archivos:
            archivo = QFile(self.directorio_actual.absoluteFilePath(f))
            tam = QFileInfo(archivo).size()

            item_archivo = QTableWidgetItem(f)
            item_archivo.setFlags(item_archivo.flags() ^ Qt.ItemIsEditable)
            item_tam = QTableWidgetItem("%d KB" % (int((tam + 1023) / 1024)))
            item_tam.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            item_tam.setFlags(item_tam.flags() ^ Qt.ItemIsEditable)

            fila = self.tabla_archivos.rowCount()
            self.tabla_archivos.insertRow(fila)
            self.tabla_archivos.setItem(fila, 0, item_archivo)
            self.tabla_archivos.setItem(fila, 1, item_tam)

        self.archivos_label.setText(self.trUtf8(
            "%d archivo(s) encontrado " % len(archivos)))

    def crear_tabla_de_archivos(self):
        self.tabla_archivos = QTableWidget()
        self.tabla_archivos.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_archivos.setHorizontalHeaderLabels(("nombre", "size"))
        self.tabla_archivos.horizontalHeader().setResizeMode(
            0, QHeaderView.Stretch)
        self.tabla_archivos.verticalHeader().hide()
        #self.tabla_archivos.setShowGrid(False)

        self.tabla_archivos.cellActivated.connect(self.abrir_archivo_item)

    def abrir_archivo_item(self, fila, columna):
        item = self.tabla_archivos.item(fila, 0)

        QDesktopServices.openUrl(QUrl(
            self.directorio_actual.absoluteFilePath(item.text())))