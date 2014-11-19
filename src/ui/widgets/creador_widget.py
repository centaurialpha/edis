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

# Módulos QtGui
from PyQt4.QtGui import (
    QToolButton,
    QIcon,
    QWidget,
    QStyle,
    QAction,
    QComboBox
    )

# Módulos QtCore
from PyQt4.QtCore import (
    SIGNAL,
    QObject,
    Qt
    )


def crear_boton(parent, texto=None, atajo=None, icono=None, tip=None,
                triggered=None, toggled=None):
    """ Estructura:
        @parent: parent
        @texto: texto que se muestra en el botón
        @atajo: shortcut de la acción
        @icono: icono del botón
        @tip: status tip
        @triggered: señal
    """
    boton = QToolButton(parent)
    if texto is not None:
        boton.setText(texto)
    if icono is not None:
        boton.setIcon(QIcon(icono))
    if texto is not None or tip is not None:
        boton.setToolTip(texto if tip is None else tip)
    if triggered is not None:
        QObject.connect(boton, SIGNAL("clicked()"), triggered)
    if toggled is not None:
        QObject.connect(boton, SIGNAL("toggled(bool)"), toggled)
        boton.setCheckable(True)
    if atajo is not None:
        boton.setShortcut(atajo)

    return boton


def get_icono_estandard(nombre):
    """ Se devuelve el ícono estándar del sistema. """

    if not nombre.startswith('SP_'):
        nombre = 'SP_' + nombre
    icono = QWidget().style().standardIcon(getattr(QStyle, nombre))
    return QIcon(icono)


def crear_accion(parent, texto, icono=None, atajo=None, tip=None,
                slot=None):
    """ Retorna un QAction con los parámetros asociados. """

    accion = QAction(parent.trUtf8(texto), parent)
    if icono is not None:
        accion.setIcon(QIcon(icono))
    if atajo is not None:
        accion.setShortcut(atajo)
    if tip is not None:
        accion.setToolTip(tip)
        accion.setStatusTip(tip)
    if slot is not None:
        parent.connect(accion, SIGNAL("triggered()"), slot)
    return accion


def create_button(parent, text=None, shortcut=None, icon=None,
                    triggered=None, toggled=None, autoraise=True, action=None):

    """ Create a ToolButton """

    tbutton = Button(parent)
    if text is not None:
        tbutton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
    if icon is not None:
        tbutton.setIcon(QIcon(icon))
    tbutton.setAutoRaise(autoraise)
    if toggled is not None:
        QObject.connect(tbutton, SIGNAL("toggled(bool)"), toggled)
    if triggered is not None:
        QObject.connect(tbutton, SIGNAL("clicked()"), triggered)
    if shortcut is not None:
        tbutton.setShortcut(shortcut)
    if action is not None:
        tbutton.setDefaultAction(action)
    return tbutton


class Button(QToolButton):

    def __init__(self, parent=None):
        QToolButton.__init__(self, parent)


class ComboSelector(QComboBox):

    def __init__(self, parent=None):
        QComboBox.__init__(self, parent)
