# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)


class TabItem(object):

    def __init__(self):
        self._id = "Nuevo_archivo"

    def get_id(self):
        return self._id

    def set_id(self, id_):
        self._id = id_
        if id_:
            self.nuevo_archivo = False

    iD = property(lambda self: self.get_id(), lambda self,
        nombre: self.set_id(nombre))
