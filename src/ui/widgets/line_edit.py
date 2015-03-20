# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import QLineEdit

from src import recursos


class CustomLineEdit(QLineEdit):

    """ QLineEdit personalizado """

    def __init__(self, parent=None):
        super(CustomLineEdit, self).__init__()

    def update(self, found):
        if not found:
            self.setStyleSheet('background: %s; border-radius: 3px' %
                               recursos.TEMA['error'])
        else:
            self.setStyleSheet('color: #dedede')
