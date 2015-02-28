# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import sys
import os

from PyQt4.QtGui import (
    QIcon,
    QSplashScreen,
    QPixmap
    )

from PyQt4.QtCore import (
    QLocale,
    QTranslator,
    QLibraryInfo,
    Qt
    )
from src import paths
from src.helpers.configuracion import ESettings

# Se cargan las configuraciones
ESettings().cargar()
#lint:disable
from src.ui.widgets import barra_de_estado
import src.ui.dock_manager
import src.ui.contenedores.principal
import src.ui.contenedores.output.contenedor_secundario
import src.ui.contenedores.lateral.navegador
import src.ui.contenedores.lateral.explorador
import src.ui.contenedores.lateral.arbol_simbolos
#lint:enable
from src.ui.main import EDIS


def correr_interfaz(app):
    app.setWindowIcon(QIcon(":image/edis"))
    local = QLocale.system().name()
    qtraductor = QTranslator()
    qtraductor.load("qt_" + local, QLibraryInfo.location(
                    QLibraryInfo.TranslationsPath))
    pixmap = QPixmap(":image/splash")
    splash = Splash(pixmap, Qt.WindowStaysOnTopHint)
    splash.setMask(pixmap.mask())
    splash.show()
    app.processEvents()

    splash.showMessage("Cargado UI...", Qt.AlignBottom | Qt.black)
    edis = EDIS()
    edis.show()

    # Aplicar estilo
    with open(os.path.join(paths.PATH,
              "extras", "temas", "default.qss")) as tema:
        estilo = tema.read()
    app.setStyleSheet(estilo)
    # Archivos de última sesión
    splash.showMessage("Cargando archivos...", Qt.AlignBottom | Qt.black)
    files = ESettings.get('general/files')
    if files is None:
        files = []
    # Archivos recientes
    recents_files = ESettings.get('general/recents-files')
    if recents_files is None:
        recents_files = []
    edis.cargar_archivos(files, recents_files)
    splash.finish(edis)
    sys.exit(app.exec_())


class Splash(QSplashScreen):

    """ Custom Splash """

    def __init__(self, pix, flag):
        super(Splash, self).__init__(pix, flag)
        self.move(800, 410)