#-*- coding: utf-8 -*-

# <Se realizan pruebas a widgets.>
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

import os
import sys
import unittest

from PyQt4.QtGui import QApplication


PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.append('../')

from edis_c.interfaz.dialogos.preferencias import preferencias_editor
from edis_c.nucleo import configuraciones


class PruebaConfiguracionEditor(unittest.TestCase):
    """ Pruebas
        -SpinBoxs -> Ok!
    """
    def setUp(self):
        self.aplicacion = QApplication(sys.argv)
        self.wid = preferencias_editor.CaracteristicasEditor()

    def poner_en_cero(self):
        """ Setea los valores en 0 """

        self.wid.spinMargen.setValue(0)
        self.wid.spinInd.setValue(0)

    def test_valores_por_defecto(self):
        """ Prueba con valores por defecto """

        self.assertEqual(self.wid.spinMargen.value(), 80)
        self.assertEqual(self.wid.spinInd.value(), 4)

    def test_spinBoxs(self):
        """ Prueba SpinBox """

        self.poner_en_cero()

        # Test
        self.wid.spinMargen.setValue(80)
        self.assertEqual(self.wid.spinMargen.value(),
            configuraciones.MARGEN)  # ok!

        self.wid.spinInd.setValue(4)
        self.assertEqual(self.wid.spinInd.value(),
            configuraciones.INDENTACION)  # ok!

    def test_checkBoxs(self):
        """ Prueba CheckBox """

        self.poner_en_cero()

        # Test
        self.wid.checkMargen.setChecked(False)
        self.assertEqual(self.wid.checkMargen.isChecked(),
            configuraciones.MOSTRAR_MARGEN)  # ok!
        self.wid.checkInd.setChecked(True)
        self.assertEqual(self.wid.checkInd.isChecked(),
            configuraciones.CHECK_INDENTACION)  # ok!


if __name__ == "__main__":
    unittest.main()