# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import re
import os
import sys

from src.tools.pycparser import (
    parse_file,
    c_ast
    )

from src.helpers import logger
from src import paths

log = logger.edis_logger.get_logger(__name__)
ERROR = log.error

path = os.path.join(paths.PATH, "tools", "pycparser")
#path = os.path.join(os.path.dirname(os.path.relpath(__file__)), "pycparser")
# Fake libc
fake_libc = os.path.join(path, "fake_libc_include")
fake_libc = '-I' + fake_libc
# CPP path
cpp_path = os.path.join(path, "cpp.exe") if sys.platform == 'win32' else 'cpp'
ERROR("%s", cpp_path)


class NodeVisitor(c_ast.NodeVisitor):

    """ Nodo visitador: basado en la clase NodeVisitor de c_ast.
            cada método visit_XXX visita la clase XXX.
            Por ejemplo, el método visit_FuncDef visita la clase FuncDef,
            analiza una función armando una estructura tipo diccionario que
            será utilizado por el IDE para armar el árbol de símbolos.
    """

    def __init__(self):
        super(NodeVisitor, self).__init__()
        self.functions = {}
        self.globals = {}
        self.structs = {}
        self.members = {}
        self.symbols_combo = {}
        self.params = []

    def visit_FuncDef(self, node):
        decl = node.decl
        function_name = decl.name
        function_nline = decl.coord.line
        if decl.type.args is not None:
            # Parámetros de la función
            for param in decl.type.args.params:
                _type = param.type
                if isinstance(_type, c_ast.PtrDecl):
                    param_name = _type.type
                    if isinstance(param_name, c_ast.PtrDecl):
                        # Puntero a puntero
                        param_name = param_name.type.declname
                    else:
                        # Puntero
                        param_name = param_name.declname
                elif isinstance(_type, c_ast.TypeDecl):
                    param_name = param.name
                    if param_name is None:
                        param_name = ""
                self.params.append(param_name)
        self.functions[function_nline] = function_name
        args = '(' + ', '.join(self.params) + ')'
        self.symbols_combo[function_nline] = (function_name + args, 'function')
        # Reiniciar parámetros
        self.params = []

    def visit_Decl(self, node):
        global_name = node.name
        global_nline = node.coord.line
        self.globals[global_name] = global_nline

    def visit_Struct(self, node):
        struct_name = node.name
        struct_nline = node.coord.line
        # Miembros de la estructura
        for member in node.decls:
            member_name = member.name
            member_nline = member.coord.line
            self.members[member_name] = member_nline
        self.structs[struct_nline] = (struct_name, self.members)
        self.symbols_combo[struct_nline] = (struct_name, 'struct')


def parse_symbols(filename):
    """ Analiza el código fuente y genera el árbol de símbolos """

    symbols = {}
    symbols_combo = None
    try:
        ast = parse_file(filename, use_cpp=True, cpp_path=cpp_path,
                         cpp_args=fake_libc)
    except Exception as reason:
        ERROR('El código fuente tiene errores de sintáxis: %s', reason)
        return {}, {}
    visitor = NodeVisitor()
    visitor.visit(ast)
    if visitor.functions:
        symbols['functions'] = visitor.functions
    if visitor.structs:
        symbols['structs'] = visitor.structs
    if visitor.globals:
        symbols['globals'] = visitor.globals
    symbols_combo = visitor.symbols_combo
    return symbols, symbols_combo


def sanitize_source_code(source_code):
    """ Limpia el código fuente para poder ser analizado por pycparser """

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