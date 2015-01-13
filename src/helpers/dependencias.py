# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os
from subprocess import Popen, PIPE
from PyQt4.QtCore import QDir


#FIXME: Multiplataforma


def detectar_ejecutables():
    ejecutables = ['gcc.exe', 'cppcheck.exe', 'ctags.exe']
    path = {}
    discos = []
    directorios = []

    for d in QDir.drives():
        discos += [QDir.toNativeSeparators(d.absolutePath())]
    for disco in discos:
        for carpeta in os.listdir(disco):
            directorios += [os.path.join(disco, carpeta)]
    for carpeta in directorios:
        for e, exe in enumerate(ejecutables):
            if e == 0:
                carpeta_ejecutable = os.path.join(carpeta, "bin", exe)
                if ("MinGW" in carpeta) and os.path.exists(carpeta_ejecutable):
                    path['gcc'] = carpeta_ejecutable
    return path


def detectar():
    passed = False
    ejecutables = ['gcc', 'cppcheck']
    dependencias = {
        'gcc': False,
        'cppcheck': False
        }
    for ejecutable in ejecutables:
        proceso = Popen(ejecutable + ' --version', stdout=PIPE, stderr=PIPE,
                        shell=True)
        if proceso.wait() == 0:
            dependencias['gcc'] = True
            dependencias['cppcheck'] = True
    for d in list(dependencias.values()):
        if not d:
            break
        passed = True
    return passed, dependencias


detectar_ejecutables()