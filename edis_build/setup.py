# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)


import os
from cx_Freeze import setup, Executable

include_files = []
#for dp, dns, filenames in os.walk('src'):
    #for i in filenames:

        #path = '/'.join(os.path.abspath(i).split('/')[:-1])
        #ext = i.split('.')[-1]
        #if ext == 'png':
            #path = os.path.join(path, "src", "images")
            #include_files.append((path, 'src/images/%s' % i))
        #elif ext == 'qss':
            #path = os.path.join(path, "src", "extras", "temas")
            #include_files.append((path, 'src/extras/temas/%s' % i))
        #elif ext == 'exe':
            #path = os.path.join(path, "src", "ectags")
            #include_files.append((path, 'src/ectags/%s' % i))
        #elif ext == 'qml':
            #path = os.path.join(path, "src", "ui")
            #include_files.append((path, 'src/ui/%s' % i))

#include_files = dict(include_files)
opt = {
    'build_exe': {
        'includes': ['PyQt4.QtNetwork'],
        'include_msvcr': True,
        'include_files': include_files}}

paquetes = []
for dir_path, dir_names, filenames in os.walk('src'):
    if not '__pycache__' in dir_path.split('/')[-1] and \
        '__init__.py' in filenames:
        paquete = dir_path.replace('/', '.')
        paquetes.append(dir_path)

exe = Executable(
    script='bin/edis',
    base='Win32GUI',
    targetName='Edis.exe',
    compress=True
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