# -*- coding: utf-8 -*-

# <Tupla de palabras reservadas de C.>
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