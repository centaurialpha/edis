# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtCore import QObject

from src.ui.contenedores.lateral import (
    arbol_simbolos,
    navegador,
    explorador
    )
from src.ectags import ectags


class ContenedorLateral(QObject):

    def __init__(self, parent=None):
        super(ContenedorLateral, self).__init__()
        self.simbolos = arbol_simbolos.ArbolDeSimbolos()
        self.ctags = ectags.Ctags()
        self.navegador = navegador.Navegador()
        self.explorador = explorador.Explorador()

    def actualizar_simbolos(self, archivo):
        if archivo == 'Nuevo_archivo':
            return
        tag = self.ctags.run_ctags(archivo)
        simbolos = self.ctags.parser(tag)
        self.simbolos.actualizar_simbolos(simbolos)