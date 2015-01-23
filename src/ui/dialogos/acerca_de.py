# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import webbrowser

from PyQt4.QtGui import (
    QDialog,
    QTabWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QPushButton,
    QWidget,
    QPixmap,
    QLabel
    )

from src import recursos
from src import ui


class AcercaDe(QDialog):

    def __init__(self, parent=None):
        super(AcercaDe, self).__init__(parent)
        self.setWindowTitle(self.tr("Acerca de EDIS"))
        self.setMinimumWidth(400)
        box = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.tabs.addTab(AboutTab(), self.tr("Acerca de"))
        self.tabs.addTab(ReportarBugTab(), self.tr("Reportar bug"))
        box.addWidget(self.tabs)

        box_boton = QHBoxLayout()
        box_boton.addSpacerItem(QSpacerItem(1, 0, QSizePolicy.Expanding))
        boton_ok = QPushButton(self.tr("Ok"))
        box_boton.addWidget(boton_ok)
        box.addLayout(box_boton)

        boton_ok.clicked.connect(self.close)


class AboutTab(QWidget):

    def __init__(self):
        super(AboutTab, self).__init__()
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        lbl_version = QLabel(self.tr("Versión: %s") % ui.__version__)
        lbl_link = QLabel("<a href='%s'><span style='color: #dedede;'>%s</span>"
                          "</a>" % (ui.__web__, ui.__web__))
        logo = QPixmap(recursos.ICONOS['about'])
        label_logo = QLabel()
        label_logo.setPixmap(logo)
        box.addWidget(label_logo)
        box.addWidget(lbl_version)
        box.addWidget(lbl_link)

        lbl_link.linkActivated.connect(lambda link: webbrowser.open(link))


class ReportarBugTab(QWidget):

    def __init__(self):
        super(ReportarBugTab, self).__init__()
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        lbl_issues = QLabel(self.tr("Detalla el bug o sugerencia en:"))
        lbl_link_issues = QLabel("<a href='%s'><span style='color: #dedede;'>%s"
                                 "</span></a>" % (ui.__reportar_bug__,
                                 ui.__reportar_bug__))

        lbl_email = QLabel(self.tr("O puedes mandar un e-mail a:"))
        lbl_link_email = QLabel("<a href='%s'><span style='color: #dedede;'>%s"
                                "</span></a>" % (ui.__email_autor__,
                                ui.__email_autor__))
        box.addWidget(lbl_issues)
        box.addWidget(lbl_link_issues)
        box.addWidget(lbl_email)
        box.addWidget(lbl_link_email)
        box.addItem(QSpacerItem(1, 0, QSizePolicy.Expanding,
                    QSizePolicy.Expanding))