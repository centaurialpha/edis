# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

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


def create_button(parent, text=None, shortcut=None, icon=None, triggered=None,
                    text_beside=False, toggled=None, autoraise=True,
                    action=None):

    """ Create a ToolButton """

    tbutton = Button(parent)
    if text is not None:
        tbutton.setText(text)
    if icon is not None:
        tbutton.setIcon(QIcon(icon))
    tbutton.setAutoRaise(autoraise)
    if triggered is not None:
        QObject.connect(tbutton, SIGNAL("clicked()"), triggered)
    if toggled is not None:
        QObject.connect(tbutton, SIGNAL("toggled(bool)"), toggled)
        tbutton.setCheckable(True)
    if action is not None:
        tbutton.setDefaultAction(action)
    if shortcut is not None:
        tbutton.setShortcut(shortcut)
    if text_beside:
        tbutton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
    else:
        tbutton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
    return tbutton


class Button(QToolButton):

    def __init__(self, parent=None):
        QToolButton.__init__(self, parent)


class ComboSelector(QComboBox):

    def __init__(self, parent=None):
        QComboBox.__init__(self, parent)
