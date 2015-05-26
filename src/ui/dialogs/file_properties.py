# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import re
import os
from datetime import datetime

from PyQt4.QtGui import (
    QDialog,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton
    )

from PyQt4.QtCore import (
    Qt,
    QFile
    )


class FileProperty(QDialog):

    def __init__(self, editor, parent=None):
        QDialog.__init__(self, parent, Qt.Dialog)
        self.setWindowTitle(self.tr("Propiedades del Archivo"))
        filename = editor.filename
        vLayout = QVBoxLayout(self)
        vLayout.setContentsMargins(10, 15, 10, 10)
        vLayout.setSpacing(10)

        lbl_title = QLabel(filename.split('/')[-1])
        lbl_title.setStyleSheet("font-weight: bold; font-size: 24px;")
        vLayout.addWidget(lbl_title)

        grid = QGridLayout()
        grid.addWidget(QLabel(self.tr("<b>Tipo:</b>")), 1, 0)
        grid.addWidget(QLabel(self.get_type(filename)), 1, 1)
        grid.addWidget(QLabel(self.tr("<b>Tamaño:</b>")), 2, 0)
        grid.addWidget(QLabel(self.get_size(filename)), 2, 1)
        grid.addWidget(QLabel(self.tr("<b>Ubicación:</b>")), 3, 0)
        grid.addWidget(QLabel(filename), 3, 1)
        grid.addWidget(QLabel(self.tr("<b>Líneas de código:</b>")), 4, 0)
        grid.addWidget(QLabel(self.tr("{0}").format(editor.lines() -
                       len(self.get_comment_spaces(editor)))), 4, 1)
        grid.addWidget(QLabel(
            self.tr("<b>Comentarios y líneas en blanco:</b>")), 5, 0)
        grid.addWidget(QLabel(
            self.tr("{0}").format(len(self.get_comment_spaces(editor)))), 5, 1)
        grid.addWidget(QLabel(self.tr("<b>Total de líneas:</b>")), 6, 0)
        grid.addWidget(QLabel(str(editor.lines())), 6, 1)
        grid.addWidget(QLabel(self.tr("<b>Modificado:</b>")), 7, 0)
        grid.addWidget(QLabel(self.tr(self.get_modification(filename))), 7, 1)

        btn_aceptar = QPushButton(self.tr("Aceptar"))
        grid.addWidget(btn_aceptar, 8, 1, Qt.AlignRight)

        vLayout.addLayout(grid)

        btn_aceptar.clicked.connect(self.close)

    def get_type(self, filename):
        try:
            ext = filename.split('.')[-1]
            if ext == 'c':
                type_ = self.tr("Archivo fuente C")
            elif ext == 'h':
                type_ = self.tr("Archivo de Cabecera")
            elif ext == 's':
                type_ = self.tr("ASM")
            return type_
        except:
            return filename.split('.')[-1].upper()

    def get_size(self, filename):
        size = (float(QFile(filename).size() + 1023.0) / 1024.0)
        return str(size)

    def get_comment_spaces(self, editor):
        spaces = re.findall('(^\n)|(^(\s+)?//)|(^( +)?($|\n))',
                            editor.text(), re.M)
        return spaces

    def get_modification(self, filename):
        try:
            time = os.path.getmtime(filename)
            format_time = datetime.fromtimestamp(
                time).strftime("%Y-%m-%d %H:%M")
            return format_time
        except:
            return "-"
