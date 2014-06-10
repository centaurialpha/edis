#-*- coding: utf- -*-

import os
import sys
import unittest

from PyQt4.QtGui import QApplication

PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.append('../')

from side_c.interfaz.dialogos import preferencias


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
        """ Prueba """

        self.poner_en_cero()

        self.wid.spinMargen.setValue(80)
        self.assertEqual(self.wid.spinMargen.value(), 80)

        self.wid.spinInd.setValue(4)
        self.assertEqual(self.wid.spinInd.value(), 4)


if __name__ == "__main__":
    unittest.main()
