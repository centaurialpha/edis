# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import sys

from PyQt4.QtGui import QIcon

from PyQt4.QtCore import (
    QLocale,
    QTranslator,
    QLibraryInfo
    )
from src import recursos
from src.helpers import (
    configuracion,
    logger
    )

#lint:disable
import src.ui.central
from src.ui.widgets import barra_de_estado
import src.ui.contenedores.principal
import src.ui.menu.menu
#lint:enable
from src.ui.edis_main import EDIS

# Logger
log = logger.edisLogger('edis.run')


def correr_interfaz(app):
    log.debug('Iniciando...')
    configuracion.ESettings().cargar()
    import src.ui.inicio  # lint:ok
    # Traductor
    local = QLocale.system().name()
    qtraductor = QTranslator()
    qtraductor.load("qt_" + local, QLibraryInfo.location(
                    QLibraryInfo.TranslationsPath))

    edis = EDIS()
    app.setWindowIcon(QIcon(recursos.ICONOS['icon']))
    # Aplicar estilo
    with open(recursos.ESTILO) as tema:
        estilo = tema.read()
    app.setStyleSheet(estilo)
    edis.show()
    #edis.detectar_dependencias()
    sys.exit(app.exec_())