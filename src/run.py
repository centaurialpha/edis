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
    QPixmap,
    )

from PyQt4.QtCore import (
    QLocale,
    QTranslator,
    QLibraryInfo,
    Qt
    )
from src import paths
from src.helpers.configurations import ESettings

# Se cargan las configuraciones
ESettings.cargar()
#lint:disable
from src.ui.widgets import status_bar
import src.ui.dock_manager
import src.ui.containers.editor_container
import src.ui.containers.output.output_container
import src.ui.containers.lateral.navigator
import src.ui.containers.lateral.explorer
import src.ui.containers.lateral.tree_symbols
#lint:enable
from src.ui.main import Edis


def run_edis(app):
    """ Se carga la interfáz """

    app.setWindowIcon(QIcon(":image/edis"))
    # Lenguaje
    local = QLocale.system().name()
    language = ESettings.get('general/language') + '.qm'
    if language:
        edis_translator = QTranslator()
        edis_translator.load(os.path.join(paths.PATH,
                             "extras", "i18n", language))
        app.installTranslator(edis_translator)
        # Qt translator
        qtranslator = QTranslator()
        qtranslator.load("qt_" + local, QLibraryInfo.location(
                         QLibraryInfo.TranslationsPath))
        app.installTranslator(qtranslator)
    pixmap = QPixmap(":image/splash")
    # Splash screen
    show_splash = False
    if ESettings.get('general/show-splash'):
        splash = Splash(pixmap, Qt.WindowStaysOnTopHint)
        splash.setMask(pixmap.mask())
        splash.show()
        app.processEvents()
        show_splash = True
    # GUI
    if show_splash:
        splash.showMessage("Loading UI...", Qt.AlignBottom | Qt.black)
    edis = Edis()
    edis.show()

    # Style Sheet
    style = ESettings.get('ventana/style-sheet')
    path_style = None
    style_sheet = None
    if style == 'Edark':
        path_style = os.path.join(paths.PATH, 'extras', 'temas', 'edark.qss')
    elif style != 'Default':
        path_style = os.path.join(paths.EDIS, style + '.qss')
    if path_style is not None:
        with open(path_style, mode='r') as f:
            style_sheet = f.read()
    app.setStyleSheet(style_sheet)
    # Archivos de última sesión
    files, recents_files = [], []
    if ESettings.get('general/load-files'):
        if show_splash:
            splash.showMessage("Loading files...", Qt.AlignBottom | Qt.black)
        files = ESettings.get('general/files')
        if files is None:
            files = []
        # Archivos recientes
        recents_files = ESettings.get('general/recents-files')
        if recents_files is None:
            recents_files = []
    edis.cargar_archivos(files, recents_files)
    if show_splash:
        splash.finish(edis)
    sys.exit(app.exec_())


class Splash(QSplashScreen):

    """ Custom Splash """

    def __init__(self, pix, flag):
        super(Splash, self).__init__(pix, flag)
        self.move(800, 410)