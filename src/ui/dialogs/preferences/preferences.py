# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from collections import OrderedDict

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

from src.ui.dialogs.preferences import (
    general_configuration,
    editor_configuration,
    theme_configuration
    )

#FIXME: Ejecución, compilación


class Preferences(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle(self.tr("Configurations - Edis"))
        self.general = general_configuration.GeneralConfiguration(self)
        self.editor = editor_configuration.EditorConfiguration()
        self.themes = theme_configuration.ThemeConfiguration()
        # Opacity effect
        self.effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.effect)
        self.animation = QPropertyAnimation(self.effect, "opacity")
        # valor: texto en combo, clave: instancia de widgets
        self.widgets = OrderedDict([
            ('General', self.general),
            ('Editor', self.editor),
            ('Style Sheet', self.themes)])

        self.load_ui()

        key_escape = QShortcut(QKeySequence(Qt.Key_Escape), self)
        self.connect(key_escape, SIGNAL("activated()"), self.close)
        self.connect(self.btn_cancel, SIGNAL("clicked()"), self.close)
        self.connect(self.btn_guardar, SIGNAL("clicked()"), self._guardar)

    def load_ui(self):
        container = QVBoxLayout(self)

        box = QHBoxLayout()
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(20)
        toolbar = QToolBar()
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        toolbar.setOrientation(Qt.Vertical)
        toolbar.setIconSize(QSize(30, 30))
        toolbar.setObjectName("preferencias")

        pref_general_action = toolbar.addAction(
            QIcon(":image/general-pref"), "General")
        pref_editor_action = toolbar.addAction(
            QIcon(":image/editor-pref"), "Editor")
        pref_style_action = toolbar.addAction(
            QIcon(":image/theme"), "Style Sheet")
        self.connect(pref_general_action, SIGNAL("triggered()"),
                     lambda: self.cambiar_widget(0))
        self.connect(pref_editor_action, SIGNAL("triggered()"),
                     lambda: self.cambiar_widget(1))
        self.connect(pref_style_action, SIGNAL("triggered()"),
                     lambda: self.cambiar_widget(2))

        box.addWidget(toolbar)

        self.stack = QStackedWidget()
        box.addWidget(self.stack)

        [self.stack.addWidget(widget)
            for widget in list(self.widgets.values())]

        box_buttons = QHBoxLayout()
        box_buttons.setMargin(10)
        box_buttons.setSpacing(10)
        box_buttons.addStretch(1)
        self.btn_cancel = QPushButton(self.tr("Cancel"))
        self.btn_guardar = QPushButton(self.tr("Save"))
        box_buttons.addWidget(self.btn_cancel)
        box_buttons.addWidget(self.btn_guardar)
        container.addLayout(box)
        container.addLayout(box_buttons)

    def mostrar(self):
        self.stack.setCurrentIndex(0)
        self.show()

    def cambiar_widget(self, index):
        if not self.isVisible():
            self.show()
        self.stack.setCurrentIndex(index)

    def _guardar(self):
        [self.stack.widget(i).guardar()
            for i in range(self.stack.count())]
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