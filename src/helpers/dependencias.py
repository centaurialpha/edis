# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os
import sys
from subprocess import Popen, PIPE

from PyQt4.QtCore import QDir

LINUX = True if sys.platform == 'linux2' else False


def detectar_dependencias():
    dependencias = {
        'gcc': False,
        'ctags': False,
        'cppcheck': False
        }

    if LINUX:
        for dep in list(dependencias.keys()):
            proceso = Popen(dep + ' --version', stdout=PIPE, stderr=PIPE,
                            shell=True)
            if proceso.wait() == 0:
                dependencias[dep] = True
    else:
        #FIXME: cppcheck y ctags
        discos = []
        directorios = []
        for d in QDir.drives():
            discos += [QDir.toNativeSeparators(d.absolutePath())]
        for disco in discos:
            for carpeta in os.listdir(disco):
                directorios += [os.path.join(disco, carpeta)]
        for carpeta in directorios:
            for exe in list(dependencias.keys()):
                if exe == 'gcc':
                    exe += '.exe'
                    ejecutable = os.path.join(carpeta, "bin", exe)
                    if ("MinGW" in carpeta) and os.path.exists(ejecutable):
                        dependencias['gcc'] = ejecutable
