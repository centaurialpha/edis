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
    QGridLayout,
    QLabel,
    QLineEdit,
    QSpinBox,
    QPlainTextEdit,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QMessageBox,
    QComboBox
    )

from PyQt4.QtCore import (
    SIGNAL,
    )

from src.tools import code_pasting
from src.ui.widgets import loading_widget


class CodePastingDialog(QDialog):

    def __init__(self, parent=None, code=''):
        super(CodePastingDialog, self).__init__(parent)
        self.setWindowTitle(self.tr("Enviar a Pastebin"))
        self.setMinimumSize(700, 500)
        self._parent = parent
        container = QVBoxLayout(self)

        # Thread
        self.thread = code_pasting.Thread()
        self.connect(self.thread, SIGNAL("finished()"),
                     self._paste_result)
        # Campos
        fields_box = QGridLayout()
        fields_box.addWidget(QLabel(self.tr("Expirar después de:")), 0, 0)
        self._spin_expire = QSpinBox()
        self._spin_expire.setSuffix(self.tr(" Días"))
        self._spin_expire.setMinimum(1)
        fields_box.addWidget(self._spin_expire, 0, 1)
        fields_box.addWidget(QLabel(self.tr("Acceso:")), 1, 0)
        self._combo_access = QComboBox()
        self._combo_access.addItems([self.tr("Publico"), self.tr("Privado")])
        fields_box.addWidget(self._combo_access, 1, 1)
        fields_box.addWidget(QLabel(self.tr("Nombre:")), 2, 0)
        self._line_filename = QLineEdit()
        place_holder_text = parent.get_active_editor().filename
        self._line_filename.setPlaceholderText(place_holder_text)
        fields_box.addWidget(self._line_filename, 2, 1)
        fields_box.addWidget(QLabel(self.tr("Descripción:")), 3, 0)

        # Editor
        self._code_editor = QPlainTextEdit()
        self._set_editor_style(self._code_editor)
        self._code_editor.setPlainText(code)

        hbox = QHBoxLayout()
        hbox.addItem(QSpacerItem(0, 1, QSizePolicy.Expanding))
        btn_paste = QPushButton(self.tr("Enviar"))
        hbox.addWidget(btn_paste)
        btn_cancel = QPushButton(self.tr("Cancelar"))
        hbox.addWidget(btn_cancel)

        container.addLayout(fields_box)
        container.addWidget(self._code_editor)
        container.addLayout(hbox)

        # Loading widget
        self.loading_widget = loading_widget.LoadingWidget(self)
        self.loading_widget.hide()

        # Conexiones
        self.connect(btn_cancel, SIGNAL("clicked()"), self.close)
        self.connect(btn_paste, SIGNAL("clicked()"), self._emit_data)

    def _emit_data(self):
        code = self._code_editor.toPlainText()
        expire = str(self._spin_expire.value()) + 'D'
        paste_name = self._line_filename.text()
        if not paste_name:
            paste_name = self._parent.get_active_editor().filename
        self.loading_widget.show()
        self.thread.paste(code, paste_name, expire)

    def _paste_result(self):
        self.loading_widget.hide()
        result = self.thread.result
        if result is None:
            QMessageBox.critical(self, self.tr("Error!"),
                                 self.tr("No hay código"))
            return
        QMessageBox.information(self, self.tr("URL"),
                                str(result))
        self.close()

    def _set_editor_style(self, editor):
        style = 'QPlainTextEdit {color: #E2E2E5; background-color: #0E0F12; }'
        editor.setStyleSheet(style)

    def resizeEvent(self, event):
        super(CodePastingDialog, self).resizeEvent(event)
        self.loading_widget.resize(event.size())