#-*- coding: utf-8 -*-


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