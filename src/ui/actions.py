# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)


ACTIONS = ([
    {
        "name": "Archivo nuevo",
        "connection": "add_editor",
        "shortcut": "new"},
    {
        "name": "Abrir archivo",
        "connection": "open_file",
        "shortcut": "open"},
    {
        "name": "Abrir archivo reciente",
        "menu": True,
        "separator": True},
    {
        "name": "Cerrar",
        "connection": "close_file",
        "shortcut": "close"},
    {
        "name": "Cerrar todo",
        "connection": "close_all"},
    {
        "name": "Cerrar los demás",
        "connection": "close_all_others",
        "separator": True},
    {
        "name": "Guardar",
        "connection": "save_file",
        "shortcut": "save"},
    {
        "name": "Guardar como...",
        "connection": "save_file_as"},
    {
        "name": "Guardar todo",
        "connection": "save_all",
        "separator": True},
    {
        "name": "Propiedades",
        "connection": "file_properties",
        "separator": True},
    {
        "name": "Salir",
        "connection": "edis.close",
        "shortcut": "exit"}],
    # Menú editar
    [{
        "name": "Deshacer",
        "connection": "action_undo",
        "shortcut": "undo"},
    {
        "name": "Rehacer",
        "connection": "action_redo",
        "shortcut": "redo"},
    {
        "name": "Cortar",
        "connection": "action_cut",
        "shortcut": "cut"},
    {
        "name": "Copiar",
        "connection": "action_copy",
        "shortcut": "copy"},
    {
        "name": "Pegar",
        "connection": "action_paste",
        "shortcut": "paste"},
    {
        "name": "Seleccionar todo",
        "connection": "action_select_all",
        "shortcut": "select",
        "separator": True},
    {
        "name": "Indentar",
        "connection": "action_indent",
        "shortcut": "indent"},
    {
        "name": "Quitar indentación",
        "connection": "action_unindent",
        "shortcut": "unindent",
        "separator": True},
    {
        "name": "Duplicar línea",
        "connection": "action_duplicate_line",
        "shortcut": "duplicate"},
    {
        "name": "Eliminar línea",
        "connection": "action_delete_line",
        "shortcut": "delete",
        "separator": True},
    {
        "name": "A minúsculas",
        "connection": "action_to_lowercase"},
    {
        "name": "A mayúsculas",
        "connection": "action_to_uppercase"},
    {
        "name": "A título",
        "connection": "action_to_title",
        "separator": True},
    {
        "name": "Comentar",
        "connection": "action_comment",
        "shortcut": "comment"},
    {
        "name": "Descomentar",
        "connection": "action_uncomment",
        "shortcut": "uncomment",
        "separator": True},
    {
        "name": "Mover hacia arriba",
        "connection": "action_move_up",
        "shortcut": "up"},
    {
        "name": "Mover hacia abajo",
        "connection": "action_move_down",
        "shortcut": "down",
        "separator": True},
    {
        "name": "Configuración",
        "connection": "edis.show_settings"}],
    # Menú ver
    [{
        "name": "Pantalla completa",
        "connection": "edis.show_full_screen",
        "shortcut": "fullscreen"},
    {
        "name": "Ocultar todo",
        "connection": "edis.show_hide_all",
        "shortcut": "hide-all"},
    {
        "name": "Mostrar/ocultar compilador",
        "connection": "edis.show_hide_output",
        "shortcut": "hide-output"},
    {
        "name": "Mostrar/ocultar toolbars",
        "connection": "edis.show_hide_toolbars",
        "shortcut": "hide-toolbar",
        "separator": True},
    {
        "name": "Mostrar tabs y espacios en blanco",
        "connection": "show_tabs_and_spaces"},
    {
        "name": "Mostrar guías",
        "connection": "show_indentation_guides",
        "separator": True},
    {
        "name": "Selector",
        "connection": "show_selector",
        "shortcut": "show-selector",
        "separator": True},
    {
        "name": "Acercar",
        "connection": "action_zoom_in",
        "shortcut": "zoom-in"},
    {
        "name": "Alejar",
        "connection": "action_zoom_out",
        "shortcut": "zoom-out"}],
    # Menú buscar
    [{
        "name": "Buscar",
        "connection": "find",
        "shortcut": "find"},
    {
        "name": "Buscar y reemplazar",
        "connection": "find_and_replace",
        "shortcut": "find-replace",
        "separator": True},
    {
        "name": "Ir a línea",
        "connection": "show_go_to_line",
        "shortcut": "go-to-line"}],
    # Menú ejecución
    [{
        "name": "Compilar",
        "connection": "build_source_code",
        "shortcut": "build"},
    {
        "name": "Ejecutar",
        "connection": "run_binary",
        "shortcut": "run"},
    {
        "name": "Compilar y ejecutar",
        "connection": "build_and_run",
        "shortcut": "build-run"},
    {
        "name": "Terminar programa",
        "connection": "stop_program",
        "shortcut": "stop",
        "separator": True},
    {
        "name": "Limpiar construcción",
        "connection": "clean_construction"}],
    # Menú acerca de
    [{
        "name": "Reportar bug!",
        "connection": "edis.report_bug",
        "separator": True},
    {
        "name": "Archivo de log",
        "connection": "show_log_file",
        "separator": True},
    {
        "name": "Acerca de Edis",
        "connection": "edis.about_edis"},
    {
        "name": "Acerca de Qt",
        "connection": "edis.about_qt"}]
    )