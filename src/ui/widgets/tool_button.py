# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)


from PyQt4.QtGui import (
    QToolButton,
    QStylePainter,
    QStyle,
    QStyleOptionButton,
    )


class CustomToolButton(QToolButton):

    def __init__(self, texto, parent=None):
        QToolButton.__init__(self, parent)
        self.setObjectName("dock_button")
        self.setText(texto)
        self.setCheckable(True)
        self.setAutoRaise(True)

    def paintEvent(self, evento):
        painter = QStylePainter(self)
        painter.rotate(-90)
        painter.translate(-self.height(), 0)
        painter.drawControl(QStyle.CE_PushButton, self.getStyleOptions())

    def getStyleOptions(self):
        opciones = QStyleOptionButton()
        opciones.initFrom(self)
        tam = opciones.rect.size()
        tam.transpose()
        opciones.rect.setSize(tam)
        if self.isChecked():
            opciones.state |= QStyle.State_On

        opciones.text = self.text()
        return opciones

    def sizeHint(self):
        tam = super(CustomToolButton, self).sizeHint()
        tam.transpose()
        return tam
