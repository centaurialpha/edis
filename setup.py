# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os
import sys
from distutils.core import setup

MODULOS = [
    ('PyQt4', 'http://riverbankcomputing.co.uk/software/pyqt/intro'),
    ('PyQt4.Qsci', 'http://riverbankcomputing.co.uk/software/qscintilla/intro')
    ]

for nombre_modulo, link in MODULOS:
    try:
        desde = 'PyQt4' if nombre_modulo == 'PyQt4.Qsci' else ''
        __import__(nombre_modulo, fromlist=desde)
    except ImportError:
        print("El módulo %s no está instalado.\n%s para más info." %
                (nombre_modulo, link))
        sys.exit(1)

from src import ui


def _paquetes():
    paquetes = []
    for e in os.listdir(os.getcwd()):
        if os.path.isdir(e) and not e.startswith('.'):
            for f in os.walk(e):
                if f[0].split('/')[-1].startswith('__pycache__'):
                    sin_pycache = '/'.join(f[0].split('/')[:-1])
                    paquetes.append(sin_pycache)
    return paquetes

setup(
    name=ui.__nombre__,
    version=ui.__version__,
    description=ui.__descripcion__,
    author='Gabriel Acosta',
    author_email='acostadariogabriel@gmail.com',
    url=ui.__codigo_fuente__,
    include_package_data=True,
    package_data={'': ['*.png', '*.qss', '*.qml']},
    packages=_paquetes(),
    scripts=['edis.py']
    )