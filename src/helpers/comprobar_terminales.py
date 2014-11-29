# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from subprocess import Popen, PIPE


def comprobar():
    """ Devuelve una lista con las terminales disponibles en el sistema. """

    terminales = [
        "gnome-terminal",
        "x-terminal-emulator",
        "terminator",
        "guake",
        "lxterminal",
        "yakuake",
        "eterm",
        "rxvt",
        "wterm",
        "konsole",
        "xterm"
        ]

    ex = {}
    instaladas = []
    terminales = [terminales] if isinstance(terminales, str) else terminales
    for terminal in terminales:
        try:
            Popen([terminal, '--help'], stdout=PIPE, stderr=PIPE)
            ex[terminal] = True
        except OSError:
            ex[terminal] = False
    [instaladas.append(terminal) for terminal in terminales
        if ex[terminal]]

    return instaladas
