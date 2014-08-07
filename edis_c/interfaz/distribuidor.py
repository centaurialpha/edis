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

# Módulos Python

# Módulos QtCore
from PyQt4.QtCore import QObject

# Módulos QtGui
from PyQt4.QtGui import QPrinter
from PyQt4.QtGui import QPrintPreviewDialog
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QFileDialog

# Módulos EDIS
from edis_c.nucleo import configuraciones
from edis_c.interfaz.dialogos import dialogo_insertar_include
from edis_c.interfaz.dialogos import dialogo_insertar_macro

__Instancia = None


# Singleton
def _Distribuidor(*args, **kw):
    global __Instancia
    if __Instancia is None:
        __Instancia = Distribuidor(*args, **kw)
    return __Instancia


class Distribuidor(QObject):
    """ Esta clase puede acceder a todos los contenedores,
        distribuyendo las acciones de los widgets. """
    _TUX = configuraciones.LINUX

    def __init__(self, edis):
        QObject.__init__(self)
        # Aplicación principal
        self.edis = edis

    def imprimir_documento(self):
        Weditor = self.edis.contenedor_principal.devolver_editor_actual()
        if Weditor is not None:
            nombre = 'Sin_nombre.pdf'
            impresora = QPrinter(QPrinter.HighResolution)
            impresora.setPageSize(QPrinter.A4)
            impresora.setOutputFileName(nombre)
            impresora.setDocName(nombre)

            vista = QPrintPreviewDialog(impresora)
            vista.paintRequested[QPrinter].connect(Weditor.print_)
            tam = QApplication.instance().desktop().screenGeometry()
            ancho = tam.width() - 100
            alto = tam.height() - 100
            vista.setMinimumSize(ancho, alto)
            vista.exec_()

    def insertar_include(self):
        Weditor = self.edis.contenedor_principal.devolver_editor_actual()
        if Weditor is not None:
            dialogo = dialogo_insertar_include.DialogoInsertarInclude(Weditor,
                self.edis)
            dialogo.show()

    def insertar_macro(self):
        Weditor = self.edis.contenedor_principal.devolver_editor_actual()
        if Weditor is not None:
            dialogo = dialogo_insertar_macro.DialogoInsertarMacro(Weditor,
                self.edis)
            dialogo.show()

    def estadisticas_de_archivo(self):
        Weditor = self.edis.contenedor_principal.devolver_editor_actual()
        if Weditor is not None:
            pass
            #FIXME:

    def exportar_como_pdf(self):
        Weditor = self.edis.contenedor_principal.devolver_editor_actual()
        if Weditor is not None:
            nombre = QFileDialog.getSaveFileName(Weditor,
                self.trUtf8("Exportar a PDF"), filter='(*.pdf)')
            nombre += '.pdf'
            if nombre:
                p = QPrinter(QPrinter.HighResolution)
                p.setPageSize(QPrinter.A4)
                p.setColorMode(QPrinter.Color)
                p.setOutputFormat(QPrinter.PdfFormat)
                p.setOutputFileName(nombre)
                Weditor.document().print_(p)
        #FIXME: Mover a un helper

    def recargar_barra_de_herramientas(self):
        self.edis.cargar_toolbar()

    def compilar(self):
        Weditor = self.edis.contenedor_principal.devolver_editor_actual()
        if Weditor is not None:
            if not self._TUX:
                Weditor.ID = Weditor.ID.replace('/', '\\')
            self.edis.contenedor_principal.guardar_archivo(Weditor)
            self.edis.contenedor_secundario.compilar(Weditor.ID)

    def ejecutar(self):
        self.edis.contenedor_secundario.ejecutar()