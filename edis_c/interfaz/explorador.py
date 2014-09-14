# -*- coding: utf-8 -*-

from PyQt4.QtGui import (
    QListView,
    QWidget,
    QStandardItemModel,
    QStandardItem,
    QVBoxLayout,
    QMenu,
    QAction,
    QTabWidget,
    QIcon,
    QTreeView,
    QFileSystemModel,
    )
from PyQt4.QtCore import (
    SIGNAL,
    QThread,
    Qt,
    QModelIndex,
    pyqtSlot,
    QStringList,
    QDir
    )

from edis_c.interfaz.contenedor_principal import contenedor_principal
#from edis_c.interfaz.editor.editor import Editor
from edis_c.nucleo import logger
from edis_c import recursos
log = logger.edisLogger('edis_c.interfaz.explorador')


class TabExplorador(QWidget):

    def __init__(self, parent=None):
        super(TabExplorador, self).__init__()
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(1)
        self.navegador = Navegador(self)
        self.explorador = Explorador(self)
        self.tabs.addTab(self.navegador,
            QIcon(recursos.ICONOS['navegador']), '')
        self.tabs.addTab(self.explorador,
            QIcon(recursos.ICONOS['explorador']), '')
        vbox.addWidget(self.tabs)


class Explorador(QWidget):
    """ Explorador de archivos basado en QFileSystemModel """

    def __init__(self, parent=None):
        super(Explorador, self).__init__()
        vb = QVBoxLayout(self)
        vb.setContentsMargins(0, 0, 0, 0)

        self.tree = QTreeView()
        self.tree.header().setHidden(True)
        self.tree.setAnimated(True)

        self.model = QFileSystemModel(self.tree)
        home_path = QDir.toNativeSeparators(QDir.homePath())
        self.model.setRootPath(home_path)
        filtro = QStringList("")
        filtro << "*.c" << "*.h"  # Filtro
        self.tree.setModel(self.model)
        self.tree.setRootIndex(QModelIndex(self.model.index(home_path)))
        self.model.setNameFilters(filtro)
        self.model.setNameFilterDisables(False)

        # Se ocultan algunas columnas (size, type, y date modified)
        self.tree.hideColumn(1)
        self.tree.hideColumn(2)
        self.tree.hideColumn(3)

        vb.addWidget(self.tree)

        # Conexión a slot
        self.tree.doubleClicked.connect(self.doble_click)

    @pyqtSlot(QModelIndex)
    def doble_click(self, i):
        ind = self.model.index(i.row(), 0, i.parent())
        archivo = self.model.filePath(ind)
        # Señal emitida -> ruta completa del archivo
        self.emit(SIGNAL("dobleClickArchivo(QString)"), archivo)


class Navegador(QWidget):

    def __init__(self, parent=None):
        super(Navegador, self).__init__(parent)
        self.parent = parent
        self.archivos = []

        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        self.lista = ListView(self)
        self.model = QStandardItemModel(self.lista)
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

        for i in archivos:
            item = QStandardItem(i)
            if str(i[-1]).startswith('h'):
                item.setIcon(QIcon(recursos.ICONOS['cabecera']))
            if str(i[-1]).startswith('c'):
                item.setIcon(QIcon(recursos.ICONOS['main']))

            self.model.appendRow(item)
        self.lista.setModel(self.model)

    def enterEvent(self, event):
        pass

    def leaveEvent(self, event):
        pass

    def cargar_archivo(self, archivos):
        #if isinstance(archivos, QString):
            #archivos = [str(archivos)]
        #self.model = QStandardItemModel(self.lista)
        #self.lista.setModel(self.model)
        #if len(list(archivos)) == 1:
            #archivo = list(archivos)[0]
            #item = QStandardItem(archivo)
            #self.model.appendRow(item)
        #else:
            #for i in archivos:
                #item = QStandardItem(i)
                #self.model.appendRow(item)
        pass

    def borrar_item(self, item):
        self.model.removeRow(item)

    def get_archivos(self):
        return contenedor_principal.ContenedorMain().get_archivos()

    def get_indice(self):
        pass

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

    def run(self):
        import time
        time.sleep(2)
        try:
            cp = contenedor_principal.ContenedorMain()
            archivos = cp.tab.get_archivos_para_hilo()
            self.emit(SIGNAL("archivosRecibidos(QStringList)"),
                archivos)
        except:
            log.error('Error en ejecución de thread!')