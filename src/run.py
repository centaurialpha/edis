# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import sys

from src import recursos
from src.helpers import (
    #configuraciones,
    logger
    )

#lint:disable
#from src.ui import central
#from src.ui.contenedores import principal
import src.ui.central
from src.ui.widgets import barra_de_estado
import src.ui.contenedores.principal
import src.ui.menu.menu
from src.ui.edis_main import EDIS
#lint:enable

# Logger
log = logger.edisLogger('edis.run')


def correr_interfaz(app):
    log.debug('Iniciando...')
    edis = EDIS()
    # Aplicar estilo
    with open(recursos.ESTILO) as tema:
        estilo = tema.read()
    app.setStyleSheet(estilo)
    edis.show()
    sys.exit(app.exec_())
    #sys.exit(app.exec_())
    #DEBUG('Corriendo interfaz')
    #t0 = time()
    #config = QSettings(recursos.CONFIGURACION, QSettings.IniFormat)
    #QCoreApplication.setOrganizationName('EDIS')
    #QCoreApplication.setOrganizationDomain('EDIS')
    #QCoreApplication.setApplicationName('EDIS')

    #app.setWindowIcon(QIcon(recursos.ICONOS['icono']))
    #imagenSplash = QPixmap(recursos.ICONOS['splash'])  # Splash
    #splash = QSplashScreen(imagenSplash, Qt.WindowStaysOnTopHint)
    #splash.setMask(imagenSplash.mask())
    #splash.show()

    #app.processEvents()

    # Idioma
    #local = unicode(QLocale.system().name())
    #qTraductor = QTranslator()
    #qTraductor.load("qt_" + local,
        #QLibraryInfo.location(QLibraryInfo.TranslationsPath))
    #app.installTranslator(qTraductor)

    # Se cargan las configuraciones
    #configuraciones.cargar_configuraciones()

    #edis = IDE()
    #splash.showMessage("Cargando GUI...",
                        #Qt.AlignCenter | Qt.AlignTop, Qt.black)
    # Carga de archivos abiertos desde la última sesión
    #DEBUG('Cargando archivos...')
    #archivos_abiertos = config.value('archivosAbiertos/mainTab', []).toList()
    #tmp = []
    #for archivo in archivos_abiertos:
        #d = archivo.toList()
        #if d:
            #tmp.append((unicode(d[0].toString()), d[1].toInt()[0]))
    #archivos_abiertos = tmp

    # Archivos recientes
    #recientes = config.value('archivosAbiertos/archivosRecientes', []).toList()
    #tmp = []
    #for archivo in recientes:
        #d = archivo.toString()
        #tmp.append(d)
    #recientes = tmp
    #if recientes is not None:
        #archivos_recientes = list(recientes)
    #else:
        #archivos_recientes = list()
    #archivos_recientes = [archivo for archivo in archivos_recientes]

    #archivos_abiertos_hilo = []
    #for i in range(len(archivos_abiertos)):
        #archivos_abiertos_hilo.append(archivos_abiertos[i][0])

    #edis.cargar_sesion(archivos_abiertos, archivos_recientes)

    #splash.finish(edis)
    #edis.explorador.navegador.hilo.start()
    #DEBUG('Tiempo: {0}'.format(time() - t0))