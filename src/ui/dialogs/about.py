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
    QLabel,
    QGroupBox
    )

from PyQt4.QtCore import (
    Qt,
    SIGNAL
    )

from src import ui


class AcercaDe(QDialog):

    def __init__(self, parent):
        QDialog.__init__(self, parent, Qt.WindowMinMaxButtonsHint)
        self.setWindowTitle(self.tr("About Edis"))
        self.setMinimumWidth(485)
        box = QVBoxLayout(self)
        label_logo = QLabel()
        label_logo.setPixmap(QPixmap(":image/edis"))
        title_label = QLabel(self.tr("<h1>Edis</h1>\n<i>a simple "
                                     "cross-platform IDE for C</i>"))
        title_label.setAlignment(Qt.AlignRight)
        box_logo = QHBoxLayout()
        box_logo.addWidget(label_logo)
        box_logo.addWidget(title_label)
        box.addLayout(box_logo)
        lbl_version = QLabel(self.tr("Version: {0}").format(ui.__version__))
        box.addWidget(lbl_version)
        lbl_link = QLabel("Web: <a href='%s'><span style='color: #0197FD;'>"
                          "%s</span></a>" % (ui.__web__, ui.__web__))
        lbl_sc = QLabel(self.tr("Source Code: <a href='{0}'><span style="
                        "'color: #0197FD;'>{1}</span></a>").format(
                        ui.__source_code__, ui.__source_code__))
        box.addWidget(lbl_link)
        box.addWidget(lbl_sc)
        # License
        box.addWidget(QLabel(self.tr("License: <b>Edis</b> is licensed under "
                                     "the terms of the <b>G</b>NU "
                                     "<b>P</b>ublic <b>L</b>icense "
                                     "version 3 or later.")))
        # Thanks to
        group = QGroupBox(self.tr("Edis Team:"))
        group.setStyleSheet("QGroupBox { font-size: 16px; padding: 10px;"
                            "margin-top: 10 5px; border: 1px solid gray; }"
                            "QGroupBox::title { "
                            "subcontrol-position: top center;"
                            "subcontrol-origin: margin; }")
        vbox = QVBoxLayout(group)
        vbox.setAlignment(Qt.AlignCenter)
        vbox.addWidget(QLabel("Gabriel Acosta <gabo>"))
        vbox.addWidget(QLabel("Martín Miranda <debianitram>"))
        vbox.addWidget(QLabel("Rodrigo Acosta <ekimdev>"))
        box.addWidget(group)

        box_boton = QHBoxLayout()
        box_boton.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Expanding))
        btn_ok = QPushButton(self.tr("Ok"))
        box_boton.addWidget(btn_ok)
        box.addLayout(box_boton)

        self.connect(btn_ok, SIGNAL("clicked()"), self.close)
        self.connect(lbl_link, SIGNAL("linkActivated(QString)"),
                     lambda link: webbrowser.open_new(link))
        self.connect(lbl_sc, SIGNAL("linkActivated(QString)"),
                     lambda link: webbrowser.open_new(link))
