#-*- coding: utf-8 -*-

from setuptools import find_packages
packages = find_packages(exclude=["prueba_de_software"])
import warnings
warnings.simplefilter('ignore', DeprecationWarning)
import py2exe
warnings.resetwarnings()

from distutils.core import setup

target = {
    "script": "edis-c.py",
    "version": "1.0-alpha",
    "company_name": "",
    "copyright": "GPL",
    "name": "Edis",
    "dest_base": "Edis",
    }

setup(
    name="edis",
    author="Gabriel Acosta",
 #   author_email_="acostadariogabriel@gmail.com",
    url="http://github.com/centaurialpha/edis",
    license="GNU General Public License (GPL)",
    data_files=[('otros/QtQML', ['edis_c/otros/QtQML/notificacion.qml']),
        ('otros/pagina_de_bienvenida',
            ['edis_c/otros/pagina_de_bienvenida/pagina_de_bienvenida.qml',
            'edis_c/otros/pagina_de_bienvenida/Boton.qml',
            "edis_c/otros/pagina_de_bienvenida/fondo.png",
            'edis_c/otros/pagina_de_bienvenida/pylogo.png',
            'edis_c/otros/pagina_de_bienvenida/seiryu.png']),
        ('imagenes', ['edis_c/imagenes/abrir.png', 'edis_c/imagenes/nuevo.png',
            'edis_c/imagenes/buscar.png', 'edis_c/imagenes/codigo_c.png',
            'edis_c/imagenes/comentar.png', 'edis_c/imagenes/compilar.png',
            'edis_c/imagenes/compilar-ejecutar.png',
            'edis_c/imagenes/copiar.png',
            'edis_c/imagenes/cortar.png', 'edis_c/imagenes/deshacer.png',
            'edis_c/imagenes/desindentar.png',
            'edis_c/imagenes/edis_seiryu.png',
            'edis_c/imagenes/editor.png', 'edis_c/imagenes/frenar.png',
            'edis_c/imagenes/general.png', 'edis_c/imagenes/guardar.png',
            'edis_c/imagenes/indentar.png',
            'edis_c/imagenes/insertar-include.png',
            'edis_c/imagenes/main_c.png', 'edis_c/imagenes/notas.png',
            'edis_c/imagenes/pegar.png', 'edis_c/imagenes/play.png',
            'edis_c/imagenes/print.png', 'edis_c/imagenes/rehacer.png',
            'edis_c/imagenes/salir.png', 'edis_c/imagenes/seiryu_icono.png',
            'edis_c/imagenes/separador.png', 'edis_c/imagenes/tema.png',
            'edis_c/imagenes/titulo.png', 'edis_c/imagenes/terminal.png'])],
    package_data={"edis_c": ["imagenes/*", "nucleo/*", "otros/*",
                             "otros/idiomas/*", "otros/pagina_de_bienvenida/*",
                             "otros/QtQML/notificacion.qml", "otros/temas/*",
                             "interfaz/*",
                             "interfaz/contenedor_principal/*",
                             "interfaz/contenedor_secundario/*",
                             "interfaz/dialogos/*",
                             "interfaz/dialogos/preferencias/*",
                             "interfaz/editor/*", "interfaz/ide/*",
                             "interfaz/menu/*"]},
    zipfile=None,
    options={
        "py2exe": {
            "compressed": 0,
              "optimize": 0,
              "includes": ['sip', 'PyQt4.QtNetwork'],
              "excludes": ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email',
                  'pywin.debugger', 'pywin.debugger.dbgcon', 'pywin.dialogs',
                  'tcl', 'Tkconstants', 'Tkinter'],
              "packages": packages,
              "bundle_files": 1,
              "dist_dir": "dist",
              "xref": False,
              "skip_archive": False,
              "ascii": False,
              "custom_boot_script": '',
            }
        },
    console=[],
    windows=[target],
    service=[],
    com_server=[],
    ctypes_com_server=[]
        )