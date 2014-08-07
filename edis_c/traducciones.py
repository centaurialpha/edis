#-*- coding: utf-8 -*-

# <Archivo para traducir.>
# Copyright (C) <2014>  <Gabriel Acosta>
# This file is part of EDIS-C.

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

from PyQt4 import QtCore

tr = QtCore.QCoreApplication.translate

# Menú
TRAD_MENU_ARCHIVO = ("&Archivo")
TRAD_MENU_EDITAR = tr("EDIS-C", "&Editar")
TRAD_MENU_VER = tr("EDIS-C", "&Ver")
TRAD_MENU_INSERTAR = tr("EDIS-C", "&Insertar")
TRAD_MENU_BUSCAR = tr("EDIS-C", "&Buscar")
TRAD_MENU_CODIGO = tr("EDIS-C", "&Código fuente")
TRAD_MENU_ACERCA_DE = tr("EDIS-C", "Ace&rca de")

# Menú archivo
TRAD_NUEVO = tr("EDIS-C", "Nuevo archivo")
TRAD_NUEVO_PLANTILLA = tr("EDIS-C", "Nuevo desde plantilla")
TRAD_NUEVO_MAIN = tr("EDIS-C", "main.c")
TRAD_ABRIR = tr("EDIS-C", "Abrir archivo")
TRAD_GUARDAR = tr("EDIS-C", "Guardar")
TRAD_GUARDAR_COMO = tr("EDIS-C", "Guardar como")
TRAD_GUARDAR_TODO = tr("EDIS-C", "Guardar todo")
TRAD_IMPRIMIR = tr("EDIS-C", "Imprimir archivo")
TRAD_PDF = tr("EDIS-C", "Exportar como PDF")
TRAD_CERRAR = tr("EDIS-C", "Cerrar")
TRAD_CERRAR_TODO = tr("EDIS-C", "Cerrar todo")
TRAD_CERRAR_EXC = tr("EDIS-C", "Cerrar todo excepto actual")
TRAD_SALIR = tr("EDIS-C", "Salir")

# Tooltips menú archivo
TRAD_NUEVO_TT = tr("EDIS-C", "Crear un nuevo archivo")
TRAD_NUEVO_MAIN_TT = tr(
    "EDIS-C", "Crear un nuevo archivo de C con función main")
TRAD_ABRIR_TT = tr("EDIS-C", "Abrir cualquier archivo de tipo C (.c .h)")
TRAD_GUARDAR_TT = tr("EDIS-C", "Guardar cambios en el archivo actual")
TRAD_GUARDAR_COMO_TT = tr("EDIS-C", "Elegir dónde guardar archivo actual")
TRAD_GUARDAR_TODO_TT = tr("EDIS-C", "Guardar todas las pestañas")
TRAD_IMPRIMIR_TT = tr("EDIS-C", "Imprimir código fuente")
TRAD_PDF_TT = tr("EDIS-C", "Exportar código fuente como archivo PDF")
TRAD_CERAR_TT = tr("EDIS-C", "Cerrar pestaña actual")
TRAD_CERRAR_TODO_TT = tr("EDIS-C", "Cerrar todas las pestañas")
TRAD_CERRAR_EXC_TT = tr("EDIS-C", "Cerrar todas las pestañas excepto actual")
TRAD_SALIR_TT = tr("EDIS-C", "Salir de EDIS")

# Menú editar
TRAD_DESHACER = tr("EDIS-C", "Deshacer")
TRAD_REHACER = tr("EDIS-C", "Rehacer")
TRAD_CORTAR = tr("EDIS-C", "Cortar")
TRAD_COPIAR = tr("EDIS-C", "Copiar")
TRAD_PEGAR = tr("EDIS-C", "Pegar")
TRAD_INDENTAR = tr("EDIS-C", "Indentar bloque")
TRAD_QUITAR_INDENT = tr("EDIS-C", "Quitar Indentación")
TRAD_SELECCIONAR = tr("EDIS-C", "Seleccionar todo")
TRAD_MOVER_ARRIBA = tr("EDIS-C", "Mover arriba")
TRAD_MOVER_ABAJO = tr("EDIS-C", "Mover abajo")
TRAD_MAYUSCULAS = tr("EDIS-C", "Convertir a mayúsculas")
TRAD_MINUSCULAS = tr("EDIS-C", "Convertir a minúsculas")
TRAD_CONV_TITULO = tr("EDIS-C", "Convertir a título")
TRAD_PREFERENCIAS = tr("EDIS-C", "Preferencias")

