# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

"""
Sintaxis - Lenguaje C
"""

sintax = {
  "comment": [
    "//"
  ],
  "multiline_comment": {
    "open": "/*",
    "close": "*/"
  },
  "extension": [
    "c"
  ],
    "braces": [
        '\(', '\)',
        '\[', '\]',
        '\{', '\}'
        ],
  "string": [
    "\""
  ],
  "operators": [
    "=",
    "==",
    "!=",
    "<",
    "<=",
    ">",
    ">=",
    "\\+",
    "-",
    "\\*",
    "/",
    "//",
    "\\%",
    "\\*\\*",
    "\\+=",
    "-=",
    "\\*=",
    "/=",
    "\\%=",
    "!",
    "\\^",
    "\\|",
    "\\&",
    "\\~",
    ">>",
    "<<"
  ],
  "types": [
      "char",
      "double",
      "float",
      "int",
      "long",
      "register",
      "short",
      "signed",
      "static",
      "unsigned",
      "void",
      "volatile"
      ],
  "keywords": [
    "auto",
    "break",
    "case",
    "const",
    "continue",
    "default",
    "do",
    "else",
    "enum",
    "extern",
    "for",
    "goto",
    "if",
    "return",
    "sizeof",
    "struct",
    "switch",
    "typedef",
    "union",
    "while"
  ]
}