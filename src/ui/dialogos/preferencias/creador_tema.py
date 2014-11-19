#-*- coding: utf-8 -*-

# Copyright (C) <2014>  <Gabriel Acosta>

# EDIS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# EDIS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with EDIS.  If not, see <http://www.gnu.org/licenses/>.

# Módulos Python
import copy

# Módulos QtGui
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QColorDialog
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QGroupBox

# Módulos QtCore
from PyQt4.QtCore import QString

# Módulos EDIS
from src import recursos
from src.helpers import manejador_de_archivo
from src.ui.contenedor_principal import contenedor_principal


class CreadorDeTemaEditor(QWidget):

    def __init__(self, parent):
        super(CreadorDeTemaEditor, self).__init__()
        self.parent = parent
        layoutM = QVBoxLayout(self)
        layoutH = QHBoxLayout()
        layoutH.setContentsMargins(0, 0, 0, 0)

        self.original = copy.copy(recursos.NUEVO_TEMA)

        self.linea_palabraReservada = QLineEdit()
        boton_palabraReservada = QPushButton(self.trUtf8("Color"))
        self.linea_operador = QLineEdit()
        boton_operador = QPushButton(self.trUtf8("Color"))
        self.linea_braces = QLineEdit()
        boton_braces = QPushButton(self.trUtf8("Color"))
        self.linea_struct = QLineEdit()
        boton_struct = QPushButton(self.trUtf8("Color"))
        self.linea_cadena = QLineEdit()
        boton_cadena = QPushButton(self.trUtf8("Color"))
        self.linea_caracter = QLineEdit()
        boton_caracter = QPushButton(self.trUtf8("Color"))
        self.linea_include = QLineEdit()
        boton_include = QPushButton(self.trUtf8("Color"))
        self.linea_comentario = QLineEdit()
        boton_comentario = QPushButton(self.trUtf8("Color"))
        self.linea_numero = QLineEdit()
        boton_numero = QPushButton(self.trUtf8("Color"))
        self.linea_texto = QLineEdit()
        boton_texto = QPushButton(self.trUtf8("Color"))
        self.linea_fondoEditor = QLineEdit()
        boton_fondoEditor = QPushButton(self.trUtf8("Color"))
        self.linea_seleccion = QLineEdit()
        boton_seleccion = QPushButton(self.trUtf8("Color"))
        self.linea_fondoSeleccion = QLineEdit()
        boton_fondoSeleccion = QPushButton(self.trUtf8("Color"))
        self.linea_lineaActual = QLineEdit()
        boton_lineaActual = QPushButton(self.trUtf8("Color"))
        self.linea_sidebar = QLineEdit()
        boton_sidebar = QPushButton(self.trUtf8("Color"))
        self.linea_numeroLinea = QLineEdit()
        boton_numeroLinea = QPushButton(self.trUtf8("Color"))
        self.linea_numeroSeleccionado = QLineEdit()
        boton_numeroSeleccionado = QPushButton(self.trUtf8("Color"))
        self.linea_margen = QLineEdit()
        boton_margen = QPushButton(self.trUtf8("Color"))

        layoutHo = QHBoxLayout()
        grupoResaltado = QGroupBox(self.trUtf8("Resaltado de Sintaxis:"))
        grupoEditor = QGroupBox(self.trUtf8("Editor:"))
        grilla = QGridLayout(grupoResaltado)
        grilla_ = QGridLayout(grupoEditor)
        layoutHo.addWidget(grupoResaltado)
        layoutHo.addWidget(grupoEditor)

        # Resaltado de Sintaxis
        grilla.addWidget(QLabel(self.trUtf8("Palabra reservada:")), 0, 0)
        grilla.addWidget(self.linea_palabraReservada, 0, 1)
        grilla.addWidget(boton_palabraReservada, 0, 2)
        grilla.addWidget(QLabel(self.trUtf8("Operador:")), 1, 0)
        grilla.addWidget(self.linea_operador, 1, 1)
        grilla.addWidget(boton_operador, 1, 2)
        grilla.addWidget(QLabel(self.trUtf8("Braces:")), 2, 0)
        grilla.addWidget(self.linea_braces, 2, 1)
        grilla.addWidget(boton_braces, 2, 2)
        grilla.addWidget(QLabel(self.trUtf8("Estructuras:")), 3, 0)
        grilla.addWidget(self.linea_struct, 3, 1)
        grilla.addWidget(boton_struct, 3, 2)
        grilla.addWidget(QLabel(self.trUtf8("Cadena:")), 4, 0)
        grilla.addWidget(self.linea_cadena, 4, 1)
        grilla.addWidget(boton_cadena, 4, 2)
        grilla.addWidget(QLabel(self.trUtf8("Caracteres:")), 5, 0)
        grilla.addWidget(self.linea_caracter, 5, 1)
        grilla.addWidget(boton_caracter, 5, 2)
        grilla.addWidget(QLabel(self.trUtf8("Include:")), 6, 0)
        grilla.addWidget(self.linea_include, 6, 1)
        grilla.addWidget(boton_include, 6, 2)
        grilla.addWidget(QLabel(self.trUtf8("Comentario:")), 7, 0)
        grilla.addWidget(self.linea_comentario, 7, 1)
        grilla.addWidget(boton_comentario, 7, 2)
        grilla.addWidget(QLabel(self.trUtf8("Número:")), 8, 0)
        grilla.addWidget(self.linea_numero, 8, 1)
        grilla.addWidget(boton_numero, 8, 2)
        # Tema editor
        grilla_.addWidget(QLabel(self.trUtf8("Texto editor:")), 0, 0)
        grilla_.addWidget(self.linea_texto, 0, 1)
        grilla_.addWidget(boton_texto, 0, 2)
        grilla_.addWidget(QLabel(self.trUtf8("Fondo editor:")), 1, 0)
        grilla_.addWidget(self.linea_fondoEditor, 1, 1)
        grilla_.addWidget(boton_fondoEditor, 1, 2)
        grilla_.addWidget(QLabel(self.trUtf8("Texto seleccionado:")), 2, 0)
        grilla_.addWidget(self.linea_seleccion, 2, 1)
        grilla_.addWidget(boton_seleccion, 2, 2)
        grilla_.addWidget(QLabel(self.trUtf8("Fondo selección:")), 3, 0)
        grilla_.addWidget(self.linea_fondoSeleccion, 3, 1)
        grilla_.addWidget(boton_fondoSeleccion, 3, 2)
        grilla_.addWidget(QLabel(self.trUtf8("Linea actual:")), 4, 0)
        grilla_.addWidget(self.linea_lineaActual, 4, 1)
        grilla_.addWidget(boton_lineaActual, 4, 2)
        grilla_.addWidget(QLabel(self.trUtf8("Sidebar:")), 5, 0)
        grilla_.addWidget(self.linea_sidebar, 5, 1)
        grilla_.addWidget(boton_sidebar, 5, 2)
        grilla_.addWidget(QLabel(self.trUtf8("Número sidebar:")), 6, 0)
        grilla_.addWidget(self.linea_numeroLinea, 6, 1)
        grilla_.addWidget(boton_numeroLinea, 6, 2)
        grilla_.addWidget(QLabel(self.trUtf8("Número seleccionado:")), 7, 0)
        grilla_.addWidget(self.linea_numeroSeleccionado, 7, 1)
        grilla_.addWidget(boton_numeroSeleccionado, 7, 2)
        grilla_.addWidget(QLabel(self.trUtf8("Márgen:")), 8, 0)
        grilla_.addWidget(self.linea_margen, 8, 1)
        grilla_.addWidget(boton_margen, 8, 2)

        layoutHH = QHBoxLayout()
        layoutHH.addWidget(QLabel(self.trUtf8("Guardar tema:")))
        lineEdit = QLineEdit()
        layoutHH.addWidget(lineEdit)
        boton_guardarTema = QPushButton(self.trUtf8("Guardar"))
        layoutHH.addWidget(boton_guardarTema)

        layoutH.addWidget(grupoResaltado)
        layoutH.addWidget(grupoEditor)
        layoutM.addLayout(layoutHH)
        layoutM.addLayout(layoutH)

        # Color de botón obtenido del texto.
        self.linea_palabraReservada.textChanged[QString].connect(
            lambda: self.estilo_boton(boton_palabraReservada,
                self.linea_palabraReservada.text()))
        self.linea_operador.textChanged[QString].connect(
            lambda: self.estilo_boton(boton_operador,
                self.linea_operador.text()))
        self.linea_braces.textChanged[QString].connect(
            lambda: self.estilo_boton(boton_braces, self.linea_braces.text()))
        self.linea_struct.textChanged[QString].connect(
            lambda: self.estilo_boton(boton_struct, self.linea_struct.text()))
        self.linea_cadena.textChanged[QString].connect(
            lambda: self.estilo_boton(boton_cadena, self.linea_cadena.text()))
        self.linea_caracter.textChanged[QString].connect(
            lambda: self.estilo_boton(boton_caracter,
                self.linea_caracter.text()))
        self.linea_include.textChanged[QString].connect(
            lambda: self.estilo_boton(boton_include, self.linea_include.text()))
        self.linea_comentario.textChanged[QString].connect(
            lambda: self.estilo_boton(boton_comentario,
                self.linea_comentario.text()))
        self.linea_numero.textChanged[QString].connect(
            lambda: self.estilo_boton(boton_numero, self.linea_numero.text()))
        self.linea_texto.textChanged[QString].connect(
            lambda: self.estilo_boton(boton_texto, self.linea_texto.text()))
        self.linea_fondoEditor.textChanged[QString].connect(
            lambda: self.estilo_boton(boton_fondoEditor,
                self.linea_fondoEditor.text()))
        self.linea_seleccion.textChanged[QString].connect(
            lambda: self.estilo_boton(boton_seleccion,
                self.linea_seleccion.text()))
        self.linea_fondoSeleccion.textChanged[QString].connect(
            lambda: self.estilo_boton(boton_fondoSeleccion,
                self.linea_fondoSeleccion.text()))
        self.linea_lineaActual.textChanged[QString].connect(
            lambda: self.estilo_boton(boton_lineaActual,
                self.linea_lineaActual.text()))
        self.linea_sidebar.textChanged[QString].connect(
            lambda: self.estilo_boton(boton_sidebar,
                self.linea_sidebar.text()))
        self.linea_numeroLinea.textChanged[QString].connect(
            lambda: self.estilo_boton(boton_numeroLinea,
                self.linea_numeroLinea.text()))
        self.linea_numeroSeleccionado.textChanged[QString].connect(
            lambda: self.estilo_boton(boton_numeroSeleccionado,
                self.linea_numeroSeleccionado.text()))
        self.linea_margen.textChanged[QString].connect(
            lambda: self.estilo_boton(boton_margen,
                self.linea_margen.text()))

        # Elección de color
        boton_palabraReservada.clicked.connect(lambda: self.elegir_color(
            self.linea_palabraReservada, boton_palabraReservada))
        boton_operador.clicked.connect(lambda: self.elegir_color(
            self.linea_operador, boton_operador))
        boton_braces.clicked.connect(lambda: self.elegir_color(
            self.linea_braces, boton_braces))
        boton_struct.clicked.connect(lambda: self.elegir_color(
            self.linea_struct, boton_struct))
        boton_cadena.clicked.connect(lambda: self.elegir_color(
            self.linea_cadena, boton_cadena))
        boton_caracter.clicked.connect(lambda: self.elegir_color(
            self.linea_caracter, boton_caracter))
        boton_include.clicked.connect(lambda: self.elegir_color(
            self.linea_include, boton_include))
        boton_comentario.clicked.connect(lambda: self.elegir_color(
            self.linea_comentario, boton_comentario))
        boton_numero.clicked.connect(lambda: self.elegir_color(
            self.linea_numero, boton_numero))
        boton_texto.clicked.connect(lambda: self.elegir_color(
            self.linea_texto, boton_texto))
        boton_fondoEditor.clicked.connect(lambda: self.elegir_color(
            self.linea_fondoEditor, boton_fondoEditor))
        boton_seleccion.clicked.connect(lambda: self.elegir_color(
            self.linea_seleccion, boton_seleccion))
        boton_fondoSeleccion.clicked.connect(lambda: self.elegir_color(
            self.linea_fondoSeleccion, boton_fondoSeleccion))
        boton_lineaActual.clicked.connect(lambda: self.elegir_color(
            self.linea_lineaActual, boton_lineaActual))
        boton_sidebar.clicked.connect(lambda: self.elegir_color(
            self.linea_sidebar, boton_sidebar))
        boton_numeroLinea.clicked.connect(lambda: self.elegir_color(
            self.linea_numeroLinea, boton_numeroLinea))
        boton_numeroSeleccionado.clicked.connect(lambda: self.elegir_color(
            self.linea_numeroSeleccionado, boton_numeroSeleccionado))
        boton_margen.clicked.connect(lambda: self.elegir_color(
            self.linea_margen, boton_margen))

        # Para previsualizar el editor cuando se presiona Enter
        for i in range(0, 8):
            item = grilla_.itemAtPosition(i, 1).widget()
            boton = grilla_.itemAtPosition(i, 2).widget()
            item.returnPressed.connect(self.previsualizar)
            self.estilo_boton(boton, item.text())

        boton_guardarTema.clicked.connect(self.guardar_tema)

    def aplicar_estilo_de_color(self):
        self.linea_palabraReservada.setText(
            recursos.NUEVO_TEMA.get('palabra',
                recursos.TEMA_EDITOR['palabra']))
        self.linea_operador.setText(recursos.NUEVO_TEMA.get('operador',
            recursos.TEMA_EDITOR['operador']))
        self.linea_braces.setText(recursos.NUEVO_TEMA.get('braces',
            recursos.TEMA_EDITOR['brace']))
        self.linea_struct.setText(recursos.NUEVO_TEMA.get('struct',
            recursos.TEMA_EDITOR['struct']))
        self.linea_cadena.setText(recursos.NUEVO_TEMA.get('cadena',
            recursos.TEMA_EDITOR['cadena']))
        self.linea_caracter.setText(recursos.NUEVO_TEMA.get('caracter',
            recursos.TEMA_EDITOR['caracter']))
        self.linea_include.setText(recursos.NUEVO_TEMA.get('include',
            recursos.TEMA_EDITOR['include']))
        self.linea_comentario.setText(recursos.NUEVO_TEMA.get('comentario',
            recursos.TEMA_EDITOR['comentario']))
        self.linea_numero.setText(recursos.NUEVO_TEMA.get('numero',
            recursos.TEMA_EDITOR['numero']))
        self.linea_texto.setText(recursos.NUEVO_TEMA.get('texto-editor',
            recursos.TEMA_EDITOR['texto-editor']))
        self.linea_fondoEditor.setText(recursos.NUEVO_TEMA.get('fondo-editor',
            recursos.TEMA_EDITOR['fondo-editor']))
        self.linea_seleccion.setText(recursos.NUEVO_TEMA.get('seleccion-editor',
            recursos.TEMA_EDITOR['seleccion-editor']))
        self.linea_fondoSeleccion.setText(
            recursos.NUEVO_TEMA.get('fondo-seleccion-editor',
                recursos.TEMA_EDITOR['fondo-seleccion-editor']))
        self.linea_lineaActual.setText(recursos.NUEVO_TEMA.get('linea-actual',
            recursos.TEMA_EDITOR['linea-actual']))
        self.linea_sidebar.setText(recursos.NUEVO_TEMA.get('widget-num-linea',
            recursos.TEMA_EDITOR['widget-num-linea']))
        self.linea_numeroLinea.setText(recursos.NUEVO_TEMA.get('numero-linea',
            recursos.TEMA_EDITOR['numero-linea']))
        self.linea_numeroSeleccionado.setText(
            recursos.NUEVO_TEMA.get('num-seleccionado',
                recursos.TEMA_EDITOR['num-seleccionado']))
        self.linea_margen.setText(recursos.NUEVO_TEMA.get('margen-linea',
            recursos.TEMA_EDITOR['margen-linea']))

    def estilo_boton(self, boton, nombre):
        """ Pinta los botones """

        if QColor(nombre).isValid():
            boton.setAutoFillBackground(True)
            estilo = ('background: %s; border-radius: 5px; '
                        'padding: 5px;' % nombre)
            boton.setStyleSheet(estilo)

    def elegir_color(self, lineEdit, boton):
        color = QColorDialog.getColor(QColor(lineEdit.text()),
            self, self.trUtf8("Elige el color: "))
        if color.isValid():
            lineEdit.setText(str(color.name()))
            self.estilo_boton(boton, color.name())
            self.previsualizar()

    def previsualizar(self):
        tema = {
            "palabra": str(self.linea_palabraReservada.text()),
            "operador": str(self.linea_operador.text()),
            "brace": str(self.linea_braces.text()),
            "struct": str(self.linea_struct.text()),
            "cadena": str(self.linea_cadena.text()),
            "caracter": str(self.linea_caracter.text()),
            "include": str(self.linea_include.text()),
            "comentario": str(self.linea_comentario.text()),
            "numero": str(self.linea_numero.text()),
            "texto-editor": str(self.linea_texto.text()),
            "fondo-editor": str(self.linea_fondoEditor.text()),
            "seleccion-editor": str(self.linea_seleccion.text()),
            "fondo-seleccion-editor": str(self.linea_fondoSeleccion.text()),
            "linea-actual": str(self.linea_lineaActual.text()),
            "widget-num-linea": str(self.linea_sidebar.text()),
            "numero-linea": str(self.linea_numeroLinea.text()),
            "num-seleccionado": str(self.linea_numeroSeleccionado.text()),
            "margen-linea": str(self.linea_margen.text())
            }
        recursos.NUEVO_TEMA = tema
        Weditor = contenedor_principal.ContenedorMain().devolver_editor_actual()
        if Weditor is not None:
            Weditor.estilo_editor()
        return tema

    def hideEvent(self, evento):
        super(CreadorDeTemaEditor, self).hideEvent(evento)
        Weditor = contenedor_principal.ContenedorMain().devolver_editor_actual()
        if Weditor is not None:
            Weditor.estilo_editor()

    def showEvent(self, evento):
        super(CreadorDeTemaEditor, self).showEvent(evento)
        Weditor = contenedor_principal.ContenedorMain().devolver_editor_actual()
        if Weditor is not None:
            Weditor.estilo_editor()
        self.aplicar_estilo_de_color()

    def guardar_tema(self):
        #print "1"
        nombre_tema = unicode(self.linea_nombre.text()).strip()
        #print nombre_tema
        nombre_archivo = manejador_de_archivo.crear_path(
            recursos.TEMAS_GUARDADOS, nombre_tema) + '.color'
        print nombre_archivo
        r = True
        if manejador_de_archivo.archivo_existente(nombre_archivo):
            r = QMessageBox.question(self, self.trUtf8("El tema ya existe!"),
                self.trUtf8("Sobreescribir el tema: %s?" % nombre_archivo),
                QMessageBox.Yes, QMessageBox.No)
        if nombre_tema != '' and r in (QMessageBox.Yes, True):
            tema = self.previsualizar()
            manejador_de_archivo.guardar_tema_editor(nombre_archivo, tema)
            QMessageBox.information(self, self.trUtf8("Tema guardado!"),
                self.trUtf8("El tema se ha guardado en: %s" % nombre_archivo))

        elif r == QMessageBox.Yes:
            QMessageBox.information(self, self.trUtf8("Tema no guardado!"),
                self.trUtf8("El nombre es inválido!"))

    def guardar(self):
        pass