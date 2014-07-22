#-*- coding: utf-8 -*-

import re

from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QGridLayout
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QStyle
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QCheckBox
from PyQt4.QtGui import QTextDocument
from PyQt4.QtGui import QTextCursor
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QKeySequence
from PyQt4.QtGui import QShortcut

from PyQt4.QtCore import Qt
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QObject

from edis_c import recursos
from edis_c.interfaz.contenedor_principal import contenedor_principal

_dialogobuscarInstancia = None


def DialogoBuscar(*args, **kw):
    global _dialogobuscarInstancia
    if _dialogobuscarInstancia is None:
        _dialogobuscarInstancia = _DialogoBuscar(*args, **kw)
    return _dialogobuscarInstancia


class _DialogoBuscar(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent, Qt.Dialog)

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
        self.widget_buscar.checkSensitivo.setCheckState(Qt.Unchecked)
        self.widget_buscar.checkToda.setCheckState(Qt.Unchecked)
        self.hide()
        self.widget_buscar.setVisible(True)
        Weditor = contenedor_principal.ContenedorMain().devolver_editor_actual()
        #print "antes"
        if Weditor:
            #print "dentro"
            Weditor.setFocus()

    def buscar(self):
        s = 0 if not self.widget_buscar.checkSensitivo.isChecked() \
            else QTextDocument.FindCaseSensitively
        w = 0 if not self.widget_buscar.checkToda.isChecked() \
            else QTextDocument.FindWholeWords
        banderas = s + w
        Weditor = contenedor_principal.ContenedorMain().devolver_editor_actual()
        if Weditor:
            Weditor.buscar_match(unicode(self.widget_buscar.line_edit.text()),
                banderas)

    def buscar_siguiente(self):
        s = 0
        w = 0
        s if not self.widget_buscar.checkSensitivo.isChecked() \
            else QTextDocument.FindCaseSensitively
        w if not self.widget_buscar.checkToda.isChecked() \
            else QTextDocument.FindWholeWords
        banderas = 0 + s + w
        Weditor = contenedor_principal.ContenedorMain().devolver_editor_actual()
        if Weditor:
            Weditor.buscar_match(unicode(self.widget_buscar.line_edit.text()),
                banderas, True)

    def buscar_anterior(self):
        s = 0 if not self.widget_buscar.checkSensitivo.isChecked() \
            else QTextDocument.FindCaseSensitively
        w = 0 if not self.widget_buscar.checkToda.isChecked() \
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

        self.checkSensitivo = QCheckBox(self.trUtf8(
            "Respetar sensitivo al contexto"))
        self.checkToda = QCheckBox(self.trUtf8(
            "Buscar toda la palabra"))
        self.line_edit = LineEdit(self)
        self.line_edit.setMinimumWidth(300)
        self.boton_cerrar = QPushButton(
            self.style().standardIcon(QStyle.SP_DialogCloseButton), '')
        self.boton_buscar = QPushButton(QIcon(recursos.ICONOS['buscar']), '')
        self.boton_anterior = QPushButton(
            self.style().standardIcon(QStyle.SP_ArrowDown), '')
        self.boton_siguiente = QPushButton(
            self.style().standardIcon(QStyle.SP_ArrowUp), '')

        layoutPrincipal = QGridLayout()
        layoutPrincipal.addWidget(QLabel(self.trUtf8("Buscar:")), 0, 0)
        layoutPrincipal.addWidget(self.line_edit, 0, 1)
        layoutPrincipal.addWidget(self.boton_buscar, 0, 2)
        layoutPrincipal.addWidget(self.boton_anterior, 0, 3)
        layoutPrincipal.addWidget(self.boton_siguiente, 0, 4)
        layoutPrincipal.addWidget(self.checkSensitivo, 1, 0)
        layoutPrincipal.addWidget(self.checkToda, 2, 0)
        self.setLayout(layoutPrincipal)

        self.total = 0
        self.indice = 0
        self.line_edit.contador_.actualizar_contador(self.indice, self.total)

        self.connect(self.boton_buscar, SIGNAL("clicked()"),
            self.buscar_siguiente)
        self.connect(self.boton_siguiente, SIGNAL("clicked()"),
            self.buscar_siguiente)
        self.connect(self.boton_anterior, SIGNAL("clicked()"),
            self.buscar_anterior)
        self.connect(self.checkSensitivo, SIGNAL("stateChanged(int)"),
            self.check_state_changed)
        self.connect(self.checkToda, SIGNAL("stateChanged(int)"),
            self.check_state_changed)

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
        if self.checkToda.isChecked():
            patron = r'\b%s\b' % search
            temp_text = ' '.join(re.findall(patron, texto, re.IGNORECASE))
            texto = temp_text if temp_text != '' else texto
        if self.checkSensitivo.isChecked():
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


class LineEdit(QLineEdit):

    def __init__(self, parent):
        QLineEdit.__init__(self, parent)
        self._parent = parent
        self.contador_ = Contador(self)

    def keyPressEvent(self, event):
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
        layoutH.setMargin(0)
        line_edit.setLayout(layoutH)
        layoutH.addStretch()
        self.contador = QLabel(line_edit)
        layoutH.addWidget(self.contador)
        line_edit.setStyleSheet("padding-right: 1px;")
        line_edit.setTextMargins(0, 0, 0, 0)

    def actualizar_contador(self, indice_, total_, hasSearch_=False):
        mensaje = self.tr("%1 de %2").arg(indice_).arg(total_)
        self.contador.setText(mensaje)
        self.line.setStyleSheet("background: none;color: gray;")
        if indice_ == 0 and total_ == 0 and hasSearch_:
            #self.contador.setStyleSheet(
                #"background: red;color; white;border-radius: 3px;")
            self.line.setStyleSheet(
                "background: red;color;white;border-radius: 3px")