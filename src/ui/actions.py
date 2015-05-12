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
        "name": translate("EDIS", "New File"),
        "connection": "create_editor",
        "shortcut": "new"},
    {
        "name": translate("EDIS", "New Project"),
        "connection": "create_new_project",
        "shortcut": "new-project"},
    {
        "name": translate("EDIS", "Open File"),
        "connection": "open_file",
        "shortcut": "open"},
    {
        "name": translate("EDIS", "Open Recent File"),
        "menu": True,
        "separator": True},
    {
        "name": translate("EDIS", "Open Project"),
        "connection": "open_project",
        "shortcut": "open-project"},
    {
        "name": translate("EDIS", "Open Folder..."),
        "connection": "open_directory"},
    {
        "name": translate("EDIS", "Close"),
        "connection": "close_file",
        "shortcut": "close"},
    {
        "name": translate("EDIS", "Close All"),
        "connection": "close_all",
        "separator": True},
    {
        "name": translate("EDIS", "Reload"),
        "connection": "reload_file",
        "shortcut": "reload",
        "separator": True},
    {
        "name": translate("EDIS", "Save"),
        "connection": "save_file",
        "shortcut": "save"},
    {
        "name": translate("EDIS", "Save As..."),
        "icon": "save-as",
        "connection": "save_file_as",
        "separator": True},
    {
        "name": translate("EDIS", "Properties"),
        "icon": "properties",
        "connection": "file_properties",
        "shortcut": "properties",
        "separator": True},
    {
        "name": translate("EDIS", "Exit"),
        "connection": "edis.close",
        "shortcut": "exit"}], [
    # Menú editar
    {
        "name": translate("EDIS", "Undo"),
        "connection": "action_undo",
        "shortcut": "undo"},
    {
        "name": translate("EDIS", "Redo"),
        "connection": "action_redo",
        "shortcut": "redo"},
    {
        "name": translate("EDIS", "Cut"),
        "connection": "action_cut",
        "shortcut": "cut"},
    {
        "name": translate("EDIS", "Copy"),
        "connection": "action_copy",
        "shortcut": "copy"},
    {
        "name": translate("EDIS", "Paste"),
        "connection": "action_paste",
        "shortcut": "paste"},
    {
        "name": translate("EDIS", "Select All"),
        "connection": "action_select_all",
        "shortcut": "select",
        "separator": True},
    {
        "name": translate("EDIS", "Indent More"),
        "connection": "action_indent",
        "shortcut": "indent"},
    {
        "name": translate("EDIS", "Indent Less"),
        "connection": "action_unindent",
        "shortcut": "unindent",
        "separator": True},
    {
        "name": translate("EDIS", "Duplicale Line"),
        "connection": "action_duplicate_line",
        "shortcut": "duplicate"},
    {
        "name": translate("EDIS", "Delete Line"),
        "connection": "action_delete_line",
        "shortcut": "delete",
        "separator": True},
    {
        "name": translate("EDIS", "To lower"),
        "connection": "action_to_lowercase"},
    {
        "name": translate("EDIS", "To UPPER"),
        "connection": "action_to_uppercase"},
    {
        "name": translate("EDIS", "To Title"),
        "connection": "action_to_title",
        "separator": True},
    {
        "name": translate("EDIS", "Comment"),
        "connection": "action_comment",
        "shortcut": "comment"},
    {
        "name": translate("EDIS", "Uncomment"),
        "connection": "action_uncomment",
        "shortcut": "uncomment",
        "separator": True},
    {
        "name": translate("EDIS", "Move Up"),
        "connection": "action_move_up",
        "shortcut": "up"},
    {
        "name": translate("EDIS", "Move Down"),
        "connection": "action_move_down",
        "shortcut": "down",
        "separator": True},
    {
        "name": translate("EDIS", "Configuration"),
        "connection": "show_settings",
        "shortcut": "preferences"}], [
    # Menú ver
    {
        "name": translate("EDIS", "Show Fullscreen"),
        "connection": "edis.show_full_screen",
        "shortcut": "fullscreen"},
    {
        "name": translate("EDIS", "Show Dev Mode"),
        "connection": "edis.show_hide_all",
        "shortcut": "hide-all"},
    {
        "name": translate("EDIS", "Show/hide Compiler"),
        "connection": "edis.show_hide_output",
        "shortcut": "hide-output"},
    {
        "name": translate("EDIS", "Show/hide Lateral"),
        "connection": "edis.show_hide_lateral",
        "shortcut": "hide-lateral"},
    {
        "name": translate("EDIS", "Show/hide Toolbars"),
        "connection": "edis.show_hide_toolbar",
        "shortcut": "hide-toolbar",
        "separator": True},
    {
        "name": translate("EDIS", "Show Tabs and Spaces"),
        "connection": "show_tabs_and_spaces"},
    {
        "name": translate("EDIS", "Show Indentation Guides"),
        "connection": "show_indentation_guides"},
    {
        "name": translate("EDIS", "Delete Markers"),
        "connection": "delete_editor_markers",
        "separator": True},
    {
        "name": translate("EDIS", "Show File Selector"),
        "connection": "show_selector",
        "shortcut": "show-selector",
        "separator": True},
    {
        "name": translate("EDIS", "Zoom In"),
        "connection": "action_zoom_in",
        "shortcut": "zoom-in"},
    {
        "name": translate("EDIS", "Zoom Out"),
        "connection": "action_zoom_out",
        "shortcut": "zoom-out"},
    {
        "name": translate("EDIS", "Normal Size"),
        "connection": "action_normal_size",
        "shortcut": "normal-font-size"}], [
    # Menú buscar
    {
        "name": translate("EDIS", "Find..."),
        "connection": "find",
        "shortcut": "find"},
    {
        "name": translate("EDIS", "Replace"),
        "connection": "find_and_replace",
        "shortcut": "find-replace",
        "separator": True},
    {
        "name": translate("EDIS", "Go To Line"),
        "connection": "show_go_to_line",
        "shortcut": "go"}], [
    # Menú ejecución
    {
        "name": translate("EDIS", "Build"),
        "connection": "build_source_code",
        "shortcut": "build"},
    {
        "name": translate("EDIS", "Execute"),
        "connection": "run_binary",
        "shortcut": "run"},
    {
        "name": translate("EDIS", "Build and Execute"),
        "connection": "build_and_run",
        "shortcut": "build-run"},
    {
        "name": translate("EDIS", "Stop"),
        "connection": "stop_program",
        "shortcut": "stop",
        "separator": True},
    {
        "name": translate("EDIS", "Clean Construction"),
        "icon": "clean",
        "connection": "clean_construction"}], [
    {
        "name": translate("EDIS", "Code Pasting"),
        "connection": "code_pasting",
        "shortcut": "cpaste"}], [
    # Menú acerca de
    {
        "name": translate("EDIS", "Report bug!"),
        "icon": "bug",
        "connection": "edis.report_bug",
        "separator": True},
    {
        "name": translate("EDIS", "About Edis"),
        "connection": "edis.about_edis"},
    {
        "name": translate("EDIS", "About Qt"),
        "icon": "qt",
        "connection": "edis.about_qt"}]
    )
