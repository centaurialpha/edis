# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os
import shlex
from subprocess import Popen, PIPE
from src.core import (
    settings,
    paths
    )

if not settings.IS_LINUX:
    CTAGS = os.path.join(paths.PATH, "tools", "ctags", "ctags.exe")

# c: class name
# d: define (from #define XXX)
# e: enumerator
# f: function or method name
# F: file name
# g: enumeration name
# m: member (of structure or class data)
# n: namespace
# p: function prototype
# s: structure name
# t: typedef
# u: union name
# v: variable


class Tag(object):
    """ Representa un 'tag' del código fuente """

    def __init__(self, name):
        self.name = name
        self.type = None
        self.parent = {}


class CtagsParser(object):

    def __init__(self):
        self._tags = []

    def parse(self, filename):
        """ Ejecuta ctags """

        command = "ctags -n --fields=Sks -f - '%s'" % filename
        args = shlex.split(command)
        # Flag para ocultar la consola en Windows
        if not settings.IS_LINUX:
            CREATE_NO_WINDOW = 0x08000000
            process = Popen(args,
                            stdout=PIPE,
                            executable=CTAGS,
                            creationflags=CREATE_NO_WINDOW)
        else:
            process = Popen(args,
                            stdout=PIPE,
                            executable='ctags')
        self._parse_output(process.communicate()[0])

    def _parse_output(self, output):
        """ Analiza la salida de ctags y crea los objectos Tags """

        for line in output.splitlines():
            for i, field in enumerate(line.decode('utf-8').split('\t')):
                if i == 0:
                    tag = Tag(field)
                elif i == 2:
                    tag.lineno = field.rstrip(';"')
                elif i == 3:
                    tag.type = field
                elif i == 4:
                    key, value = field.split(':')
                    tag.parent[key] = value
            self._tags.append(tag)

    @property
    def tags(self):
        return self._tags


def get_symbols(filename):
    """ Analiza los objetos 'Tag' y arma la estructura de símbolos """

    # FIXME: mejorar el árbol en estructuras y enumeraciones

    symbols, symbols_combo = {}, {}
    variables = {}
    enums = {}
    structs = {}
    members = {}
    functions = {}

    ctags = CtagsParser()
    ctags.parse(filename)

    for token in ctags.tags:
        if token.type == 'f':
            functions[token.lineno] = token.name
            try:
                args = token.parent['signature']
            except:
                args = ''
            symbols_combo[int(token.lineno)] = (token.name + args, 'function')
        elif token.type == 'v' or token.type == 't':
            variables[token.name] = token.lineno
        elif token.type == 's':
            structs[token.lineno] = token.name
            symbols_combo[int(token.lineno)] = (token.name, 'struct')
        elif token.type == 'g':
            enums[token.lineno] = token.name
            symbols_combo[int(token.lineno)] = (token.name, 'enum')
        elif token.type == 'e':
            members[token.name] = (token.lineno, token.parent['enum'])
        elif token.type == 'm':
            members[token.name] = (token.lineno, token.parent['struct'])

    if functions:
        symbols['functions'] = functions
    if variables:
        symbols['globals'] = variables
    if enums:
        symbols['enums'] = enums
    if structs:
        symbols['structs'] = structs
    if members:
        symbols['members'] = members

    return symbols, symbols_combo