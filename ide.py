#-*- coding: utf-8 -*-

from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QDesktopWidget

from side_c.gui.menu import menu_acerca_de
from side_c.gui.menu import menu_archivo


class IDE(QMainWindow):

    def __init__(self):
        super(IDE, self).__init__()
        self.setMinimumSize(800, 600)
        self.setWindowTitle('SIDE-C')
        get_pantalla = QDesktopWidget().screenGeometry()
        self.posicionar_ventana(get_pantalla)

        # Menu
        menu = self.menuBar()
        archivo = menu.addMenu(self.tr("&Archivo"))
        editar = menu.addMenu(self.tr("&Editar"))
        acerca = menu.addMenu(self.tr("Acer&ca de"))

        self._menu_archivo = menu_archivo.MenuArchivo(archivo, self)
        self._menu_acerca_de = menu_acerca_de.MenuAcercade(acerca, self)

    def posicionar_ventana(self, pantalla):
        """ Posiciona la ventana en el centro de la pantalla. """

        tam_ventana = self.geometry()

        self.move((pantalla.width() - tam_ventana.width()) / 2,
            (pantalla.height() - tam_ventana.height()) / 2)


def main():
    app = QApplication(sys.argv)

    widget = IDE()
    widget.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    import sys
    main()