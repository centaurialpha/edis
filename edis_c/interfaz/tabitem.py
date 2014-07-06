#-*- coding: utf-8 -*-

# Copyright (C) <2014>  <Gabriel Acosta>

# EDIS-C is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# EDIS-C is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with EDIS-C.  If not, see <http://www.gnu.org/licenses/>.

class TabItem(object):

    def __init__(self):
        self._id = ""

    def get_id(self):
        return self._id

    def set_id(self, id_):
        self._id = id_
        if id_:
            self.nuevo_archivo = False

    ID = property(lambda self: self.get_id(), lambda self,
        nombre: self.set_id(nombre))