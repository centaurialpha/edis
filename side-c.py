#-*- coding: utf-8 -*-
import sys
import time

from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QSplashScreen
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QIcon

from PyQt4.QtCore import Qt
from PyQt4.QtCore import QCoreApplication

from side_c import recursos
from side_c.interfaz.ide import Ide


def main():
    app = QApplication(sys.argv)

    QCoreApplication.setOrganizationName('SIDE-C')
    QCoreApplication.setOrganizationDomain('SIDE-C')
    QCoreApplication.setApplicationName('SIDE-C')

    app.setWindowIcon(QIcon(recursos.ICONOS['icono']))

    # Imágen SPLASH
    splash_imagen = QPixmap(recursos.ICONOS['splash'])
    splash = QSplashScreen(splash_imagen, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_imagen.mask())
    splash.show()
    app.processEvents()

    if sys.platform != 'win32':
        app.setCursorFlashTime(0)

    splash.showMessage("Cargando interfaz",
        Qt.AlignRight | Qt.AlignTop, Qt.white)
    time.sleep(2)
    side = Ide.IDE()
    side.show()

    splash.finish(side)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()