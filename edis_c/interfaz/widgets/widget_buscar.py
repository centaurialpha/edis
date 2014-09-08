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

import re

#from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QCompleter
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QLineEdit
#from PyQt4.QtGui import QCheckBox
from PyQt4.QtGui import QTextDocument
from PyQt4.QtGui import QTextCursor
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QKeySequence
from PyQt4.QtGui import QShortcut
from PyQt4.QtGui import QSizePolicy

from PyQt4.QtCore import Qt
from PyQt4.QtCore import QStringList
from PyQt4.QtCore import QString
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QObject

from edis_c import recursos
from edis_c.interfaz.contenedor_principal import contenedor_principal
from edis_c.interfaz.widgets.creador_widget import crear_boton
from edis_c.interfaz.widgets.creador_widget import get_icono_estandard

_Instancia = None

_ICONO = recursos.ICONOS


def WidgetBusqueda(*args, **kw):
    global _Instancia
    if _Instancia is None:
        _Instancia = _WidgetBuscar(*args, **kw)
    return _Instancia


class _WidgetBuscar(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.setWindowTitle(self.trUtf8("Buscar"))
        layoutV = QVBoxLayout(self)
        layoutV.setContentsMargins(0, 0, 0, 0)
        layoutV.setSpacing(0)

        self.widget_buscar = WidgetBuscar(self)
        layoutV.addWidget(self.widget_buscar)

        self.widget_reemplazo = WidgetReemplazo(self)
        layoutV.addWidget(self.widget_reemplazo)
        self.widget_reemplazo.setVisible(False)

        self.tecla_escape = QShortcut(QKeySequence(Qt.Key_Escape), self)

        self.connect(self.tecla_escape, SIGNAL("activated()"), self.ocultar)

    def ocultar(self):
        #self.widget_buscar.boton_sensitivo.setC
        #self.widget_buscar.boton_todo.setCheckState(Qt.Unchecked)
        self.hide()
        self.widget_buscar.setVisible(True)
        widget = contenedor_principal.ContenedorMain().devolver_widget_actual()
        if widget is not None:
            widget.setFocus()

    def buscar(self):
        self.widget_buscar.line_edit.setFocus()
        s = 0 if not self.widget_buscar.boton_sensitivo.isChecked() \
            else QTextDocument.FindCaseSensitively
        w = 0 if not self.widget_buscar.boton_todo.isChecked() \
            else QTextDocument.FindWholeWords
        banderas = s + w
        Weditor = contenedor_principal.ContenedorMain().devolver_editor_actual()
        if Weditor:
            Weditor.buscar_match(unicode(self.widget_buscar.line_edit.text()),
                banderas)

    def buscar_siguiente(self):
        s = 0
        w = 0
        s if not self.widget_buscar.boton_sensitivo.isChecked() \
            else QTextDocument.FindCaseSensitively
        w if not self.widget_buscar.boton_todo.isChecked() \
            else QTextDocument.FindWholeWords
        banderas = 0 + s + w
        Weditor = contenedor_principal.ContenedorMain().devolver_editor_actual()
        if Weditor:
            Weditor.buscar_match(unicode(self.widget_buscar.line_edit.text()),
                banderas, True)

    def buscar_anterior(self):
        s = 0 if not self.widget_buscar.boton_sensitivo.isChecked() \
            else QTextDocument.FindCaseSensitively
        w = 0 if not self.widget_buscar.boton_todo.isChecked() \
            else QTextDocument.FindWholeWords
        banderas = 1 + s + w
        Weditor = contenedor_principal.ContenedorMain().devolver_editor_actual()
        if Weditor:
            Weditor.buscar_match(unicode(self.widget_buscar.line_edit.text()),
                banderas, True)


class WidgetBuscar(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self._parent = parent
        grilla = QGridLayout()
        grilla.setContentsMargins(0, 0, 0, 0)
        self.setLayout(grilla)

        self.boton_sensitivo = crear_boton(self,
            triggered=self.check_state_changed, icono=get_icono_estandard(
                'FileDialogContentsView'), tip='Sensitivo')
        self.boton_todo = crear_boton(self,
            triggered=self.check_state_changed, icono=get_icono_estandard(
                'FileDialogDetailedView'), tip='Toda la palabra')
        self.line_edit = LineEdit(self)
        self.line_edit.setMinimumWidth(300)
        self.boton_cerrar = crear_boton(self, triggered=self.hide,
            icono=_ICONO['salir'], tip='Cerrar')
        self.boton_buscar = crear_boton(self, triggered=self.buscar_siguiente,
            icono=recursos.ICONOS['buscar'], tip='Buscar')
        self.boton_anterior = crear_boton(self, triggered=self.buscar_anterior,
            icono=_ICONO['anterior'], tip='Buscar anterior')
        self.boton_siguiente = crear_boton(self,
            triggered=self.buscar_siguiente, icono=_ICONO['siguiente'],
            tip='Buscar siguiente')
        self.boton_sensitivo.setCheckable(True)
        self.boton_todo.setCheckable(True)

        layoutH = QHBoxLayout()
        self.widgets = [
            self.boton_cerrar,
            self.line_edit,
            self.boton_buscar,
            self.boton_anterior,
            self.boton_siguiente,
            self.boton_sensitivo,
            self.boton_todo
            ]
        for widget in self.widgets:
            layoutH.addWidget(widget)
        grilla.addLayout(layoutH, 0, 1)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.total = 0
        self.indice = 0
        self.line_edit.contador_.actualizar_contador(self.indice, self.total)

    def check_state_changed(self):
        editor = contenedor_principal.ContenedorMain().devolver_editor_actual()
        if editor:
            editor.moveCursor(QTextCursor.Start)
            self.buscar_matches(editor)

    def buscar_siguiente(self):
        self._parent.buscar_siguiente()
        if self.total > 0 and self.indice < self.total:
            self.indice += 1
        elif self.total > 0:
            self.indice = 1
        self.line_edit.contador_.actualizar_contador(self.indice, self.total)

    def buscar_anterior(self):
        self._parent.buscar_anterior()
        if self.total > 0 and self.indice > 1:
            self.indice -= 1
        elif self.total > 0:
            self.indice = self.total
            Weditor = \
            contenedor_principal.ContenedorMain().devolver_editor_actual()
            Weditor.moveCursor(QTextCursor.End)
            self._parent.buscar_anterior()
        self.line_edit.contador_.actualizar_contador(self.indice, self.total)

    def buscar_matches(self, editor):
        if editor is None:
            return
        texto = editor.devolver_texto()
        search = unicode(self.line_edit.text())
        hasSearch = len(search) > 0
        if self.boton_todo.isChecked():
            patron = r'\b%s\b' % search
            temp_text = ' '.join(re.findall(patron, texto, re.IGNORECASE))
            texto = temp_text if temp_text != '' else texto
        if self.boton_sensitivo.isChecked():
            self.total = texto.count(search)
        else:
            self.total = texto.lower().count(search.lower())
        if hasSearch and self.total > 0:
            cursor = editor.textCursor()
            cursor.movePosition(QTextCursor.WordLeft)
            cursor.movePosition(QTextCursor.Start, QTextCursor.KeepAnchor)
            texto = unicode(cursor.selectedText())
            self.indice = texto.count(search) + 1
        else:
            self.indice = 0
            self.total = 0
        self.line_edit.contador_.actualizar_contador(self.indice, self.total,
            hasSearch)
        if hasSearch:
            self._parent.buscar()


class WidgetReemplazo(QWidget):

    def __init__(self, parent):
        super(WidgetReemplazo, self).__init__(parent)


class Completer(QCompleter):

    def __init__(self, palabras):
        super(Completer, self).__init__(palabras)
        self.setCompletionMode(QCompleter.PopupCompletion)
        self.setCaseSensitivity(Qt.CaseInsensitive)


class LineEdit(QLineEdit):

    def __init__(self, parent):
        QLineEdit.__init__(self, parent)
        self._parent = parent
        self.palabras = ['gabo', 'gabriel']
        self.completer = None
        self.listaComp = QStringList()
        self.contador_ = Contador(self)
        self.setPlaceholderText(self.trUtf8("Buscar!"))
        # Completador
        #for i in self.palabras:
            #self.listaComp.append(QString(i))
        if self.completer is None:
            self.completer = Completer(self.palabras)
            self.setCompleter(self.completer)
            #self.completer.setWidget(self)

    def agregar_al_completer(self):
        palabra = self.text()
        self.palabras.append(palabra)
        for i in self.palabras:
            self.listaComp.append(str(i))
        self.completer = Completer(self.palabras)
        self.setCompleter(self.completer)
        print(self.palabras)
            #if not self.palabras[i] == palabra:
                #self.listaComp.append(QString(i))
        ##pass

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.agregar_al_completer()
        editor = contenedor_principal.ContenedorMain().devolver_editor_actual()
        if editor is None:
            super(LineEdit, self).keyPressEvent(event)
            return
        if editor and event.key() in (Qt.Key_Enter, Qt.Key_Return):
            self._parent.buscar_siguiente()
            return
        super(LineEdit, self).keyPressEvent(event)
        if int(event.key()) in range(32, 162) or \
        event.key() == Qt.Key_Backspace:
            has_replace = self._parent._parent.widget_reemplazo.isVisible()
            if not has_replace:
                self._parent.buscar_matches(editor)


class Contador(QObject):

    def __init__(self, line_edit):
        QObject.__init__(self)
        self.line = line_edit
        layoutH = QHBoxLayout(line_edit)
        layoutH.setMargin(4)
        line_edit.setLayout(layoutH)
        layoutH.addStretch()
        self.contador = QLabel(line_edit)
        layoutH.addWidget(self.contador)

    def actualizar_contador(self, indice_, total_, hasSearch_=False):
        mensaje = self.tr("%1 de %2").arg(indice_).arg(total_)
        self.contador.setText(mensaje)
        ESTILO = {
            'True': True if indice_ == 0 and total_ == 0 and hasSearch_ else
            False
            }
        if ESTILO['True']:
            self.line.setStyleSheet(
                'background-color: rgb(255, 100, 10);border-radius: 3px;')
        else:
            self.line.setStyleSheet("color: gray;")