#-*- coding: utf-8 -*-

import os
import sys
import unittest

from PyQt4.QtGui import QApplication


PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.append('../')

from side_c.interfaz.dialogos import preferencias
from side_c.nucleo import configuraciones


class PruebaConfiguracionEditor(unittest.TestCase):
    """" Pruebas
        -SpinBoxs -> Ok!
    """
    def setUp(self):
        self.aplicacion = QApplication(sys.argv)
        self.wid = preferencias.ConfiguracionEditor(None)

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
            configuraciones.MARGEN)

        self.wid.spinInd.setValue(4)
        self.assertEqual(self.wid.spinInd.value(),
            configuraciones.INDENTACION)

    def test_checkBoxs(self):
        """ Prueba CheckBox """

        self.poner_en_cero()

        # Test
        self.wid.checkMargen.setChecked(True)
        self.assertEqual(self.wid.checkMargen.isChecked(),
            configuraciones.MOSTRAR_MARGEN)
        self.wid.checkInd.setChecked(True)
        self.assertEqual(self.wid.checkInd.isChecked(),
            configuraciones.CHECK_INDENTACION)

if __name__ == "__main__":
    unittest.main()
