# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Gabriel Acosta <acostadariogabriel at gmail>
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

from collections import OrderedDict

# Módulos QtGui
from PyQt4.QtGui import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QCheckBox,
    QSlider,
    QLCDNumber,
    QSpacerItem,
    QSizePolicy,
    QLabel,
    QComboBox,
    QSpinBox,
    QTabWidget,
    QFontComboBox,
    QFont
    )

# Módulos QtCore
from PyQt4.QtCore import Qt

# Módulos EDIS
from src.core import settings
from src.ui.main import Edis


class EditorConfiguration(QTabWidget):

    __TABS = OrderedDict()

    def __init__(self):
        super(EditorConfiguration, self).__init__()
        self.general = GeneralSection()
        self.display = DisplaySection()
        self.completion = CompletionSection()

        preferences = Edis.get_component("preferences")
        preferences.install_section(self)

    @classmethod
    def install_widget(cls, name, obj):
        cls.__TABS[name] = obj

    def get_tabs(self):
        return self.__TABS

    def install_tab(self, obj, name):
        self.addTab(obj, name)

    def save(self):
        for index in range(self.count()):
            self.widget(index).save()


class GeneralSection(QWidget):
    """ Clase Configuracion Editor """

    def __init__(self):
        super(GeneralSection, self).__init__()
        main_container = QVBoxLayout(self)

        # Tabs and indentation
        group_indentation = QGroupBox(self.tr("Indentación y Tabs:"))
        box = QGridLayout(group_indentation)
        box.setContentsMargins(20, 5, 20, 5)
        box.addWidget(QLabel(self.tr("Política:")), 0, 0)
        self.combo_tabs = QComboBox()
        self.combo_tabs.setFixedWidth(350)
        self.combo_tabs.addItems([
            self.tr("Solo Espacios"),
            self.tr("Solo Tabulaciones"),
            ])
        box.addWidget(self.combo_tabs, 0, 1)
        self.combo_tabs.setCurrentIndex(
            int(settings.get_setting('editor/usetabs')))
        # Auto indent
        self.check_autoindent = QCheckBox(self.tr("Indentación Automática"))
        box.addWidget(self.check_autoindent, 1, 0)
        box.setAlignment(Qt.AlignLeft)
        self.check_autoindent.setChecked(settings.get_setting('editor/indent'))

        # Minimap
        group_minimap = QGroupBox(self.tr("Minimapa:"))
        box = QGridLayout(group_minimap)
        box.setContentsMargins(20, 5, 20, 5)
        self.check_minimap = QCheckBox(
            self.tr("Activar Minimapa (requiere reiniciar el Editor)"))
        self.check_minimap.setChecked(settings.get_setting('editor/minimap'))
        box.addWidget(self.check_minimap, 0, 0)
        #self.check_minimap_animation = QCheckBox(self.tr("Enable animation"))
        #self.check_minimap_animation.setChecked(
            #settings.get_setting('editor/minimap-animation'))
        #box.addWidget(self.check_minimap_animation, 1, 0)
        #box.addWidget(QLabel(self.tr("Size Area:")), 2, 0)
        #self.spin_area_minimap = QSpinBox()
        #self.spin_area_minimap.setFixedWidth(350)
        #box.addWidget(self.spin_area_minimap, 2, 1)
        box.setAlignment(Qt.AlignLeft)

        # Cursor
        group_caret = QGroupBox(self.tr("Cursor:"))
        box = QGridLayout(group_caret)
        box.setContentsMargins(20, 5, 20, 5)
        box.setAlignment(Qt.AlignLeft)
        # Type
        box.addWidget(QLabel(self.tr("Tipo:")), 0, 0)
        self.combo_caret = QComboBox()
        self.combo_caret.setFixedWidth(300)
        caret_types = [
            self.tr('Invisible'),
            self.tr('Línea'),
            self.tr('Bloque')
            ]
        self.combo_caret.addItems(caret_types)
        index = settings.get_setting('editor/cursor')
        self.combo_caret.setCurrentIndex(index)
        box.addWidget(self.combo_caret, 0, 1)
        # Width
        box.addWidget(QLabel(self.tr("Ancho:")), 1, 0)
        self.spin_caret_width = QSpinBox()
        self.spin_caret_width.setFixedWidth(300)
        if index != 1:
            self.spin_caret_width.setEnabled(False)
        self.spin_caret_width.setRange(1, 3)
        self.spin_caret_width.setValue(
            settings.get_setting('editor/caret-width'))
        box.addWidget(self.spin_caret_width, 1, 1, Qt.AlignLeft)
        # Period
        box.addWidget(QLabel(self.tr("Período (ms):")), 2, 0)
        self.slider_caret_period = QSlider(Qt.Horizontal)
        self.slider_caret_period.setMaximum(500)
        self.slider_caret_period.setFixedWidth(300)
        box.addWidget(self.slider_caret_period, 2, 1, Qt.AlignLeft)
        lcd_caret = QLCDNumber()
        lcd_caret.setSegmentStyle(QLCDNumber.Flat)
        box.addWidget(lcd_caret, 2, 3)

        # Font
        group_typo = QGroupBox(self.tr("Fuente:"))
        box = QGridLayout(group_typo)
        box.setContentsMargins(20, 5, 20, 5)
        box.addWidget(QLabel(self.tr("Familia:")), 0, 0)
        self.combo_font = QFontComboBox()
        self.combo_font.setFixedWidth(350)
        box.addWidget(self.combo_font, 0, 1)
        self._load_font()
        box.addWidget(QLabel(self.tr("Tamaño:")), 1, 0)
        self.spin_size_font = QSpinBox()
        self.spin_size_font.setValue(settings.get_setting('editor/size-font'))
        self.spin_size_font.setFixedWidth(350)
        box.addWidget(self.spin_size_font, 1, 1)
        box.setAlignment(Qt.AlignLeft)

        # Scheme
        group_scheme = QGroupBox(self.tr("Tema:"))
        box = QVBoxLayout(group_scheme)
        box.setContentsMargins(20, 5, 20, 5)
        self.combo_scheme = QComboBox()
        self.combo_scheme.setFixedWidth(350)
        self.combo_scheme.addItems(['Dark Edis', 'White Edis'])
        scheme = settings.get_setting('editor/scheme')
        index = 0
        if scheme != 'dark':
            index = 1
        self.combo_scheme.setCurrentIndex(index)
        box.addWidget(self.combo_scheme)
        box.addWidget(QLabel(self.tr("Requiere reiniciar Edis")))

        ## Agrupación
        main_container.addWidget(group_indentation)
        main_container.addWidget(group_minimap)
        main_container.addWidget(group_caret)
        main_container.addWidget(group_typo)
        main_container.addWidget(group_scheme)
        main_container.addItem(QSpacerItem(0, 10, QSizePolicy.Expanding,
                               QSizePolicy.Expanding))

        EditorConfiguration.install_widget(self.tr("General"), self)

        # Conexiones
        self.combo_scheme.currentIndexChanged['const QString&'].connect(
            self._change_scheme)
        self.combo_caret.currentIndexChanged[int].connect(
            self._caret_type_changed)
        self.slider_caret_period.valueChanged[int].connect(
            lcd_caret.display)

        self.slider_caret_period.setValue(
            settings.get_setting('editor/cursor-period'))

    def _change_scheme(self, theme):
        theme = theme.split()[0].lower()
        editor_container = Edis.get_component("principal")
        editor = editor_container.get_active_editor()
        if editor is not None:
            # Restyle
            pass

    def _caret_type_changed(self, index):
        self.spin_caret_width.setEnabled(bool(index))

    def _load_font(self):

        font = settings.get_setting('editor/font')
        self.combo_font.setCurrentFont(QFont(font))

    def save(self):
        """ Guarda las configuraciones del Editor. """

        use_tabs = bool(self.combo_tabs.currentIndex())
        settings.set_setting('editor/usetabs', use_tabs)
        auto_indent = self.check_autoindent.isChecked()
        settings.set_setting('editor/indent', auto_indent)
        settings.set_setting('editor/minimap', self.check_minimap.isChecked())
        #settings.set_setting('editor/minimap-animation',
                             #self.check_minimap_animation.isChecked())
        font = self.combo_font.currentFont().family()
        settings.set_setting('editor/font', font)
        font_size = self.spin_size_font.value()
        settings.set_setting('editor/size-font', font_size)
        scheme = self.combo_scheme.currentText().split()[0].lower()
        settings.set_setting('editor/scheme', scheme)
        settings.set_setting('editor/cursor',
                             self.combo_caret.currentIndex())
        settings.set_setting('editor/caret-width',
                             self.spin_caret_width.value())
        settings.set_setting('editor/cursor-period',
                             self.slider_caret_period.value())
        editor_container = Edis.get_component("principal")
        editor = editor_container.get_active_editor()
        if editor is not None:
            editor.setIndentationsUseTabs(use_tabs)
            editor.load_font(font, font_size)


