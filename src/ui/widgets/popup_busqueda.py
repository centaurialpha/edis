# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)


from PyQt4.QtGui import (
    QDialog,
    QLineEdit,
    QHBoxLayout,
    QToolButton,
    QIcon,
    QCheckBox,
    QLabel
    )

from PyQt4.QtCore import (
    Qt,
    QPoint,
    QSize,
    QPropertyAnimation,
    QObject
    )

from src import recursos


class PopupBusqueda(QDialog):

    def __init__(self, editor):
        super(PopupBusqueda, self).__init__(editor)
        self.editor = editor
        self.total = 0
        # Popup!
        self.setWindowFlags(Qt.Popup)
        box = QHBoxLayout(self)
        self.linea = Linea(self)
        self.linea.setMinimumWidth(300)
        # Posición con respecto al editor
        point = editor.rect().bottomLeft()
        global_point = editor.mapToGlobal(point)
        self.move(global_point - QPoint(self.width() - 100, 34))

        # Ui
        btn_cerrar = QToolButton()
        btn_cerrar.setIcon(QIcon(recursos.ICONOS['close']))
        btn_buscar = QToolButton()
        btn_buscar.setIcon(QIcon(recursos.ICONOS['search']))
        btn_anterior = QToolButton()
        btn_anterior.setIcon(QIcon(recursos.ICONOS['arrow-back']))
        btn_siguiente = QToolButton()
        btn_siguiente.setIcon(QIcon(recursos.ICONOS['arrow-forward']))
        self.check_cs = QCheckBox(self.tr(
                                "Sensitivo a maýusculas y minúsculas"))
        self.check_wo = QCheckBox(self.tr(
                                "Solo palabras completas"))
        box.addWidget(btn_cerrar)
        box.addWidget(self.linea)
        box.addWidget(btn_buscar)
        box.addWidget(btn_anterior)
        box.addWidget(btn_siguiente)
        box.addWidget(self.check_cs)
        box.addWidget(self.check_wo)

        ancho_widget = editor.width() - self.sizeHint().width() + 17
        box.setContentsMargins(5, 5, ancho_widget, 5)

        # Conexiones
        btn_cerrar.clicked.connect(self.close)
        self.linea.returnPressed.connect(self.buscar)

    @property
    def texto(self):
        return self.linea.text()

    def buscar(self, weditor=None):
        #FIXME: Completar
        if weditor is None:
            weditor = self.editor
        palabra = self.texto
        codigo = weditor.texto
        self.total = codigo.count(palabra)
        weditor.buscar(palabra)
        self.linea.contador.actualizar(self.total)

    def showEvent(self, e):
        super(PopupBusqueda, self).showEvent(e)
        tam = self.linea.size()
        tam_inicio = QSize(tam.width(), 10)
        self.resize(tam_inicio)

        # Animación
        animacion = QPropertyAnimation(self.linea, 'size', self.linea)
        animacion.setStartValue(tam_inicio)
        animacion.setEndValue(tam)
        animacion.setDuration(300)
        animacion.start()
        self.linea.setFocus()


class Linea(QLineEdit):

    def __init__(self, popup):
        super(Linea, self).__init__(popup)
        self.popup = popup
        self.contador = Contador(self)

    def keyPressEvent(self, e):
        weditor = self.popup.editor
        if weditor is None:
            super(Linea, self).keyPressEvent(e)
            return
        if weditor and e.key() in (Qt.Key_Enter, Qt.Key_Return):
            #FIXME: Buscar siguiente
            pass
        super(Linea, self).keyPressEvent(e)
        # Iterar en todas las teclas
        if int(e.key()) in range(32, 162) or e.key() == Qt.Key_Backspace:
            self.popup.buscar(weditor)


class Contador(QObject):

    def __init__(self, linea):
        super(Contador, self).__init__()
        self._linea = linea
        box = QHBoxLayout(self._linea)
        box.setMargin(2)
        self._linea.setLayout(box)
        box.addStretch()
        self._contador = QLabel(self._linea)
        box.addWidget(self._contador)
        self._total = "%s"
        self._contador.setText(self._total % 0)

    def actualizar(self, total):
        self._contador.setText(self._total % total)
        if total == 0:
            self._linea.setStyleSheet(
                "background-color: #e73e3e; border-radius: 3px;")
        else:
            self._linea.setStyleSheet("color: #dedede")