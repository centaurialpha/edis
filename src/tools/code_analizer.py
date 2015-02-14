# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import re

from .pycparser import (
    c_parser,
    c_ast
    )


def parse_symbols(source):
    """ Parsea el código fuente para obtener los símbolos:

        Estructuras, uniones, variables, funciones.
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
        elif ast_object.__class__ is c_ast.Decl:
            if ast_object.type.__class__ is c_ast.Struct:
                parse_structs(ast_object)

    return {'functions': functions}


def parse_structs(ast_object):
    structs = {}
    _members = []

    members = ast_object.type.decls
    struct_name = ast_object.type.name
    struct_nline = ast_object.type.coord.line

    for member in members:
        member_name = member.name
        member_nline = member.coord.line
        _members.append({member_nline: member_name})

    print(_members)


def sanitize_source_code(source_code):
    """ Ignora comentarios y declarativas del preprocesador """

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