class DisplaySection(QWidget):

    def __init__(self):
        super(DisplaySection, self).__init__()
        EditorConfiguration.install_widget(self.tr("Visualización"), self)
        container = QVBoxLayout(self)

        # Text wrapping
        group_wrapping = QGroupBox(self.tr("Ajuste de Texto:"))
        box = QGridLayout(group_wrapping)
        self.check_wrap = QCheckBox(self.tr("Activar ajuste de texto"))
        box.addWidget(self.check_wrap, 0, 0)
        self.check_margin = QCheckBox(self.tr("Mostrar márgen derecho:"))
        box.addWidget(self.check_margin, 1, 0)
        self.slider_margin = QSlider(Qt.Horizontal)
        self.slider_margin.setMaximum(180)
        self.slider_margin.setFixedWidth(350)
        box.addWidget(self.slider_margin, 1, 1, Qt.AlignLeft)
        lcd_margin = QLCDNumber()
        lcd_margin.setSegmentStyle(QLCDNumber.Flat)
        box.addWidget(lcd_margin, 1, 2, Qt.AlignLeft)
        box.setAlignment(Qt.AlignLeft)
        container.addWidget(group_wrapping)  # Add group

        # Extras: line number, markers, whitespace, etc
        group_extras = QGroupBox(self.tr("Visualización:"))
        box = QGridLayout(group_extras)
        self.check_line_numbers = QCheckBox(
            self.tr("Mostrar números de líneas"))
        box.addWidget(self.check_line_numbers, 0, 0)
        self.check_current_line = QCheckBox(self.tr("Resaltar línea actual"))
        box.addWidget(self.check_current_line, 0, 1)
        self.check_mark_change = QCheckBox(self.tr("Marcar línea modificada"))
        box.addWidget(self.check_mark_change, 1, 0)
        self.check_match_brace = QCheckBox(
            self.tr("Resaltar [], {}, (), <>"))
        box.addWidget(self.check_match_brace, 1, 1)
        self.check_whitespace = QCheckBox(
            self.tr("Mostrar espacios en blanco"))
        box.addWidget(self.check_whitespace, 2, 0)
        self.check_guides = QCheckBox(self.tr("Mostrar guías de indentación"))
        box.addWidget(self.check_guides, 2, 1)
        self.check_eof = QCheckBox(self.tr("Mostrar EOF"))
        box.addWidget(self.check_eof, 3, 0)
        container.addWidget(group_extras)  # Add group

        # Spacer
        container.addItem(QSpacerItem(0, 10, QSizePolicy.Expanding,
                          QSizePolicy.Expanding))

        # Connections
        self.slider_margin.valueChanged[int].connect(lcd_margin.display)

        # Configuration
        self.check_wrap.setChecked(
            settings.get_setting('editor/wrap-mode'))
        self.check_line_numbers.setChecked(
            settings.get_setting('editor/show-line-number'))
        self.check_mark_change.setChecked(
            settings.get_setting('editor/mark-change'))
        self.check_match_brace.setChecked(
            settings.get_setting('editor/match-brace'))
        self.check_current_line.setChecked(
            settings.get_setting('editor/show-caret-line'))
        self.check_eof.setChecked(
            settings.get_setting('editor/eof'))
        self.check_margin.setChecked(
            settings.get_setting('editor/show-margin'))
        self.slider_margin.setValue(settings.get_setting('editor/width-margin'))
        self.check_whitespace.setChecked(
            settings.get_setting('editor/show-tabs-spaces'))
        self.check_guides.setChecked(
            settings.get_setting('editor/show-guides'))

    def save(self):
        settings.set_setting('editor/wrap-mode',
            self.check_wrap.isChecked())
        settings.set_setting('editor/show-margin',
            self.check_margin.isChecked())
        settings.set_setting('editor/width-margin',
            self.slider_margin.value())
        settings.set_setting('editor/show-line-number',
            self.check_line_numbers.isChecked())
        settings.set_setting('editor/mark-change',
            self.check_mark_change.isChecked())
        settings.set_setting('editor/match-brace',
            self.check_match_brace.isChecked())
        settings.set_setting('editor/show-caret-line',
            self.check_current_line.isChecked())
        settings.set_setting('editor/show-tabs-spaces',
            self.check_whitespace.isChecked())
        settings.set_setting('editor/show-guides',
            self.check_guides.isChecked())
        settings.set_setting('editor/eof',
            self.check_eof.isChecked())
        editor_container = Edis.get_component("principal")
        editor = editor_container.get_active_editor()
        if editor is not None:
            editor.set_brace_matching()
            editor.show_line_numbers()
            editor.update_options()
            editor.update_margin()