# Tooltips menú editar
TRAD_DESHACER_TT = tr("EDIS-C", "Acción deshacer")
TRAD_REHACER_TT = tr("EDIS-C", "Acción rehacer")
TRAD_CORTAR_TT = tr("EDIS-C", "Acción cortar")
TRAD_COPIAR_TT = tr("EDIS-C", "Acción copiar")
TRAD_PEGAR_TT = tr("EDIS-C", "Acción pegar")
TRAD_INDENTAR_TT = tr("EDIS-C", "Aplica indentación a uno o más bloques")
TRAD_QUITAR_INDENT_TT = tr("EDIS-C", "Quita indentación a uno o más bloques")
TRAD_SELECCIONAR_TT = tr("EDIS-C", "Selecciona todo el archivo")
TRAD_MOVER_ARRIBA_TT = tr(
    "EDIS-C", "Mueve una o más líneas de código hacia arriba")
TRAD_MOVER_ABAJO_TT = tr(
    "EDIS-C", "Mueve una o más líneas de códigohacia abajo")
TRAD_MAYUSCULAS_TT = tr(
    "EDIS-C", "Convierte a mayúsculas el texto seleccionado")
TRAD_MINUSCULAS_TT = tr(
    "EDIS-C", "Convierte a minúsculas el texto seleccionado")
TRAD_CONV_TITULO_TT = tr(
    "EDIS-C", "Convierte a tipo título el texto seleccionado")
TRAD_PREFERENCIAS_TT = tr("EDIS-C", "Preferencias de EDIS")

# Menú ver
TRAD_PANTALLA_COMPLETA = tr("EDIS-C", "Pantalla completa")
TRAD_MOSTRAR_TODO = tr("EDIS-C", "Mostrar/Ocultar todo")
TRAD_MOSTRAR_TOOLBAR = tr("EDIS-C", "Mostrar/Ocultar toolbars")
TRAD_MOSTRAR_SALIDA = tr("EDIS-C", "Mostrar/Ocultar compilador")
TRAD_ZOOM_MAS = tr("EDIS-C", "Zoom +")
TRAD_ZOOM_MENOS = tr("EDIS-C", "Zoom -")

# Menú insertar
TRAD_TITULO = tr("EDIS-C", "Insertar título")
TRAD_SEPARADOR = tr("EDIS-C", "Insertar separador")

# Submenú fecha y hora
TRAD_MENU_FECHA_HORA = tr("EDIS-C", "Insertar  fecha y hora")
TRAD_DMA = tr("EDIS-C", "dd-mm-aaaa")
TRAD_MDA = tr("EDIS-C", "mm-dd-aaaa")
TRAD_AMD = tr("EDIS-C", "aaaa-mm-dd")
TRAD_DMAH = tr("EDIS-C", "dd-mm-aaaa hh:mm")
TRAD_MDAH = tr("EDIS-C", "mm-dd-aaaa hh:mm")
TRAD_AMDH = tr("EDIS-C", "aaaa-mm-dd hh:mm")

# Submenú include
TRAD_MENU_INCLUDE = tr("EDIS-C", "Insertar '#include <>'")
TRAD_STDIO = tr("EDIS-C", "stdio.h")
TRAD_STDLIB = tr("EDIS-C", "stdlib.h")
TRAD_STRING = tr("EDIS-C", "string.h")
TRAD_INCLUDE = tr("EDIS-C", "#include <...>")

# Menú código
TRAD_COMPILAR = tr("EDIS-C", "Compilar")
TRAD_EJECUTAR = tr("EDIS-C", "Ejecutar")
TRAD_COMPILAR_COMPILAR = tr("EDIS-C", "Compilar y ejecutar")
TRAD_TERMINAR = tr("EDIS-C", "Terminar")

#Menú acerca de
TRAD_REPORTAR_BUGS = tr("EDIS-C", "Reportar bugs!")
TRAD_EDIS = tr("EDIS-C", "Acerca de EDIS")
TRAD_QT = tr("EDIS-C", "Acerca de Qt")