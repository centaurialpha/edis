# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

# Test pyctags

from pyctags import exuberant_ctags

from pyctags.harvesters import (
    kind_harvester
    )


def generate_tag_file(filename):
    ctags = exuberant_ctags(files=[filename])
    tag_file = ctags.generate_object(
        generator_options={'--fields': 'fimKnsSzt', '-F': None})
    harvester = kind_harvester()
    harvester.process_tag_list(tag_file.tags)
    kinds = harvester.get_data()

    return kinds


def get_symbols(filename='/home/gabo/test.c'):
    kinds = generate_tag_file(filename)
    symbols = []

    for c in kinds:
        for i in range(len(kinds[c])):
            symbol = Symbol(type_=c)
            symbol.name = kinds[c][i].name
            symbol.line_number = kinds[c][i].line_number
            symbol.definition = kinds[c][i].pattern[2:-2]
            symbols.append(symbol)


class Symbol(object):

    def __init__(self, name='', line=None, type_=None):
        self.name = name
        self.line_number = line
        self.definition = ''
        self.members = {}
        self.type = type_


get_symbols()