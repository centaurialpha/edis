#-*- coding: utf-8 -*-

# <Archivo principal, para correr el programa se debe ejecutar este archivo.>
# Copyright (C) <2014>  <Gabriel Acosta>

# EDIS-C is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# EDIS-C is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with EDIS-C.  If not, see <http://www.gnu.org/licenses/>.

import sys
#import time

from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QSplashScreen
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QIcon

from PyQt4.QtCore import Qt
from PyQt4.QtCore import QCoreApplication

from edis_c import recursos
from edis_c.interfaz.ide import Ide


def main():
    app = QApplication(sys.argv)

    QCoreApplication.setOrganizationName('EDIS-C')
    QCoreApplication.setOrganizationDomain('EDIS-C')
    QCoreApplication.setApplicationName('EDIS-C')

    app.setWindowIcon(QIcon(recursos.ICONOS['seiryu_icono']))

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
#    time.sleep(2)
    side = Ide.IDE()
    side.show()

    splash.finish(side)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()