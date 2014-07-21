#-*- coding: utf-8 -*-

from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QGroupBox
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QCheckBox

from edis_c.nucleo import configuraciones


class ConfiguracionEjecucion(QWidget):

    def __init__(self, parent):
        super(ConfiguracionEjecucion, self).__init__(parent)

        layoutV = QVBoxLayout(self)

        grupoCompilacion = QGroupBox(
            self.trUtf8("Opciones de compilación y ejecución"))
        grilla = QVBoxLayout(grupoCompilacion)

        # Checks parámetros adicionales para el compilador
        self.checkWerror = QCheckBox(
            self.trUtf8("-Werror: Considera los warnings como error."))
        self.checkO2 = QCheckBox(
            self.trUtf8("-O2: Optimización para 32bits."))

        grilla.addWidget(self.checkWerror)
        grilla.addWidget(self.checkO2)

        # Configuraciones
        parametros = list(str(configuraciones.PARAMETROS).split())
        if '-Werror' in parametros:
            self.checkWerror.setChecked(True)
        if '-O2' in parametros:
            self.checkO2.setChecked(True)

        layoutV.addWidget(grupoCompilacion)
