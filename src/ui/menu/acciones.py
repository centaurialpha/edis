# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
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
        'nombre': 'Nuevo archivo',
        'conexion': 'agregar_editor',
        'atajo': _ATAJO['nuevo'],
        'icono': _ICONO['new']},
    {
        'seccion': 0,
        'nombre': 'Nuevo proyecto',
        'conexion': 'proyecto_nuevo',
        'separador': True},
    {
        'seccion': 0,
        'nombre': 'Abrir',
        'conexion': "abrir_archivo",
        'atajo': _ATAJO['abrir'],
        'icono': _ICONO['folder-open']},
    {
        'seccion': 0,
        'nombre': 'Abrir reciente',
        'submenu': True,
        'separador': True},
    {
        'seccion': 0,
        'nombre': 'Cerrar actual',
        'conexion': 'cerrar_archivo',
        'atajo': _ATAJO['cerrar-tab']},
    {
        'seccion': 0,
        'nombre': 'Cerrar todo',
        'conexion': 'cerrar_todo'},
    {
        'seccion': 0,
        'nombre': 'Cerrar los demás',
        'conexion': 'cerrar_demas',
        'separador': True},
    {
        'seccion': 0,
        'nombre': 'Guardar',
        'conexion': "guardar_archivo",
        'atajo': _ATAJO['guardar'],
        'icono': _ICONO['save']},
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
        'conexion': "imprimir_documento",
        'atajo': _ATAJO['imprimir']},
    {
        'seccion': 0,
        'nombre': 'Propiedades',
        'conexion': "propiedades_de_archivo",
        'atajo': _ATAJO['propiedades'],
        'separador': True},
    {
        'seccion': 0,
        'nombre': 'Exportar',
        'conexion': 'exportar_archivo',
        'separador': True},
    {
        'seccion': 0,
        'nombre': 'Salir',
        'conexion': 'edis.close',
        'atajo': _ATAJO['salir']},
    {
        'seccion': 1,
        'nombre': 'Deshacer',
        'conexion': 'deshacer',
        'atajo': _ATAJO['deshacer'],
        'icono': _ICONO['undo']},
    {
        'seccion': 1,
        'nombre': 'Rehacer',
        'conexion': 'rehacer',
        'atajo': _ATAJO['rehacer'],
        'icono': _ICONO['redo'],
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
        'icono': _ICONO['paste']},
    {
        'seccion': 1,
        'nombre': 'Seleccionar todo',
        'conexion': 'seleccionar_todo',
        'atajo': _ATAJO['seleccionar'],
        'separador': True},
    {
        'seccion': 1,
        'nombre': 'Indentar',
        'conexion': 'indentar',
        'atajo': _ATAJO['indentar'],
        'icono': _ICONO['indent']},
    {
        'seccion': 1,
        'nombre': 'Remover indentación',
        'conexion': 'remover_indentacion',
        'atajo': _ATAJO['quitar-indentacion'],
        'icono': _ICONO['unindent'],
        'separador': True},
    {
        'seccion': 1,
        'nombre': 'Duplicar línea',
        'conexion': 'duplicar_linea',
        'atajo': _ATAJO['duplicar']},
    {
        'seccion': 1,
        'nombre': 'Eliminar línea',
        'conexion': 'eliminar_linea',
        'atajo': _ATAJO['eliminar'],
        'separador': True},
    {
        'seccion': 1,
        'nombre': 'A minúsculas',
        'conexion': "convertir_a_minusculas"},
    {
        'seccion': 1,
        'nombre': 'A mayúsculas',
        'conexion': "convertir_a_mayusculas"},
    {
        'seccion': 1,
        'nombre': 'Convertir a título',
        'conexion': 'convertir_a_titulo',
        'separador': True},
    {
        'seccion': 1,
        'nombre': 'Comentar',
        'conexion': 'comentar_documento'},
    {
        'seccion': 1,
        'nombre': 'Descomentar',
        'conexion': 'descomentar_documento',
        'separador': True},
    {
        'seccion': 1,
        'nombre': 'Plegar/desplegar todo',
        'conexion': 'plegar_desplegar',
        'separador': True},
    {
        'seccion': 1,
        'nombre': 'Mover hacia arriba',
        'conexion': 'mover_linea_arriba',
        'atajo': _ATAJO['mover-arriba'],
        'icono': _ICONO['arrow-up']},
    {
        'seccion': 1,
        'nombre': 'Mover hacia abajo',
        'conexion': 'mover_linea_abajo',
        'atajo': _ATAJO['mover-abajo'],
        'icono': _ICONO['arrow-down'],
        'separador': True},
    {
        'seccion': 1,
        'nombre': 'Configuración',
        'conexion': "edis.configuracion_edis",
        'atajo': _ATAJO['preferencias'],
        'separador': True},
    {
        'seccion': 2,
        'nombre': 'Pantalla completa',
        'conexion': 'edis.mostrar_pantalla_completa',
        'atajo': _ATAJO['fullscreen']},
    {
        'seccion': 2,
        'nombre': 'Mostrar lateral',
        'conexion': 'edis.mostrar_ocultar_lateral',
        'checkable': True,
        'atajo': _ATAJO['lateral']},
    {
        'seccion': 2,
        'nombre': 'Mostrar compilador',
        'conexion': 'edis.mostrar_ocultar_output',
        'checkable': True,
        'atajo': _ATAJO['mostrar-compilador']},
    {
        'seccion': 2,
        'nombre': 'Mostrar toolbar',
        'conexion': 'edis.mostrar_ocultar_toolbar',
        'atajo': _ATAJO['mostrar-toolbar'],
        'separador': True},
    {
        'seccion': 2,
        'nombre': 'Mostrar tabs y espacios en blanco',
        'conexion': 'mostrar_tabs_espacios_blancos',
        'checkable': True},
    {
        'seccion': 2,
        'nombre': 'Mostrar guías',
        'conexion': 'mostrar_guias',
        'checkable': True,
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
        'nombre': 'Buscar',
        'conexion': 'busqueda',
        'atajo': _ATAJO['busqueda-rapida']},
    {
        'seccion': 3,
        'nombre': 'Reemplazar',
        'conexion': 'reemplazar',
        'atajo': _ATAJO['buscar'],
        'separador': True},
    {
        'seccion': 3,
        'nombre': 'Ir a línea',
        'conexion': 'ir_a_linea_dialogo'},
    {
        'seccion': 5,
        'nombre': 'Compilar',
        'conexion': 'compilar_codigo_fuente',
        'icono': _ICONO['build']},
    {
        'seccion': 5,
        'nombre': 'Ejecutar',
        'conexion': 'ejecutar_programa',
        'icono': _ICONO['run']},
    {
        'seccion': 5,
        'nombre': 'Compilar y ejecutar',
        'conexion': 'compilar_ejecutar',
        'separador': True},
    {
        'seccion': 5,
        'nombre': 'Terminar',
        'conexion': 'terminar_programa',
        'icono': _ICONO['stop'],
        'separador': True},
    {
        'seccion': 5,
        'nombre': 'Limpiar construcción',
        'conexion': 'limpiar_construccion'},
    {
        'seccion': 6,
        'nombre': 'Reportar bug!',
        'conexion': 'edis.reportar_bug'},
    {
        'seccion': 6,
        'nombre': 'Archivo log',
        'conexion': 'archivo_log',
        'separador': True},
    {
        'seccion': 6,
        'nombre': 'Acerca de EDIS',
        'conexion': 'edis.acerca_de_edis'},
    {
        'seccion': 6,
        'nombre': 'Acerca de Qt',
        'conexion': 'edis.acerca_de_qt'},
)
