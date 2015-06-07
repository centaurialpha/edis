# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import webbrowser

from PyQt4.QtGui import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QPushButton,
    QPixmap,
    QLabel
    )

from PyQt4.QtCore import (
    Qt,
    QEvent
    )

from src import ui
from src.ui.main import Edis


class AcercaDe(QDialog):

    def __init__(self, parent):
        QDialog.__init__(self, parent, Qt.WindowMinMaxButtonsHint)
        self.clicks = 0
        self.setWindowTitle(self.tr("Acerca de Edis"))
        self.setMinimumWidth(485)
        box = QVBoxLayout(self)
        self.label_logo = QLabel()
        self.label_logo.setPixmap(QPixmap(":image/edis"))
        title_label = QLabel(self.tr("<h1>Edis</h1>\n<i>a simple "
                                     "cross-platform IDE for C</i>"))
        title_label.setAlignment(Qt.AlignRight)
        box_logo = QHBoxLayout()
        box_logo.addWidget(self.label_logo)
        box_logo.addWidget(title_label)
        box.addLayout(box_logo)
        lbl_version = QLabel(self.tr("<b>Versión:</b> {0}").format(
                             ui.__version__))
        box.addWidget(lbl_version)
        http = "http://"
        lbl_link = QLabel("<b>Web:</b> <a href='%s'><span style='color: "
                          "#626655;'>%s</span></a>" % (ui.__web__,
                                                       ui.__web__.replace(
                                                           http, "")))
        lbl_sc = QLabel(self.tr("<b>Código fuente:</b> <a href='{0}'><span"
                        " style='color: #626655;'>{1}</span></a>").format(
                        ui.__source_code__,
                        ui.__source_code__.replace(http, "")))
        box.addWidget(lbl_link)
        box.addWidget(lbl_sc)
        # License
        box.addWidget(QLabel(self.tr("<b>Licencia:</b> <i>Edis</i> se "
                                     "distribuye bajo los términos de la "
                                     "licencia <b>GPLv3+</b>")))
        box.addWidget(QLabel(self.tr("<b>Autor:</b> {0}").format(
                      ui.__author__)))
        box.addWidget(QLabel(self.tr("<b>e-mail:</b> {0}").format(
                      ui.__email_author__)))
        # Thanks to
        lbl_contributors = QLabel(self.tr("Agradezco a los que <a href="
                                  "{0}><span style='color: #626655;'>"
                                  "contribuyeron</span></a> con Edis").format(
                                  ui.__contributors__))
        box.addWidget(lbl_contributors)

        box_boton = QHBoxLayout()
        box_boton.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Expanding))
        btn_ok = QPushButton(self.tr("Aceptar"))
        box_boton.addWidget(btn_ok)
        box.addLayout(box_boton)

        # Conexiones
        btn_ok.clicked.connect(self.close)
        lbl_link.linkActivated['QString'].connect(self._open_link)
        lbl_sc.linkActivated['QString'].connect(self._open_link)
        lbl_contributors.linkActivated['QString'].connect(self._open_link)
        self.label_logo.installEventFilter(self)

    def _open_link(self, link):
        webbrowser.open_new(link)

    def eventFilter(self, obj, event):
        if obj == self.label_logo and event.type() == QEvent.MouseButtonPress:
            self.clicks += 1
            if self.clicks == 6:
                self.close()
                editor_container = Edis.get_component("principal")
                editor_container.show_snake()
        return False