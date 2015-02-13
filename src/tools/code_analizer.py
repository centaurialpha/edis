# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import re
from pycparser import (
    c_parser,
    c_ast
    )


def parse_symbols(source):
    """ Parsea el código fuente para obtener los símbolos:

        Estructuras, variables, funciones.
    """

    functions = {}
    parser = c_parser.CParser()
    # AST Abstract Syntax Tree
    ast = parser.parse(source)
    ast_objects = ast.ext
    for ast_object in ast_objects:
        if ast_object.__class__ is c_ast.FuncDef:
            function_name = ast_object.decl.name
            function_nline = ast_object.decl.coord.line
            functions[function_nline] = function_name

    return {'functions': functions}


def sanitize_source_code(source_code):
    """ Ignora comentarios y declarativas """

    def blot_out_non_new_lines(str_in):
        return "" + ("\n" * str_in.count('\n'))

    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return blot_out_non_new_lines(s)
        else:
            return s
    source = ""
    for line in source_code.splitlines():
        if line.startswith('#'):
            source += '\n'
            continue
        source += line + '\n'
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE)
    return re.sub(pattern, replacer, source)