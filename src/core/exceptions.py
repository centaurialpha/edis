# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)


class EdisIOError(Exception):
    pass


class EdisFileExistsError(Exception):

    def __init__(self, filename):
        super(EdisFileExistsError, self).__init__()
        self.filename = filename