class CompletionSection(QWidget):

    def __init__(self):
        super(CompletionSection, self).__init__()
        EditorConfiguration.install_widget(self.tr("Autocompletado"), self)
        container = QVBoxLayout(self)

        group_complete = QGroupBox(self.tr("Completar:"))
        box = QGridLayout(group_complete)
        box.setContentsMargins(20, 5, 20, 5)
        self.check_bracket = QCheckBox(self.tr("Corchetes []"))
        box.addWidget(self.check_bracket, 0, 0)
        self.check_paren = QCheckBox(self.tr("Paréntesis ()"))
        box.addWidget(self.check_paren, 0, 1)
        self.check_key = QCheckBox(self.tr("Llaves {}"))
        box.addWidget(self.check_key, 1, 0)
        self.check_quote = QCheckBox(self.tr("Comillas Dobles \" \""))
        box.addWidget(self.check_quote, 1, 1)
        self.check_single_quote = QCheckBox(self.tr("Comillas Simples ' '"))
        box.addWidget(self.check_single_quote, 2, 0)

        group_completion = QGroupBox(self.tr("Completado de Código:"))
        box = QGridLayout(group_completion)
        box.setContentsMargins(20, 5, 20, 5)
        self.check_completion = QCheckBox(self.tr("Activar Completado"))
        box.addWidget(self.check_completion, 0, 0)
        self.check_document = QCheckBox(self.tr("Basado en el código"))
        box.addWidget(self.check_document, 0, 1)
        self.check_keywords = QCheckBox(self.tr("Palabras Claves"))
        box.addWidget(self.check_keywords, 1, 0)
        self.check_cs = QCheckBox(
            self.tr("Sensitivo a mayúsculas y minúsculas"))
        box.addWidget(self.check_cs, 1, 1)
        self.check_replace_word = QCheckBox(self.tr("Reemplazar Palabra"))
        box.addWidget(self.check_replace_word, 2, 0)
        self.check_show_single = QCheckBox(self.tr("Mostrar Simple"))
        box.addWidget(self.check_show_single, 2, 1)
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(
            self.tr("Número de caractéres para mostrar lista:")))
        self.spin_threshold = QSpinBox()
        self.spin_threshold.setMinimum(1)
        self.spin_threshold.setFixedWidth(100)
        hbox.addWidget(self.spin_threshold)
        box.addLayout(hbox, 3, 0, Qt.AlignLeft)

        # Agrupo al contenedor principal
        container.addWidget(group_complete)
        container.addWidget(group_completion)
        container.addItem(QSpacerItem(0, 10, QSizePolicy.Expanding,
                          QSizePolicy.Expanding))

        self._state_change(self.check_completion.isChecked())
        # Conexiones
        self.check_completion.stateChanged[int].connect(self._state_change)

        # Configuration
        self.check_key.setChecked(
            settings.get_setting('editor/complete-brace'))
        self.check_bracket.setChecked("[" in settings.BRACES)
        self.check_paren.setChecked("(" in settings.BRACES)
        self.check_quote.setChecked('""' in settings.QUOTES)
            #settings.get_setting('editor/complete-double-quote'))
        self.check_single_quote.setChecked("''" in settings.QUOTES)
            #settings.get_setting('editor/complete-single-quote'))
        self.check_completion.setChecked(
            settings.get_setting('editor/completion'))
        self.spin_threshold.setValue(
            settings.get_setting('editor/completion-threshold'))
        self.check_keywords.setChecked(
            settings.get_setting('editor/completion-keywords'))
        self.check_document.setChecked(
            settings.get_setting('editor/completion-document'))
        self.check_cs.setChecked(
            settings.get_setting('editor/completion-cs'))
        self.check_replace_word.setChecked(
            settings.get_setting('editor/completion-replace-word'))
        self.check_show_single.setChecked(
            settings.get_setting('editor/completion-single'))

    def _state_change(self, value):
        state = bool(value)
        self.check_document.setEnabled(state)
        self.check_keywords.setEnabled(state)
        self.check_cs.setEnabled(state)
        self.check_replace_word.setEnabled(state)
        self.check_show_single.setEnabled(state)
        self.spin_threshold.setEnabled(state)

    def save(self):
        settings.set_setting('editor/complete-brace',
            self.check_key.isChecked())
        settings.set_setting('editor/complete-bracket',
            self.check_bracket.isChecked())
        if self.check_bracket.isChecked():
            settings.BRACES['['] = ']'
        elif ('[') in settings.BRACES:
            del settings.BRACES['[']
        settings.set_setting('editor/complete-paren',
            self.check_paren.isChecked())
        if self.check_paren.isChecked():
            settings.BRACES['('] = ')'
        elif ('(') in settings.BRACES:
            del settings.BRACES['(']
        settings.set_setting('editor/complete-double-quote',
            self.check_quote.isChecked())
        if self.check_quote.isChecked():
            settings.QUOTES.append('""')
        elif '""' in settings.QUOTES:
            settings.QUOTES.remove('""')
        settings.set_setting('editor/complete-single-quote',
            self.check_single_quote.isChecked())
        if self.check_single_quote.isChecked():
            settings.QUOTES.append('""')
        elif "''" in settings.QUOTES:
            settings.QUOTES.remove("''")
        code_completion = self.check_completion.isChecked()
        settings.set_setting('editor/completion',
            code_completion)
        settings.set_setting('editor/completion-threshold',
            self.spin_threshold.value())
        settings.set_setting('editor/completion-keywords',
            self.check_keywords.isChecked())
        settings.set_setting('editor/completion-document',
            self.check_document.isChecked())
        settings.set_setting('editor/completion-cs',
            self.check_cs.isChecked())
        settings.set_setting('editor/completion-replace-word',
            self.check_replace_word.isChecked())
        settings.set_setting('editor/completion-single',
            self.check_show_single.isChecked())
        editor_container = Edis.get_component("principal")
        editor = editor_container.get_active_editor()
        if editor is not None:
            editor.active_code_completion(code_completion)


editor_configuration = EditorConfiguration()