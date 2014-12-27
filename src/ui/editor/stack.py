# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import (
    QStackedWidget,
    QMessageBox
    )

from PyQt4.QtCore import (
    pyqtSignal
    )


class StackWidget(QStackedWidget):

    todo_cerrado = pyqtSignal()
    guardar_editor_actual = pyqtSignal(name="Guardar_Editor_Actual")
    archivo_modificado = pyqtSignal(bool)
    archivo_cerrado = pyqtSignal(int)

    def __init__(self, parent=None):
        super(StackWidget, self).__init__()
        self.no_esta_abierto = True
        self.editores = []

    def agregar_widget(self, widget):
        stack = self.addWidget(widget)
        self.editores.append(widget)
        self.cambiar_widget(stack)

    def editor_modificado(self, valor=True):
        weditor = self.widget_actual
        if valor and self.no_esta_abierto:
            weditor.texto_modificado = True
        else:
            weditor.texto_modificado = False
        self.archivo_modificado.emit(valor)

    def cerrar(self):
        self.eliminar_widget(self.widget_actual, self.indice_actual)

    def cerrar_todo(self):
        for indice in range(self.contar):
            self.eliminar_widget(self.widget_actual, 0)

    def cerrar_demas(self):
        self.insertWidget(0, self.widget_actual)
        for indice in range(self.contar):
            if self.contar > 1:
                self.eliminar_widget(self.widget_actual, 1)

    def archivos_sin_guardar(self):
        archivos = list()
        editores = len(self.editores)
        for indice in range(editores):
            editor = self.editores[indice]
            if editor.texto_modificado:
                archivos.append(editor.iD)
        return archivos

    def check_archivos_sin_guardar(self):
        valor = False
        for indice in range(self.contar):
            valor = valor or self.editor(indice).texto_modificado
        return valor

    def eliminar_widget(self, weditor, indice):
        if indice != -1:
            self.cambiar_widget(indice)

            SI = QMessageBox.Yes
            NO = QMessageBox.No
            CANCELAR = QMessageBox.Cancel

            respuesta = NO
            if weditor.texto_modificado:
                respuesta = QMessageBox.question(self, self.trUtf8(
                                                "Archivo no guardado"),
                                                self.trUtf8("El archivo "
                                                "<b>%s</b> no se ha guardado"
                                            "<br>¿ Guardar ?") % weditor.iD,
                                            SI | NO | CANCELAR)
                if respuesta == CANCELAR:
                    return
                elif respuesta == SI:
                    self.guardar_editor_actual.emit()
            self.removeWidget(weditor)  # Se elimina del stack
            del self.editores[indice]  # Se elimina de la lista
            self.archivo_cerrado.emit(indice)
            # Foco al widget actual
            if self.widget_actual is not None:
                self.widget_actual.setFocus()
            else:
                self.todo_cerrado.emit()

    def archivos_abiertos(self):
        archivos = list()
        for indice in range(self.contar):
            archivos.append(self.editor(indice).iD)
        return archivos

    def cambiar_widget(self, indice):
        self.setCurrentIndex(indice)

    @property
    def widget_actual(self):
        return self.currentWidget()

    @property
    def indice_actual(self):
        return self.currentIndex()

    @property
    def contar(self):
        return self.count()

    def editor(self, indice):
        return self.widget(indice)