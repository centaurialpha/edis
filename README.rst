EDIS-C | Entorno de Desarrollo Integrado Simple para C.
=========================================================
.. image:: https://requires.io/github/centaurialpha/edis/requirements.png?branch=master
     :target: https://requires.io/github/centaurialpha/edis/requirements/?branch=master
.. image:: http://img.shields.io/badge/Python-2.7-yellow.svg
     :target: https://python.org
.. image:: http://img.shields.io/badge/Qt-4.8-brightgreen.svg
     :target: https://qt-project.org
.. image:: http://img.shields.io/badge/PyQt-4-blue.svg
     :target: http://riverbankcomputing.co.uk/software/pyqt/intro
.. image:: http://img.shields.io/badge/Licencia-GPLv3-red.svg
     :target: http://gplv3.fsf.org
     
Instrucciones para ejecutar EDIS (GNU/Linux)
--------------------------------------------

Asumiendo que ya se tiene instalado PyQt (Estoy 100% seguro que Python ya lo está ;):
Sistemas basados en Debian:
     sudo apt-get install python-qt4

Sistemas basados en Archlinux:

     sudo pacman -S python2-pyqt4
     
Descargar el archivo .zip, descomprimir e ingresar a la carpeta y correr el archivo .py:

     unzip -x edis-master.zip
     
     cd edis-master.zip
     
     python edis-c.py
     
     
También puedes clonar el repositorio (Antes instalar git):

     sudo apt-get install git

Instrucciones para ejecutar EDIS (Windows)
------------------------------------------

Instalar Python 2.7 y PyQt4 (NOTA: El instalador de PyQt debe ser para Python 2.7):

* `Python`_
* `PyQt`_

Descargar el archivo zip, descomprimir, entrar a la carpeta y correr el archivo .py desde la consola:

     python edis-c.py
     
.. _Python: https://www.python.org/download/releases/2.7.8/
.. _PyQt: http://www.riverbankcomputing.co.uk/software/pyqt/download
