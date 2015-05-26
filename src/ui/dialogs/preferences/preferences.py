# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QIcon,
    QToolBar,
    QStackedWidget,
    QPushButton,
    QGraphicsOpacityEffect,
    QShortcut,
    QKeySequence
    )

from PyQt4.QtCore import (
    Qt,
    SIGNAL,
    QSize,
    QPropertyAnimation
    )

from src.ui.main import Edis


class Preferences(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle(self.tr("Configuraciones - Edis"))
        self.__sections = []
        # Opacity effect
        self.effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.effect)
        self.animation = QPropertyAnimation(self.effect, "opacity")

        Edis.load_component("preferences", self)
        # Install sections
        #lint:disable
        from src.ui.dialogs.preferences import (
            environment_configuration,
            editor_configuration,
            compiler_configuration
            )
        #lint:enable
        self.load_ui()
        key_escape = QShortcut(QKeySequence(Qt.Key_Escape), self)
        self.connect(key_escape, SIGNAL("activated()"), self.close)
        self.connect(self.btn_cancel, SIGNAL("clicked()"), self.close)
        self.connect(self.btn_guardar, SIGNAL("clicked()"), self._save)

    def install_section(self, obj):
        self.__sections.append(obj)

    def load_ui(self):
        container = QVBoxLayout(self)

        box = QHBoxLayout()
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)
        toolbar = QToolBar()
        toolbar.setToolButtonStyle(3)
        toolbar.setOrientation(Qt.Vertical)
        toolbar.setIconSize(QSize(30, 30))
        toolbar.setObjectName("preferencias")

        environment_section = toolbar.addAction(
            QIcon(":image/general-pref"), "Entorno")
        editor_section = toolbar.addAction(
            QIcon(":image/editor-pref"), "Editor")
        compiler_section = toolbar.addAction(
            QIcon(":image/compiler-pref"), "Compilador")
        self.connect(environment_section, SIGNAL("triggered()"),
                     lambda: self.change_widget(0))
        self.connect(editor_section, SIGNAL("triggered()"),
                     lambda: self.change_widget(1))
        self.connect(compiler_section, SIGNAL("triggered()"),
                     lambda: self.change_widget(2))

        # Set size
        for action in toolbar.actions():
            widget = toolbar.widgetForAction(action)
            widget.setFixedSize(80, 50)

        box.addWidget(toolbar)

        self.stack = QStackedWidget()
        box.addWidget(self.stack)

        # Load sections and subsections
        for section in self.__sections:
            for name, obj in list(section.get_tabs().items()):
                section.install_tab(obj, name)
            self.stack.addWidget(section)

        box_buttons = QHBoxLayout()
        box_buttons.setMargin(10)
        box_buttons.setSpacing(10)
        box_buttons.addStretch(1)
        self.btn_cancel = QPushButton(self.tr("Cancelar"))
        self.btn_guardar = QPushButton(self.tr("Guardar"))
        box_buttons.addWidget(self.btn_cancel)
        box_buttons.addWidget(self.btn_guardar)
        container.addLayout(box)
        container.addLayout(box_buttons)

    def change_widget(self, index):
        if not self.isVisible():
            self.show()
        self.stack.setCurrentIndex(index)

    def _save(self):
        for index in range(self.stack.count()):
            self.stack.widget(index).save()
        self.close()

    def close(self):
        super(Preferences, self).close()
        self.emit(SIGNAL("configurationsClose(PyQt_PyObject)"), self)

    def showEvent(self, event):
        super(Preferences, self).showEvent(event)
        self.animation.setDuration(400)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()


preferences = Preferences()