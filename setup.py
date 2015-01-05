# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os
import sys
from distutils.core import setup

PYQT = ('PyQt4', 'http://riverbankcomputing.co.uk/software/pyqt/intro')
try:
    __import__(PYQT[0])
except ImportError:
    print("El módulo %s no está instalado.\n%s para más info." %
            (PYQT[0], PYQT[1]))
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