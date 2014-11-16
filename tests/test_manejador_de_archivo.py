#-*- coding: utf8 -*-

# Pruebas con archivos y carpetas

import unittest
import os
import sys


CARPETA = os.path.dirname(os.path.realpath(__file__))
sys.path.append('../')

from edis_c.nucleo.manejador_de_archivo import leer_contenido_de_archivo
from edis_c.nucleo.manejador_de_archivo import _nombreBase
from edis_c.nucleo.manejador_de_archivo import nombre_de_archivo
from edis_c.nucleo.manejador_de_archivo import archivos_desde_carpeta


class Prueba(unittest.TestCase):

    def setUp(self):
        global CARPETA
        self.carpeta = os.path.join(CARPETA)

    def test_leer_contenido(self):
        archivo = os.path.join(self.carpeta, 'ejemplo.c')
        contenido = leer_contenido_de_archivo(archivo)
        resultado_esperado = ("#include <stdio.h>\n\nint main( void )\n"
        "{\n\tputs( \"Testing\" );\n\treturn 0;\n}\n")
        self.assertEqual(contenido, resultado_esperado)  # ok!

    def test_leer_caracteres_raros(self):
        archivo = os.path.join(self.carpeta, 'caracteres.c')
        contenido = leer_contenido_de_archivo(archivo)
        resultado_esperado = ("\xc3\xb1\xc3\xa1m\n")
        self.assertEqual(contenido, resultado_esperado)  # ok!

    def test_nombreBase(self):
        archivo = '/home/edis/archivo.c'
        #archivo_sin_ex = '/home/edis/archivo'
        prueba = _nombreBase(archivo)
        resultado_esperado = 'archivo.c'
        self.assertEqual(prueba, resultado_esperado)  # ok!
        #print prueba

    def test_nombre_de_archivo(self):
        archivo = '/home/gabo/edis/main.c'
        prueba = nombre_de_archivo(archivo)
        resultado_esperado = 'main'
        self.assertEqual(prueba, resultado_esperado)  # ok!
        #print prueba

    def test_archivos_desde_carpeta(self):
        carpeta = '/home/gabo/prueba'
        extension = '.c'
        prueba = archivos_desde_carpeta(carpeta, extension)
        resultado_esperado = ['lala.c', 'test.c']
        self.assertEqual(prueba, resultado_esperado)  # ok!


if __name__ == "__main__":
    unittest.main()