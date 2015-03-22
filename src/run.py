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
    QToolTip,
    QFont
    )

from PyQt4.QtCore import (
    QLocale,
    QTranslator,
    QLibraryInfo,
    Qt
    )
from src import paths
from src.helpers import settings

# Se cargan las configuraciones
settings.load_settings()
#lint:disable
# Se crean los objetos
from src.ui.containers.lateral import (
    tab_container,
    explorer,
    tree_symbols
    )
from src.ui.containers import editor_container
from src.ui.containers.output import output_container
from src.ui.widgets import status_bar
#lint:enable
from src.ui.main import Edis


def run_edis(app):
    """ Se carga la interfáz """

    # Ícono
    app.setWindowIcon(QIcon(":image/edis"))
    # Lenguaje
    local = QLocale.system().name()
    language = settings.get_setting('general/language')
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
    if settings.get_setting('general/show-splash'):
        splash = Splash(pixmap, Qt.WindowStaysOnTopHint)
        splash.setMask(pixmap.mask())
        splash.show()
        app.processEvents()
        show_splash = True

    # Style Sheet
    style = settings.get_setting('window/style-sheet')
    path_style = None
    style_sheet = None
    if style == 'Edark':
        path_style = os.path.join(paths.PATH, 'extras', 'theme', 'edark.qss')
    elif style != 'Default':
        path_style = os.path.join(paths.EDIS, style + '.qss')
    if path_style is not None:
        with open(path_style, mode='r') as f:
            style_sheet = f.read()
    app.setStyleSheet(style_sheet)

    # Fuente en Tooltips
    QToolTip.setFont(QFont(settings.DEFAULT_FONT, 9))

    # GUI
    if show_splash:
        splash.showMessage("Loading UI...", Qt.AlignBottom | Qt.black)
    edis = Edis()
    edis.show()
    # Archivos de última sesión
    files, recents_files = [], []
    if settings.get_setting('general/load-files'):
        if show_splash:
            splash.showMessage("Loading files...", Qt.AlignBottom | Qt.black)
        files = settings.get_setting('general/files')
        if files is None:
            files = []
        # Archivos recientes
        recents_files = settings.get_setting('general/recents-files')
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
