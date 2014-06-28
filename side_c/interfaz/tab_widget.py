#-*- coding: utf-8 -*-

from PyQt4.QtGui import QTabWidget
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QMessageBox

from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import Qt

from side_c.interfaz.editor import editor


class TabCentral(QTabWidget):

    def __init__(self, parent):
        QTabWidget.__init__(self, parent)

        self.setTabsClosable(True)
        self.setMovable(True)
        self.setAcceptDrops(True)
        self.parent = parent
        self.no_esta_abierto = True

        self.connect(self, SIGNAL("tabCloseRequested(int)"),
            self.removeTab)

    def agregar_tab(self, widget, titulo, index=None):

        if index is not None:
            insertar = self.insertTab(index, widget, titulo)
        else:
            insertar = self.addTab(widget, titulo)

        self.setCurrentIndex(insertar)
        widget.setFocus()

        return insertar

    def cerrar_tab(self):
        """ Cierra la pestaña actual. """

        self.removeTab(self.currentIndex())

    def cerrar_todo(self):
        """ Cierra todas las pestañas. """

        for tab in range(self.count()):
            self.removeTab(0)

    def cerrar_excepto_actual(self):
        """ Cierrar todas las pestañas excepto la pestaña actual.
        """

        self.tabBar().moveTab(self.currentIndex(), 0)
        for tab in range(self.count()):
            if self.count() > 1:
                self.removeTab(1)

    def tab_es_modificado(self, v):
        e = self.currentWidget()
        #texto = str(self.tabBar().tabText(self.currentIndex()))

        #if isinstance(e, editor.Editor) and self.no_esta_abierto and v \
        #and not texto.startswith('* '):
            #t = '* %s' % self.tabBar().tabText(self.currentIndex())
            #self.tabBar().setTabText(self.currentIndex(), t)

        if isinstance(e, editor.Editor) and self.no_esta_abierto and v:
            e.texto_modificado = True
            self.tabBar().setTabTextColor(self.currentIndex(),
                QColor(Qt.red))

    def tab_guardado(self, e):
        indice = self.indexOf(e)
        #texto = str(self.tabBar().tabText(indice))

        #if texto.startswith('* '):
            #texto = texto[2:]
        self.tabBar().setTabTextColor(indice, QColor(70, 70, 70))

    def check_tabs_sin_guardar(self):
        """ Devuelve Verdadero si hay algún editor que fué modificado
        y no se han guardado los cambios """

        valor = False
        for i in range(self.count()):
            if isinstance(self.widget(i), editor.Editor):
                valor = valor or self.widget(i).texto_modificado

        return valor

    def devolver_archivos_no_guardados(self):
        """ Devuelve una lista de todos los archivos que han sido modificados
        y no se han guardado los cambios """

        archivos = []

        for i in range(self.count()):
            w = self.widget(i)
            if isinstance(w, editor.Editor) and w.texto_modificado:
                archivos.append(self.tabText(i))

        return archivos

    def focusInEvent(self, e):
        QTabWidget.focusInEvent(self, e)
        self.emit(SIGNAL("changeActualTab(QTabWidget)"), self)

        eW = self.currentWidget()
        if not eW:
            return
        if eW.nuevo_archivo:
            return

    def actualizar_widget_actual(self):
        if self.currentWidget() is not None:
            self.currentWidget().setFocus()
        else:
            self.emit(SIGNAL("allTabsClosed()"))

    def removeTab(self, indice):
        if indice != -1:
            self.setCurrentIndex(indice)
            w = self.currentWidget()

            SI = QMessageBox.Yes
            NO = QMessageBox.No
            CANCELAR = QMessageBox.Cancel

            if isinstance(w, editor.Editor):
                respuesta = NO
                if w.texto_modificado:
                    nombre = self.tabBar().tabText(self.currentIndex())
                    respuesta = QMessageBox.question(self,
                        (str(self.trUtf8('El archivo **%s no esta guardado')) %
                        str(nombre)), self.trUtf8("¿Guardar antes de cerrar?"),
                            SI | NO | CANCELAR)

                if respuesta == SI:
                    self.emit(SIGNAL("saveActualEditor()"))
                    if w.texto_modificado:
                        return
                elif respuesta == CANCELAR:
                    return

            super(TabCentral, self).removeTab(indice)
            if self.currentWidget() is not None:
                self.currentWidget().setFocus()
            else:
                self.emit(SIGNAL("allTabsClosed()"))
            del w
            self.actualizar_widget_actual()