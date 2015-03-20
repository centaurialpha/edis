# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)


import os
from cx_Freeze import setup, Executable

opt = {
    'build_exe': {
        'includes': ['PyQt4.QtNetwork'],
        'include_msvcr': True,
        'include_files': []}}

paquetes = []
for dir_path, dir_names, filenames in os.walk("src"):
    if '__pycache__' not in dir_path.split('/')[-1] and \
       '__init__.py' in filenames:
        paquete = dir_path.replace('/', '.')
        paquetes.append(dir_path)

exe = Executable(
    script="bin/edis",
    base='Win32GUI',
    targetName='Edis.exe',
    compress=True,
    icon="edis_build/win/edis.ico"
    )

setup(
    name='Edis',
    version='1.0',
    author='Edis Team',
    options=opt,
    packages=paquetes,
    package_data={},
    executables=[exe]
    )
