# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from PyQt4.QtGui import QApplication
translate = QApplication.translate

ACTIONS = ([
    {
        "name": translate("EDIS", "Nuevo Archivo"),
        "connection": "create_editor",
        "shortcut": "new"},
    {
        "name": translate("EDIS", "Nuevo Proyecto"),
        "connection": "create_new_project",
        "shortcut": "new-project"},
    {
        "name": translate("EDIS", "Abrir Archivo"),
        "connection": "open_file",
        "shortcut": "open"},
    {
        "name": translate("EDIS", "Abrir Archivo Reciente"),
        "menu": True,
        "separator": True},
    {
        "name": translate("EDIS", "Abrir Proyecto"),
        "connection": "open_project",
        "shortcut": "open-project"},
    {
        "name": translate("EDIS", "Abrir Carpeta..."),
        "connection": "open_directory"},
    {
        "name": translate("EDIS", "Cerrar"),
        "connection": "close_file",
        "shortcut": "close"},
    {
        "name": translate("EDIS", "Cerrar Todo"),
        "connection": "close_all",
        "separator": True},
    {
        "name": translate("EDIS", "Recargar"),
        "connection": "reload_file",
        "shortcut": "reload",
        "separator": True},
    {
        "name": translate("EDIS", "Guardar"),
        "connection": "save_file",
        "shortcut": "save"},
    {
        "name": translate("EDIS", "Guardar Como..."),
        "icon": "save-as",
        "connection": "save_file_as",
        "separator": True},
    {
        "name": translate("EDIS", "Propiedades"),
        "icon": "properties",
        "connection": "file_properties",
        "shortcut": "properties",
        "separator": True},
    {
        "name": translate("EDIS", "Salir"),
        "connection": "edis.close",
        "shortcut": "exit"}], [
    # Menú editar
    {
        "name": translate("EDIS", "Deshacer"),
        "connection": "action_undo",
        "shortcut": "undo"},
    {
        "name": translate("EDIS", "Rehacer"),
        "connection": "action_redo",
        "shortcut": "redo"},
    {
        "name": translate("EDIS", "Cortar"),
        "connection": "action_cut",
        "shortcut": "cut"},
    {
        "name": translate("EDIS", "Copiar"),
        "connection": "action_copy",
        "shortcut": "copy"},
    {
        "name": translate("EDIS", "Pegar"),
        "connection": "action_paste",
        "shortcut": "paste"},
    {
        "name": translate("EDIS", "Seleccionar Todo"),
        "connection": "action_select_all",
        "shortcut": "select",
        "separator": True},
    {
        "name": translate("EDIS", "Indentar"),
        "connection": "action_indent",
        "shortcut": "indent"},
    {
        "name": translate("EDIS", "Quitar Indentación"),
        "connection": "action_unindent",
        "shortcut": "unindent",
        "separator": True},
    {
        "name": translate("EDIS", "A minúsculas"),
        "connection": "action_to_lowercase"},
    {
        "name": translate("EDIS", "A MAYÚSCULAS"),
        "connection": "action_to_uppercase"},
    {
        "name": translate("EDIS", "A Título"),
        "connection": "action_to_title",
        "separator": True},
    {
        "name": translate("EDIS", "Configuraciones"),
        "connection": "show_settings",
        "shortcut": "preferences"}], [
    # Menú ver
    {
        "name": translate("EDIS", "Pantalla Completa"),
        "connection": "edis.show_full_screen",
        "shortcut": "fullscreen"},
    {
        "name": translate("EDIS", "Modo Programador"),
        "connection": "edis.show_hide_all",
        "shortcut": "hide-all"},
    {
        "name": translate("EDIS", "Mostrar/Ocultar Compilador"),
        "connection": "edis.show_hide_output",
        "shortcut": "hide-output"},
    {
        "name": translate("EDIS", "Mostrar/Ocultar Lateral"),
        "connection": "edis.show_hide_lateral",
        "shortcut": "hide-lateral"},
    {
        "name": translate("EDIS", "Mostrar/Ocultar Barra de Herramientas"),
        "connection": "edis.show_hide_toolbar",
        "shortcut": "hide-toolbar",
        "separator": True},
    {
        "name": translate("EDIS", "Mostrar Espacios en Blanco y Tabs"),
        "connection": "show_tabs_and_spaces"},
    {
        "name": translate("EDIS", "Mostrar Guías de Indentación"),
        "connection": "show_indentation_guides"},
    {
        "name": translate("EDIS", "Delete Markers"),
        "connection": "delete_editor_markers",
        "separator": True},
    {
        "name": translate("EDIS", "Selector de Archivos"),
        "connection": "show_selector",
        "shortcut": "show-selector",
        "separator": True},
    {
        "name": translate("EDIS", "Acercar"),
        "connection": "action_zoom_in",
        "shortcut": "zoom-in"},
    {
        "name": translate("EDIS", "Alejar"),
        "connection": "action_zoom_out",
        "shortcut": "zoom-out"},
    {
        "name": translate("EDIS", "Restaurar Tamaño"),
        "connection": "action_normal_size",
        "shortcut": "normal-font-size"}], [
    # Menú buscar
    {
        "name": translate("EDIS", "Buscar..."),
        "connection": "find",
        "shortcut": "find"},
    {
        "name": translate("EDIS", "Reemplazar"),
        "connection": "find_and_replace",
        "shortcut": "find-replace",
        "separator": True},
    {
        "name": translate("EDIS", "Ir a Línea"),
        "connection": "show_go_to_line",
        "shortcut": "go"}], [
    # Menú código
    {
        "name": translate("EDIS", "Reemplazar tabulaciones por espacios"),
        "connection": "reemplazar_tabs_por_espacios"},
    {
        "name": translate("EDIS", "Duplicar Línea"),
        "connection": "action_duplicate_line",
        "shortcut": "duplicate"},
    {
        "name": translate("EDIS", "Eliminar Línea"),
        "connection": "action_delete_line",
        "shortcut": "delete"},
    {
        "name": translate("EDIS", "Comentar"),
        "connection": "action_comment",
        "shortcut": "comment"},
    {
        "name": translate("EDIS", "Descomentar"),
        "connection": "action_uncomment",
        "shortcut": "uncomment",
        "separator": True},
    {
        "name": translate("EDIS", "Move Hacia Arriba"),
        "connection": "action_move_up",
        "shortcut": "up"},
    {
        "name": translate("EDIS", "Move Hacia Abajo"),
        "connection": "action_move_down",
        "shortcut": "down",
        "separator": True},
    {
        "name": translate("EDIS", "Compartir Código"),
        "connection": "code_pasting",
        "shortcut": "cpaste"}], [
    # Menú ejecución
    {
        "name": translate("EDIS", "Compilar"),
        "connection": "build_source_code",
        "shortcut": "build"},
    {
        "name": translate("EDIS", "Ejecutar"),
        "connection": "run_binary",
        "shortcut": "run"},
    {
        "name": translate("EDIS", "Compilar y Ejecutar"),
        "connection": "build_and_run",
        "shortcut": "build-run"},
    {
        "name": translate("EDIS", "Frenar Ejecución"),
        "connection": "stop_program",
        "shortcut": "stop",
        "separator": True},
    {
        "name": translate("EDIS", "Limpiar Construcción"),
        "icon": "clean",
        "connection": "clean_construction"}], [
    # Menú acerca de
    {
        "name": translate("EDIS", "Reportar Bug!"),
        "icon": "bug",
        "connection": "edis.report_bug",
        "separator": True},
    {
        "name": translate("EDIS", "Acerca de Edis"),
        "connection": "edis.about_edis"},
    {
        "name": translate("EDIS", "Acerca de Qt"),
        "icon": "qt",
        "connection": "edis.about_qt"}]
    )
