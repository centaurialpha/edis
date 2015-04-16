# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

""" Parser para la línea de comandos """

import argparse

#FIXME: Completar


def parse():
    files = None

    parser = argparse.ArgumentParser()
    parser.add_argument('file', metavar='file', type=str, nargs='*')
    args = parser.parse_args()
    files = args.file
    return files