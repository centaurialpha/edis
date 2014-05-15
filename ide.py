#-*- coding: utf-8 -*-

from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QDesktopWidget
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QToolBar
from PyQt4.QtCore import Qt

from side_c.gui.menu import menu_archivo
from side_c.gui.menu import menu_editar
from side_c.gui.menu import menu_ver
from side_c.gui.menu import menu_codigo
from side_c.gui.menu import menu_acerca_de
from side_c import recursos


class IDE(QMainWindow):

    def __init__(self):
        super(IDE, self).__init__()
        self.setMinimumSize(800, 600)
        self.setWindowTitle('SIDE-C')
        get_pantalla = QDesktopWidget().screenGeometry()
        self.posicionar_ventana(get_pantalla)
        self.setWindowIcon(QIcon(recursos.ICONOS['icono']))

        # Barra de estado
        self.toolBar = self.statusBar()
        self.toolBar.showMessage("SIDE")

        # ToolBar
        self.toolbar = QToolBar(self)
        self.toolbar.setToolButtonStyle(Qt.ToolButtonIconOnly)

        # Menu
        menu = self.menuBar()
        archivo = menu.addMenu(self.tr("&Archivo"))
        editar = menu.addMenu(self.tr("&Editar"))
        ver = menu.addMenu(self.trUtf8("&Ver"))
        codigo = menu.addMenu(self.trUtf8("&Codigo fuente"))
        acerca = menu.addMenu(self.tr("Ace&rca de"))

        self._menu_archivo = menu_archivo.MenuArchivo(archivo, self)
        self._menu_editar = menu_editar.MenuEditar(editar, self)
        self._menu_ver = menu_ver.MenuVer(ver, self)
        self._menu_codigo = menu_codigo.MenuCodigoFuente(codigo, self)
        self._menu_acerca_de = menu_acerca_de.MenuAcercade(acerca, self)

    def posicionar_ventana(self, pantalla):
        """ Posiciona la ventana en el centro de la pantalla. """

        tam_ventana = self.geometry()

        self.move((pantalla.width() - tam_ventana.width()) / 2,
                  (pantalla.height() - tam_ventana.height()) / 2)
