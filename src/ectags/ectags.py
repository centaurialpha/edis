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
    #harvester = kind_harvester()
    #harvester.process_tag_list(tag_file.tags)
    #kinds = harvester.get_data()

    print(kinds)


generate_tag_file('/home/gabo/prueba.c')