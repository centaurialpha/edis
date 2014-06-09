#-*- coding: utf-8 -*-

from PyQt4.QtGui import QTabWidget
#from PyQt4.QtGui import QColor
from PyQt4.QtGui import QMessageBox

from PyQt4.QtCore import SIGNAL
#from PyQt4.QtCore import Qt

from side_c.interfaz.editor import editor
#from side_c import recursos


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

    def _esta_abierto(self, nombre):
        for i in range(self.count()):
            if self.widget(i) == nombre:
                return True
        return False

    def _mover_tab(self, nombre):
        for i in range(self.count()):
            if self.widget(i) == nombre:
                self.setCurrentIndex(i)
                return

    def tab_es_modificado(self, v):
        e = self.currentWidget()
        texto = unicode(self.tabBar().tabText(self.currentIndex()))

        if isinstance(e, editor.Editor) and self.no_esta_abierto and v \
        and not texto.startswith('* '):
            editor.texto_modificado = True
            t = '* %s' % self.tabBar().tabText(self.currentIndex())
            self.tabBar().setTabText(self.currentIndex(), t)

    def tab_guardado(self, e):
        indice = self.indexOf(e)
        texto = unicode(self.tabBar().tabText(indice))

        if texto.startswith('* '):
            texto = texto[2:]
        self.tabBar().setTabText(indice, texto)

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
            if isinstance(w, editor.Editor):
                v = QMessageBox.No
                if w.texto_modificado:
                    nombre = self.tabBar().tabText(self.currentIndex())
                    v = QMessageBox.question(self,
                        (self.tr('El archivo %s no esta guardado') %
                        nombre), self.tr("¿Guardar antes de cerrar?"),
                            QMessageBox.Yes | QMessageBox.No |
                            QMessageBox.Cancel)

                if v == QMessageBox.Yes:
                    self.emit(SIGNAL("saveActualEditor()"))
                    if w.texto_modificado:
                        return
                if v == QMessageBox.Cancel:
                    return

            super(TabCentral, self).removeTab(indice)
            if self.currentWidget() is not None:
                self.currentWidget().setFocus()
            else:
                self.emit(SIGNAL("allTabsClosed()"))
            del w
            self.actualizar_widget_actual()