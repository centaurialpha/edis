#-*- coding: utf-8 -*-

# Copyright 2014 - Gabriel Acosta
# License: MIT
# Verificar terminales

from subprocess import Popen
from subprocess import PIPE


def comprobar():
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