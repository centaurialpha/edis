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
     
**Versión actual:** 1.0-alpha *(por favor enviar reportes de cualquier bug, o sugerencia de característica desde el menú Acerca de/Reportar bugs).*

.. image:: http://s11.postimg.org/eitnbtacj/Captura_de_pantalla_de_2014_08_08_12_28_48.png

Características
---------------

* Acciones básicas de un editor. (Crear, abrir, guardar, deshacer, cortar, copiar, exportar como pdf, imprimir, etc...).
* Márgen de línea.
* Minimapa.
* Resaltado de sintaxis.
* Plegado de código.
* Comentar, descomentar código.
* Eliminar, duplicar línea(s).
* Insertado de #include y #define desde cualquier parte.
* Insertado de título y separador.
* Resaltado de braces (corchetes, llaves y paréntesis).
* Mover línea o bloques de código.
* Autoindentación.
* Autocompletado de braces.
* Guía de bloques.
* Zoom.
* Insertado de fecha y hora.
* Pestañas.
* Desplazamiento de pestañas con ALT + (1-9).
* Indentar y quitar indentación de una línea o bloques seleccionados.
* Conversión a mayúsculas, minúsculas y título a partir de una selección.
* Búsqueda de palabras.
* Ir a una línea específica.
* Estadísticas del documento (número de líneas, espacios en blanco, tamaño, etc.).

Instrucciones para ejecutar EDIS (GNU/Linux)
--------------------------------------------

Asumiendo que ya se tiene instalado PyQt (Estoy 100% seguro que Python ya lo está ;):

Sistemas basados en Debian::

     sudo apt-get install python-qt4

Sistemas basados en Archlinux::

     sudo pacman -S python2-pyqt4
     
Descargar el archivo .zip, descomprimir e ingresar a la carpeta y correr el archivo .py::

     unzip -x edis-master.zip
     
     cd edis-master.zip
     
     python edis-c.py
     
* `Video (Linux)`_

También puedes clonar el repositorio (Antes instalar git)::

     sudo apt-get install git

Instrucciones para ejecutar EDIS (Windows)
------------------------------------------

Instalar Python 2.7 y PyQt4 (NOTA: El instalador de PyQt debe ser para Python 2.7):

* `Python`_
* `PyQt`_

ATENCION!: **EDIS-C** Utiliza el compilador de `GNU (GCC)`_ 

Descargar el archivo zip, descomprimir, entrar a la carpeta y correr el archivo .py desde la consola::

     python edis-c.py

* `Video (Windows)`_

.. _Python: https://www.python.org/download/releases/2.7.8/
.. _PyQt: http://www.riverbankcomputing.co.uk/software/pyqt/download
.. _Video (Linux): https://www.youtube.com/watch?v=yXoD-RYJ0n4
.. _Video (Windows): https://www.youtube.com/watch?v=IJkHPutAwcs
.. _GNU (GCC): http://sourceforge.net/projects/mingw/files/Installer/mingw-get-setup.exe/download
