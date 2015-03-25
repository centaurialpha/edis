# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import QLineEdit


class CustomLineEdit(QLineEdit):

    """ QLineEdit personalizado """

    def __init__(self, parent=None):
        super(CustomLineEdit, self).__init__()

    def update(self, found):
        if not found:
            self.setStyleSheet('border: 2px solid #DF3E3E; border-radius: 3px')
        else:
            self.setStyleSheet('border: 1px solid gray; border-radius: 2px')