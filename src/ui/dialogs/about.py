# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
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

from PyQt4.QtCore import Qt

from src import ui


class AcercaDe(QDialog):

    def __init__(self, parent):
        QDialog.__init__(self, parent, Qt.WindowMinMaxButtonsHint)
        self.setWindowTitle(self.tr("Acerca de EDIS"))
        box = QVBoxLayout(self)
        label_logo = QLabel()
        label_logo.setPixmap(QPixmap(":image/edis"))
        label_titulo = QLabel(self.tr("<h1>EDIS</h1>\n<i>Simple Integrated "
                              "Development Environment</i>"))
        box_logo = QHBoxLayout()
        self.tabs = QTabWidget()
        self.tabs.addTab(AboutTab(), self.tr("Acerca de"))
        self.tabs.addTab(ReportarBugTab(), self.tr("Reportar bug"))
        box_logo.addWidget(label_logo)
        box_logo.addWidget(label_titulo)
        box.addLayout(box_logo)
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
        label_descripcion = QLabel(self.tr(
            "a simple cross-platform IDE for C"))
        lbl_link = QLabel("Web: <a href='%s'><span style='color: lightblue;'>"
                          "%s</span></a>" % (ui.__web__, ui.__web__))
        lbl_sc = QLabel(self.tr("Código fuente: <a href='%s'><span style="
                        "'color: lightblue;'>%s</span></a>" %
                                (ui.__codigo_fuente__, ui.__codigo_fuente__)))
        box.addWidget(label_descripcion)
        box.addWidget(lbl_version)
        box.addWidget(lbl_link)
        box.addWidget(lbl_sc)
        box.addItem(QSpacerItem(1, 0, QSizePolicy.Expanding,
                    QSizePolicy.Expanding))

        lbl_link.linkActivated.connect(lambda link: webbrowser.open(link))
        lbl_sc.linkActivated.connect(lambda link: webbrowser.open(link))


class ReportarBugTab(QWidget):

    def __init__(self):
        super(ReportarBugTab, self).__init__()
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        lbl_issues = QLabel(self.tr("Detalla el bug o sugerencia en:"))
        lbl_link_issues = QLabel("<a href='%s'><span style='color: lightblue;'>"
                                 "%s</span></a>" % (ui.__reportar_bug__,
                                                    ui.__reportar_bug__))

        lbl_email = QLabel(self.tr("O puedes mandar un e-mail a:"))
        lbl_link_email = QLabel("<a href='%s'><span style='color: lightblue;'>"
                                "%s</span></a>" % (ui.__email_autor__,
                                ui.__email_autor__))
        box.addWidget(lbl_issues)
        box.addWidget(lbl_link_issues)
        box.addWidget(lbl_email)
        box.addWidget(lbl_link_email)
        box.addItem(QSpacerItem(1, 0, QSizePolicy.Expanding,
                    QSizePolicy.Expanding))

        lbl_link_issues.linkActivated.connect(lambda l: webbrowser.open(l))
