# -*- coding: utf-8 -*-

# Copyright (C) <2014>  <Gabriel Acosta>
# This file is part of EDIS.

# EDIS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# EDIS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with EDIS.  If not, see <http://www.gnu.org/licenses/>.


from subprocess import Popen, PIPE

"""
COMANDO = ctags -n --fields=fiKmnsSzt -f  - filename

"""


def get_ctags():
    """ Return True if ctags is installed or False is not installed. """

    command = ["ctags", "--version"]
    try:
        process = Popen(command, 0, stdout=PIPE, stderr=PIPE, shell=False)
        if process.communicate()[0]:
            return True
    except:
        return False


class CTags:

    def __init__(self):
        self.tags = None

    def start_ctags(self, filename):
        """ Run the command ctags """

        cmd = ["ctags", "-n", "--fields=fimKnsSzt", "-f", "-", filename]
        process = Popen(cmd, 0, stdout=PIPE, stderr=PIPE, shell=False)
        tag = process.communicate()[0]

        return tag


class Parser(object):

    def __init__(self):
        self._symbols = {}

    @property
    def symbols(self):
        return self._symbols

    def parser_tag(self, tag):
        """
        Parse the tag for obtain the symbols of source code.

        functions = {name: [line, definition]}
        variables = {name: line}
        structs = {name: {line: [members]}}

        """

        symbols = dict()
        functions = dict()
        variables = dict()
        structs = dict()
        members = dict()
        enums = dict()
        enumerators = dict()

        for line in tag.splitlines():
            name = None
            type_ = None
            nline = None
            definition = None
            for e, v in enumerate(line.split('\t')):
                if e == 0:
                    name = v.split(':')[-1]
                if e == 3:
                    type_ = v.split(':')[-1]
                if e == 4:
                    nline = v.split(':')[-1]
                if e == 5:
                    definition = v.split(':')[-1]

            if type_ == 'function':
                functions[name] = [nline, definition]
            if type_ == 'variable':
                variables[name] = nline
            if type_ == 'enum':
                enums[name] = {nline: []}
            if type_ == 'struct':
                structs[name] = {nline: []}
            if type_ == 'enumerator':
                if not definition in enumerators:
                    enumerators[definition] = [name]
                else:
                    enumerators[definition].append(name)
            if type_ == 'member':
                if not definition in members:
                    members[definition] = [name]
                else:
                    members[definition].append(name)

        for k in list(members.keys()):
            for m in members[k]:
                key = list(structs[k].keys()).pop()
                structs[k][key].append(m)

        for e in list(enumerators.keys()):
            for en in enumerators[e]:
                key = list(enums[e].keys()).pop()
                enums[e][key].append(en)

        if functions:
            symbols['functions'] = functions
        if variables:
            symbols['variables'] = variables
        if structs:
            symbols['structs'] = structs
        if enums:
            symbols['enums'] = enums
        self._symbols = symbols

        #FIXME: Obtener números de miembros y enumerators