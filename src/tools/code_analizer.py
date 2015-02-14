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

from src.helpers import logger

log = logger.edis_logger.get_logger(__name__)
ERROR = log.error


def parse_symbols(source):
    """ Parsea el código fuente para obtener los símbolos:

        Estructuras, uniones, variables, funciones.
    """

    functions = {}
    structs = {}
    vars_globals = {}

    parser = c_parser.CParser()
    # AST Abstract Syntax Tree
    try:
        ast = parser.parse(source)
    except:
        ERROR('El código fuente tiene errores de sintáxis')
        return {}
    ast_objects = ast.ext
    for ast_object in ast_objects:
        if ast_object.__class__ is c_ast.FuncDef:
            function_name = ast_object.decl.name
            function_nline = ast_object.decl.coord.line
            functions[function_nline] = function_name
        elif ast_object.__class__ is c_ast.Decl:
            decl = ast_object.type
            if decl.__class__ is c_ast.Struct:
                struct_name = decl.name
                struct_nline = decl.coord.line
                members = parse_structs(ast_object)
                structs[struct_nline] = (struct_name, members)
            elif decl.__class__ is c_ast.TypeDecl:
                var_name = decl.declname
                var_nline = decl.coord.line
                vars_globals[var_name] = var_nline

    return {'functions': functions, 'structs': structs, 'globals': vars_globals}


def parse_structs(ast_object):
    """ Devuelve una lista con los miembros de una estructura """

    members_list = []
    members_dict = {}

    members = ast_object.type.decls

    for member in members:
        member_name = member.name
        member_nline = member.coord.line
        members_dict[member_name] = member_nline
    members_list.append(members_dict)

    return members_list


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