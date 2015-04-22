# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from urllib import (
    request,
    parse
    )

from PyQt4.QtCore import (
    QObject,
    pyqtSignal,
    QThread
    )

from src.core import exceptions


class CodePaste(QObject):

    PASTE_EXPIRE_ONE_HOUR = "1H"

    PASTE_API = "http://pastebin.com/api/api_post.php"
    PASTE_DEV_KEY = "6c71766cdadff9f33347e80131397ac2"

    # Señales
    pasteResult = pyqtSignal('QString')

    def __init__(self, code, paste_name=None, paste_private='0',
                 paste_expire_date=PASTE_EXPIRE_ONE_HOUR, paste_format='c',
                 username=None, password=None):
        QObject.__init__(self)
        self._code = code
        self._paste_name = paste_name
        self._paste_private = paste_private
        self._paste_expire_date = paste_expire_date
        self._paste_format = paste_format
        self._usename = username
        self._password = password

    @property
    def code(self):
        return self._code

    def paste(self):
        if not self.code:
            raise exceptions.NoPasteCodeError("No paste code was given")
        data = {
            #'api_option': "paste",
            'api_dev_key': CodePaste.PASTE_DEV_KEY,
            'api_paste_code': self.code,
            'api_paste_name': self._paste_name,
            'api_paste_private': self._paste_private,
            'api_paste_format': self._paste_format,
            'api_paste_expire_date': self._paste_expire_date,
            }
        response = request.urlopen(CodePaste.PASTE_API,
                                   parse.urlencode(data).encode('utf8'))
        result = response.read().decode('utf-8')
        return result


class Thread(QThread):

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        result = None
        try:
            cpaste = CodePaste(code=self._code,
                               paste_name=self._name,
                               paste_expire_date=self._expire)
            result = cpaste.paste()
        except exceptions.NoPasteCodeError:
            self.result = result
        self.result = result

    def paste(self, code, name, expire):
        self._code = code
        self._name = name
        self._expire = expire
        self.start()