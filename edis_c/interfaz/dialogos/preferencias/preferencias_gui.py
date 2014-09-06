#-*- coding: utf8 -*-

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

# Módulos QtGui
from PyQt4.QtGui import QStyleFactory
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QSizePolicy
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QComboBox
from PyQt4.QtGui import QGroupBox
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QToolBar
from PyQt4.QtGui import QActionGroup
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QListWidget

# Módulos QtCore
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QSettings
from PyQt4.QtCore import QString
from PyQt4.QtCore import QSize

# Módulos EDIS
from edis_c import recursos
from edis_c.nucleo import configuraciones
#from edis_c.interfaz import distribuidor


class TabGUI(QWidget):

    def __init__(self, parent):
        super(TabGUI, self).__init__(parent)
        layoutV = QVBoxLayout(self)

        self.barra_herramientas = configuraciones.BARRA_HERRAMIENTAS_ITEMS

        # Grupos
        grupoToolbar = QGroupBox(self.trUtf8("Editar Barra de Herramientas:"))
        grupoEstilo = QGroupBox(self.trUtf8("Estilo de Widgets:"))

        layoutVT = QVBoxLayout(grupoToolbar)
        layoutVE = QVBoxLayout(grupoEstilo)

        layoutH_seleccionar_item = QHBoxLayout()
        label_toolbar = QLabel(self.trUtf8("Items barra de herramientas:"))
        label_toolbar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        layoutH_seleccionar_item.addWidget(label_toolbar)

        self.comboBarraItems = QComboBox()
        self.cargar_comboBox(self.comboBarraItems)
        self.boton_agregar = QPushButton(self.tr("Agregar"))
        self.boton_quitar = QPushButton(self.tr("Quitar"))
        self.boton_default = QPushButton(self.trUtf8("Reestablecer"))

        # Agregando widgets al layout
        layoutH_seleccionar_item.addWidget(self.comboBarraItems)
        layoutH_seleccionar_item.addWidget(self.boton_agregar)
        layoutH_seleccionar_item.addWidget(self.boton_quitar)
        layoutH_seleccionar_item.addWidget(self.boton_default)
        layoutVT.addLayout(layoutH_seleccionar_item)

        self.toolbar_bar_items = QToolBar()
        self.toolbar_bar_items.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.toolbar_bar_items.setIconSize(QSize(15, 15))
        self.cargar_toolbar()

        # Estilo
        self.lista_estilos = QListWidget()
        estilos = list(QStyleFactory.keys())
        [self.lista_estilos.addItem(estilo) for estilo in estilos[::-1]]

        layoutVT.addWidget(self.toolbar_bar_items)
        layoutVT.addWidget(QLabel(
            self.trUtf8("Se agregará después del boton seleccionado")),
                alignment=Qt.AlignTop)
        layoutVE.addWidget(self.lista_estilos)
        layoutV.addWidget(grupoToolbar)
        layoutV.addWidget(grupoEstilo)

        # Conexiones
        self.boton_agregar.clicked.connect(self.agregar_item)
        self.boton_quitar.clicked.connect(self.quitar_item)
        self.boton_default.clicked.connect(
            self.reestablecer_barra_de_herramientas)
        self.lista_estilos.itemSelectionChanged.connect(
            lambda: self.cambiar_estilo(
                QString(self.lista_estilos.currentItem().text())))

    def cargar_comboBox(self, comboBox):
        self.items_barra = {
            'separador': [QIcon(recursos.ICONOS['linea']),
                'Agregar separador'],
            'nuevo-archivo': [QIcon(recursos.ICONOS['nuevo']),
                'Nuevo archivo'],
            'abrir-archivo': [QIcon(recursos.ICONOS['abrir']),
                'Abrir archivo'],
            'guardar-archivo': [QIcon(recursos.ICONOS['guardar']),
                'Guardar archivo'],
            'guardar-como': [QIcon(recursos.ICONOS['guardar-como']),
                'Guardar como'],
            'guardar-todo': [QIcon(recursos.ICONOS['guardar-todo']),
                'Guardar todo'],
            'deshacer': [QIcon(recursos.ICONOS['deshacer']),
                'Deshacer'],
            'rehacer': [QIcon(recursos.ICONOS['rehacer']),
                'Rehacer'],
            'cortar': [QIcon(recursos.ICONOS['cortar']),
                'Cortar'],
            'copiar': [QIcon(recursos.ICONOS['copiar']),
                'Copiar'],
            'pegar': [QIcon(recursos.ICONOS['pegar']),
                'Pegar'],
            'buscar': [QIcon(recursos.ICONOS['buscar']),
                'Buscar'],
            'acercar': [QIcon(recursos.ICONOS['acercar']),
                'Acercar'],
            'alejar': [QIcon(recursos.ICONOS['alejar']),
                'Alejar'],
            'indentar': [QIcon(recursos.ICONOS['indentar']),
                'Indentar'],
            'desindentar': [QIcon(recursos.ICONOS['quitar-indentacion']),
                'Desindentar'],
            'arriba': [QIcon(recursos.ICONOS['arriba']),
                'Mover hacia arriba'],
            'abajo': [QIcon(recursos.ICONOS['abajo']),
                'Mover hacia abajo'],
            'include': [QIcon(recursos.ICONOS['insertar-include']),
                'Include'],
            'macro': [QIcon(recursos.ICONOS['insertar-macro']),
                'Macro'],
            'linea': [QIcon(recursos.ICONOS['linea']),
                'Separador'],
            'compilar-archivo': [QIcon(recursos.ICONOS['compilar']),
                'Compilar'],
            'ejecutar-archivo': [QIcon(recursos.ICONOS['ejecutar']),
                'Ejecutar'],
            'compilar-ejecutar-archivo': [QIcon(recursos.ICONOS['comp-ejec']),
                'Compilar y Ejecutar'],
            'frenar': [QIcon(recursos.ICONOS['frenar']),
                'Frenar']
                }

        [comboBox.addItem(self.items_barra[i][0], self.items_barra[i][1], i)
            for i in self.items_barra]

    def cargar_toolbar(self):
        self.toolbar_bar_items.clear()
        self.accionGrupo = QActionGroup(self)
        self.accionGrupo.setExclusive(True)
        for i in self.barra_herramientas:
            if i == 'separador':
                self.toolbar_bar_items.addSeparator()
            else:
                accion = self.toolbar_bar_items.addAction(
                    self.items_barra[i][0], self.items_barra[i][1])
                accion.setData(i)
                accion.setCheckable(True)
                self.accionGrupo.addAction(accion)

    def agregar_item(self):
        """ Agrega un item a la barra de herramientas. """

        d = self.comboBarraItems.itemData(self.comboBarraItems.currentIndex())
        d = str(d.toString())
        if d not in self.barra_herramientas or d == 'separador':
            seleccionado = self.accionGrupo.checkedAction()
            if seleccionado is None:
                self.barra_herramientas.append(d)
            else:
                dAct = str(seleccionado.data().toString())
                self.barra_herramientas.insert(
                    self.barra_herramientas.index(dAct) + 1, d)
            self.cargar_toolbar()

    def quitar_item(self):
        """ Quita un item de la barra de herramientas. """

        d = self.comboBarraItems.itemData(self.comboBarraItems.currentIndex())
        d = str(d.toString())
        if d in self.barra_herramientas and d != 'separador':
            self.barra_herramientas.pop(self.barra_herramientas.index(d))
            self.cargar_toolbar()
        elif d == 'separador':
            self.barra_herramientas.reverse()
            self.barra_herramientas.pop(self.barra_herramientas.index(d))
            self.barra_herramientas.reverse()
            self.cargar_toolbar()

    def reestablecer_barra_de_herramientas(self):
        """ Reestablece los items de la barra de herramientas. """

        self.barra_herramientas = configuraciones.BARRA_HERRAMIENTAS_ORIGINAL
        self.cargar_toolbar()

    def cambiar_estilo(self, estilo):
        #print self.lista_estilos.currentItem()
        QApplication.setStyle(QStyleFactory.create(estilo))
        QApplication.setPalette(QApplication.style().standardPalette())

    def guardar(self):
        """ Guarda las configuraciones de la GUI. """

        configuraciones.BARRA_HERRAMIENTAS_ITEMS = self.barra_herramientas
        qconfig = QSettings(recursos.CONFIGURACION, QSettings.IniFormat)
        qconfig.setValue('configuraciones/gui/barra',
            configuraciones.BARRA_HERRAMIENTAS_ITEMS)
        #distribuidor.Distribuidor().recargar_barra_de_herramientas()  # bug!