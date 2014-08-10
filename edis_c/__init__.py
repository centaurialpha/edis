# -*- coding: utf-8 -*-

# Copyright (C) <2014>  <Gabriel Acosta>
# This file is part of EDIS-C.

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

from PyQt4.QtCore import QCoreApplication
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QStyleFactory
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QLocale
from PyQt4.QtCore import QTranslator
from PyQt4.QtCore import QLibraryInfo


from edis_c.nucleo import configuraciones
from edis_c import recursos
from edis_c.interfaz.ide.Ide import IDE

# METADATOS
__nombre__ = "EDIS-C"
__codigo_fuente__ = "http://github.com/centaurialpha/edis"
__version__ = "1.0-alpha"
__python__ = "https://www.python.org/"
__qt__ = "https://qt.digia.com/"
__pyqt__ = "http://www.riverbankcomputing.co.uk/software/pyqt/intro"
__reportar_bug__ = "http://github.com/centaurialpha/edis/issues"


# Correr Interfáz
def edis(app):
    QCoreApplication.setOrganizationName('EDIS-C')
    QCoreApplication.setOrganizationDomain('EDIS-C')
    QCoreApplication.setApplicationName('EDIS-C')

    # Ícono
    app.setWindowIcon(QIcon(recursos.ICONOS['icono']))
    # Estilo por defecto
    estilo = list(QStyleFactory.keys()).pop()
    QApplication.setStyle(QStyleFactory.create(estilo))
    # Splash
#    imagen_splash = QPixmap(':imagenes/splash')
#    splash = QSplashScreen(imagen_splash, Qt.WindowStaysOnTopHint)
#    splash.setMask(imagen_splash.mask())
#    splash.show()

    app.processEvents()

    # Idioma
    local = unicode(QLocale.system().name())
    # Diálogos en español
    qtTraductor = QTranslator()
    qtTraductor.load("qt_" + local,
        QLibraryInfo.location(QLibraryInfo.TranslationsPath))
    app.installTranslator(qtTraductor)

    configuraciones.cargar_configuraciones()

    edis = IDE()
    edis.show()

    #splash.finish(edis)

    sys.exit(app.exec_())
