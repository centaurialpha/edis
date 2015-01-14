# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os
import sys
from distutils.command.install import install
from distutils.core import setup

MODULOS = [
    ('PyQt4', 'http://riverbankcomputing.co.uk/software/pyqt/intro'),
    ('PyQt4.Qsci', 'http://riverbankcomputing.co.uk/software/qscintilla/intro')
    ]

# Se verifica dependencias de módulos
for nombre_modulo, link in MODULOS:
    try:
        desde = 'PyQt4' if nombre_modulo == 'PyQt4.Qsci' else ''
        __import__(nombre_modulo, fromlist=desde)
    except ImportError:
        print("El módulo %s no está instalado.\n%s para más info." %
                (nombre_modulo, link))
        sys.exit(1)

from src import ui


class CustomInstall(install):

    """ Clase de instalación personalizada.

    Copia todos los archivos en el directorio "PREFIX/share/Edis"
    """

    def run(self):
        install.run(self)

        for script in self.distribution.scripts:
            script_path = os.path.join(self.install_scripts,
                                       os.path.basename(script))
            with open(script_path, 'r') as f:
                contenido = f.read()
            contenido = contenido.replace('@ INSTALLED_BASE_DIR @',
                                      self._custom_data_dir)
            with open(script_path, 'w') as f:
                f.write(contenido)

    def finalize_options(self):
        """ Después de la instalación """

        install.finalize_options(self)
        data_dir = os.path.join(self.prefix, "share",
                               self.distribution.get_name())
        if self.root is None:
            build_dir = data_dir
        else:
            build_dir = os.path.join(self.root, data_dir[1:])
        self.install_lib = build_dir
        self._custom_data_dir = data_dir


# Se compila la lista de paquetes
paquetes = []
for dir_path, dir_names, filenames in os.walk('src'):
    if not '__pycache__' in dir_path.split('/')[-1] and \
        '__init__.py' in filenames:
        paquete = dir_path.replace('/', '.')
        paquetes.append(paquete)


setup(
    name=ui.__nombre__.title(),
    version=ui.__version__,
    description=ui.__descripcion__,
    author=ui.__autor__,
    author_email=ui.__email_autor__,
    url=ui.__codigo_fuente__,
    license='GPL v3',
    long_description=open('README.rst').read(),
    package_data={
        'src': ['images/*', 'extras/temas/*', 'ui/selector/*']
        },
    packages=paquetes,
    scripts=['edis'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Text Editors :: Integrated Development Environments (IDE)',
        'Topic :: Utilities'
        ],
    cmdclass={'install': CustomInstall},
    )