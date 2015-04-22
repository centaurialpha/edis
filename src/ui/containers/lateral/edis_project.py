# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

import os

from PyQt4.QtCore import QObject


class EdisProject(QObject):

    """ Esta clase representa un objeto Proyecto """

    def __init__(self, data):
        QObject.__init__(self)
        self._path = data.get('path')
        self._template = data.get('template')

    def __set_name(self, name):
        self._name = name

    def __get_name(self):
        return self._name

    name = property(__get_name, __set_name)

    @property
    def project_path(self):
        return self._path

    @property
    def project_file(self):
        epf_file = os.path.join(self._path, self.name.lower() + '.epf')
        return epf_file

    @property
    def template(self):
        return self._template