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

"""
Archivo                Editar                Ver
------------------------------------------------------------------
Nuevo                  Deshacer              Pantalla completa
Abrir                  Rehacer               Mostrar lateral
Cerrar                 Cortar                Mostrar output
    | Cerrar actual    Copiar                Mostrar toolbar
    | Cerrar todo      Pegar                 Espacios en blancos
    | Cerrar demás     Eliminar línea        Guías
Guardar                Duplicar línea        Modo wrap
Guardar como           A mayúsculas          Acercar
Guardar todo           A minúsculas          Alejar
Imprimir               A título
Propiedades            Mover hacia arriba
Exportar               Mover hacia abajo
Salir                  Indentar
                       Remover indentación
                       Comentar
                       Descomentar
                       Configuración

Herramientas           Proyecto              Ayuda
-------------------------------------------------------------------
Insertar título        Compilar              Archivo de log
Insertar separador     Ejecutar              Reportar bug
Insertar include                             Acerca de EDIS
Insertar macro                               Acerca de Qt

"""
#FIXME: Agregar tr, trUtf8 o translate para la traducción
ACCIONES = (
    {
        'seccion': 0,
        'nombre': 'Nuevo',
        'conexion': "agregar_editor",
        'atajo': _ATAJO['nuevo'],
        #'icono': _ICONO['document-new']},
            },
    {
        'seccion': 0,
        'nombre': 'Abrir',
        'conexion': "abrir_archivo",
        'atajo': _ATAJO['abrir'],
        'icono': _ICONO['folder-open'],
        'separador': True},
    {
        'seccion': 0,
        'nombre': 'Cerrar',
        'submenu': True,
        'separador': True},
    {
        'seccion': 0,
        'nombre': 'Cerrar actual',
        'conexion': 'cerrar_archivo',
        'atajo': _ATAJO['cerrar-tab'],
        'submenu': 'Cerrar'},
    {
        'seccion': 0,
        'nombre': 'Cerrar todo',
        'conexion': 'cerrar_todo',
        'submenu': 'Cerrar'},
    {
        'seccion': 0,
        'nombre': 'Cerrar los demás',
        'conexion': 'cerrar_demas',
        'submenu': 'Cerrar'},
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
        'conexion': "imprimir_archivo",
        'atajo': _ATAJO['imprimir']},
    {
        'seccion': 0,
        'nombre': 'Propiedades',
        'conexion': "propiedades_de_archivo",
        'separador': True},
    {
        'seccion': 0,
        'nombre': 'Exportar',
        'conexion': 'exportar_archivo',
        'separador': True},
    {
        'seccion': 0,
        'nombre': 'Salir',
        'conexion': 'edis.close'},
    {
        'seccion': 1,
        'nombre': 'Deshacer',
        'conexion': 'deshacer',
        'atajo': _ATAJO['deshacer']},
    {
        'seccion': 1,
        'nombre': 'Rehacer',
        'conexion': 'rehacer',
        'atajo': _ATAJO['rehacer'],
        'separador': True},
    {
        'seccion': 1,
        'nombre': 'Cortar',
        'conexion': 'cortar',
        'atajo': _ATAJO['cortar']},
    {
        'seccion': 1,
        'nombre': 'Copiar',
        'conexion': 'copiar',
        'atajo': _ATAJO['copiar']},
    {
        'seccion': 1,
        'nombre': 'Pegar',
        'conexion': 'pegar',
        'atajo': _ATAJO['pegar'],
        'separador': True},
    {
        'seccion': 1,
        'nombre': 'Seleccionar todo',
        'conexion': 'seleccionar_todo',
        'atajo': _ATAJO['seleccionar'],
        'separador': True},
    {
        'seccion': 1,
        'nombre': 'Eliminar línea',
        'conexion': 'eliminar_linea',
        'atajo': _ATAJO['eliminar']},
    {
        'seccion': 1,
        'nombre': 'Duplicar línea',
        'conexion': 'duplicar_linea',
        'atajo': _ATAJO['duplicar'],
        'separador': True},
    {
        'seccion': 1,
        'nombre': 'Texto a minúsculas',
        'conexion': "convertir_a_minusculas"},
    {
        'seccion': 1,
        'nombre': 'Texto a mayúsculas',
        'conexion': "convertir_a_mayusculas"},
    {
        'seccion': 1,
        'nombre': 'Convertir a título',
        'conexion': 'convertir_a_titulo',
        'atajo': _ATAJO['titulo'],
        'separador': True},
    {
        'seccion': 1,
        'nombre': 'Indentar',
        'conexion': 'indentar',
        'atajo': _ATAJO['indentar']},
    {
        'seccion': 1,
        'nombre': 'Remover indentación',
        'conexion': 'remover_indentacion',
        'atajo': _ATAJO['quitar-indentacion'],
        'separador': True},
    {
        'seccion': 1,
        'nombre': 'Configuración',
        'conexion': "configuracion_edis",
        'separador': True},
    {
        'seccion': 2,
        'nombre': 'Pantalla completa',
        'conexion': 'pantalla_completa',
        'atajo': _ATAJO['fullscreen']},
    {
        'seccion': 2,
        'nombre': 'Mostrar lateral',
        'conexion': 'mostrar_panel_lateral',
        'atajo': _ATAJO['lateral']},
    {
        'seccion': 2,
        'nombre': 'Mostrar compilador',
        'conexion': 'mostrar_salida_del_compilador',
        'atajo': _ATAJO['mostrar-compilador']},
    {
        'seccion': 2,
        'nombre': 'Mostrar toolbar',
        'conexion': 'mostrar_toolbar',
        'atajo': _ATAJO['mostrar-toolbar'],
        'separador': True},
    {
        'seccion': 2,
        'nombre': 'Selector',
        'conexion': 'selector',
        'atajo': _ATAJO['selector'],
        'separador': True},
    {
        'seccion': 2,
        'nombre': 'Acercar',
        'conexion': 'acercar',
        'atajo': _ATAJO['acercar']},
    {
        'seccion': 2,
        'nombre': 'Alejar',
        'conexion': 'alejar',
        'atajo': _ATAJO['alejar']},
    {
        'seccion': 3,
        'nombre': 'Búsqueda rápida',
        'conexion': 'busqueda_rapida',
        'atajo': _ATAJO['busqueda-rapida']},
    {
        'seccion': 3,
        'nombre': 'Buscar',
        'conexion': 'buscar',
        'atajo': _ATAJO['buscar']},
    {
        'seccion': 6,
        'nombre': 'Reportar bug!',
        'conexion': 'edis.reportar_bug'},
    {
        'seccion': 6,
        'nombre': 'Archivo log',
        'conexion': 'archivo_log'},
)
