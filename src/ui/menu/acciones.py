# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from src import recursos

_ATAJO = recursos.ATAJOS
_ICONO = recursos.ICONOS

# ACCIONES es una tupla de diccionarios, cada diccionario representa
# a una acción (QAction). La clave 'seccion' toma valores 0-6 y representa
# a un menu en particular.

#FIXME: Agregar tr, trUtf8 o translate para la traducción
ACCIONES = (
    {
        'seccion': 0,
        'nombre': 'Nuevo',
        'conexion': "agregar_editor",
        'atajo': _ATAJO['nuevo']},
    {
        'seccion': 0,
        'nombre': 'Abrir',
        'conexion': "abrir_archivo",
        'atajo': _ATAJO['abrir'],
        'separador': True},
    {
        'seccion': 0,
        'nombre': 'Guardar',
        'conexion': "guardar_archivo",
        'atajo': _ATAJO['guardar']},
    {
        'seccion': 0,
        'nombre': 'Guardar como',
        'conexion': "guardar_archivo_como"},
    {
        'seccion': 0,
        'nombre': 'Guardar todo',
        'conexion': "guardar_todo",
        'separador': True},
    {
        'seccion': 0,
        'nombre': 'Imprimir',
        'conexion': "imprimir_archivo"},
    {
        'seccion': 0,
        'nombre': 'Propiedades',
        'conexion': "propiedades_de_archivo",
        'separador': True},
    {
        'seccion': 0,
        'nombre': 'Cerrar',
        'conexion': 'cerrar_archivo',
        'atajo': _ATAJO['cerrar-tab']},
    {
        'seccion': 0,
        'nombre': 'Cerrar todo',
        'conexion': 'cerrar_todo'},
    {
        'seccion': 0,
        'nombre': 'Cerrar los demás',
        'conexion': 'cerrar_lo_demas',
        'separador': True},
    {
        'seccion': 0,
        'nombre': 'Salir',
        'conexion': 'salir'},
    {
        'seccion': 1,
        'nombre': 'Deshacer',
        'conexion': 'deshacer', },
    {
        'seccion': 1,
        'nombre': 'Rehacer',
        'conexion': 'rehacer',
        'separador': True},
    {
        'seccion': 1,
        'nombre': 'Cortar',
        'conexion': 'cortar', },
    {
        'seccion': 1,
        'nombre': 'Copiar',
        'conexion': 'copiar', },
    {
        'seccion': 1,
        'nombre': 'Pegar',
        'conexion': 'pegar',
        'separador': True},
    {
        'seccion': 1,
        'nombre': 'Seleccionar todo',
        'conexion': 'seleccionar_todo',
        'separador': True},
    {
        'seccion': 1,
        'nombre': 'Eliminar línea',
        'conexion': 'eliminar_linea'},
    {
        'seccion': 1,
        'nombre': 'Duplicar línea',
        'conexion': 'duplicar_linea',
        'separador': True},
    {
        'seccion': 1,
        'nombre': 'Texto a minúsculas',
        'conexion': "convertir_a_minusculas"},
    {
        'seccion': 1,
        'nombre': 'Texto a mayúsculas',
        'conexion': "convertir_a_mayusculas",
        'separador': True},
    {
        'seccion': 1,
        'nombre': 'Indentar',
        'conexion': 'indentar'},
    {
        'seccion': 1,
        'nombre': 'Remover indentación',
        'conexion': 'remover_indentacion'},
    {
        'seccion': 1,
        'nombre': 'Configuración',
        'conexion': "configuracion_edis",
        'separador': True},
    {
        'seccion': 2,
        'nombre': 'Selector',
        'conexion': 'selector',
        'atajo': _ATAJO['selector']},
    {
        'seccion': 3,
        'nombre': 'Buscar',
        'conexion': 'busqueda_rapida'}
)
