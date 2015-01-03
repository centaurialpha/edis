# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from subprocess import Popen, PIPE


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