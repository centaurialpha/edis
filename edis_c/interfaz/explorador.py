# -*- coding: utf-8 -*-

from PyQt4.QtGui import (
    QListView,
    QWidget,
    QStandardItemModel,
    QStandardItem,
    QVBoxLayout,
    QMenu,
    QAction
    )
from PyQt4.QtCore import (
    SIGNAL,
    QThread,
    Qt,
    QModelIndex,
    pyqtSlot
    )

from edis_c.interfaz.contenedor_principal import contenedor_principal
from edis_c.nucleo import logger
log = logger.edisLogger('edis_c.interfaz.explorador')


class Explorador(QWidget):

    def __init__(self, parent=None):
        super(Explorador, self).__init__(parent)
        self._parent = parent
        self.model = None
        self.archivos = []

        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        self.lista = ListView(self)
        vbox.addWidget(self.lista)
        self.hilo = ThreadArchivos(self)
        self.connect(self.hilo, SIGNAL("archivosRecibidos(QStringList)"),
            self.cargar_archivos)
        self.lista.clicked.connect(self.cambiar_tab)

    @pyqtSlot(QModelIndex)
    def cambiar_tab(self, indice):
        self.emit(SIGNAL("cambioPes(int)"), indice.row())

    def cargar_archivos(self, archivos):
        archivos = list(archivos)
        if self.model is None:
            self.model = QStandardItemModel(self.lista)
            for i in archivos:
                item = QStandardItem(i)
                self.model.appendRow(item)
        self.lista.setModel(self.model)

    def enterEvent(self, event):
        pass

    def leaveEvent(self, event):
        pass

    def cargar_archivo(self, archivos):
        if len(list(archivos)) == 1:
            archivo = list(archivos)[0]
            item = QStandardItem(archivo)
            self.model.appendRow(item)
        else:
            for i in archivos:
                item = QStandardItem(i)
                self.model.appendRow(item)

    def borrar_item(self, item):
        self.model.removeRow(item)

    def get_archivos(self):
        return contenedor_principal.ContenedorMain().get_archivos()

    def get_indice(self):
        print(self.model.currentIndex())

    def cambiar(self):
        pass


class ListView(QListView):

    def __init__(self, parent):
        super(ListView, self).__init__()
        self.parent = parent

    def contextMenuEvent(self, evento):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        menu = QMenu(self)
        accionC = QAction('Cerrar', self)
        menu.addAction(accionC)
        accionC.triggered.connect(self.parent.borrar_item)
        menu.exec_(evento.globalPos())


class ThreadArchivos(QThread):

    def __init__(self, parent):
        super(ThreadArchivos, self).__init__()
        self.arc = []

    def run(self):
        try:
            cp = contenedor_principal.ContenedorMain()
            archivos = cp.tab.get_archivos_para_hilo()
            self.emit(SIGNAL("archivosRecibidos(QStringList)"),
                archivos)
        except:
            log.error('Error en ejecución de thread!')