# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
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
    QFontComboBox
    )

# Módulos QtCore
from PyQt4.QtCore import (
    Qt,
    #SIGNAL
    )

# Módulos EDIS
# from src import recursos
from src.core import settings
from src.ui.main import Edis


class EditorConfiguration(QTabWidget):

    __TABS = OrderedDict()

    def __init__(self):
        super(EditorConfiguration, self).__init__()
        self.general = GeneralSection()
        self.display = DisplaySection()
        #self.theme = ThemeSection()
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
        group_indentation = QGroupBox(self.tr("Tabs and Indentation:"))
        box = QGridLayout(group_indentation)
        box.setContentsMargins(20, 5, 20, 5)
        box.addWidget(QLabel(self.tr("Tabs policy:")), 0, 0)
        self.combo_tabs = QComboBox()
        self.combo_tabs.setFixedWidth(350)
        self.combo_tabs.addItems([
            self.tr("Spaces Only"),
            self.tr("Tabs Only"),
            ])
        box.addWidget(self.combo_tabs, 0, 1)
        self.combo_tabs.setCurrentIndex(
            int(settings.get_setting('editor/usetabs')))
        # Auto indent
        self.check_autoindent = QCheckBox(self.tr("Auto indent"))
        box.addWidget(self.check_autoindent, 1, 0)
        box.setAlignment(Qt.AlignLeft)
        self.check_autoindent.setChecked(settings.get_setting('editor/indent'))

        # Minimap
        group_minimap = QGroupBox(self.tr("Minimap:"))
        box = QGridLayout(group_minimap)
        box.setContentsMargins(20, 5, 20, 5)
        self.check_minimap = QCheckBox(
            self.tr("Show minimap (requieres restart)"))
        self.check_minimap.setChecked(settings.get_setting('editor/minimap'))
        box.addWidget(self.check_minimap, 0, 0)
        self.check_minimap_animation = QCheckBox(self.tr("Enable animation"))
        self.check_minimap_animation.setChecked(
            settings.get_setting('editor/minimap-animation'))
        box.addWidget(self.check_minimap_animation, 1, 0)
        box.addWidget(QLabel(self.tr("Size Area:")), 2, 0)
        self.spin_area_minimap = QSpinBox()
        self.spin_area_minimap.setFixedWidth(350)
        box.addWidget(self.spin_area_minimap, 2, 1)
        box.setAlignment(Qt.AlignLeft)

        # Font
        group_typo = QGroupBox(self.tr("Font:"))
        box = QGridLayout(group_typo)
        box.setContentsMargins(20, 5, 20, 5)
        box.addWidget(QLabel(self.tr("Family:")), 0, 0)
        self.combo_font = QFontComboBox()
        self.combo_font.setFixedWidth(350)
        box.addWidget(self.combo_font, 0, 1)
        box.addWidget(QLabel(self.tr("Size:")), 1, 0)
        self.spin_size_font = QSpinBox()
        self.spin_size_font.setValue(settings.get_setting('editor/size-font'))
        self.spin_size_font.setFixedWidth(350)
        box.addWidget(self.spin_size_font, 1, 1)
        box.setAlignment(Qt.AlignLeft)

        # Scheme
        group_scheme = QGroupBox(self.tr("Scheme:"))
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
        box.addWidget(QLabel(self.tr("Requires restart Editor")))

        ## Agrupación
        main_container.addWidget(group_indentation)
        main_container.addWidget(group_minimap)
        main_container.addWidget(group_typo)
        main_container.addWidget(group_scheme)
        main_container.addItem(QSpacerItem(0, 10, QSizePolicy.Expanding,
                               QSizePolicy.Expanding))

        EditorConfiguration.install_widget(self.tr("General"), self)

        # Conexiones
        self.combo_scheme.currentIndexChanged['const QString&'].connect(
            self._change_scheme)

    def _change_scheme(self, theme):
        theme = theme.split()[0].lower()
        editor_container = Edis.get_component("principal")
        editor = editor_container.get_active_editor()
        if editor is not None:
            # Restyle
            pass

    def _type_changed(self, index):
        self.spin_caret_width.setEnabled(bool(index))

    def _load_font(self):
        fuente = settings.get_setting('editor/font')
        if not fuente:
            fuente = settings.DEFAULT_FONT
        size = str(settings.get_setting('editor/size-font'))
        texto = fuente + ', ' + size
        self.btn_font.setText(texto)

    def save(self):
        """ Guarda las configuraciones del Editor. """

        #FIXME: actualizar autoindent
        #FIXME: animacion y area de minimap
        use_tabs = bool(self.combo_tabs.currentIndex())
        settings.set_setting('editor/usetabs', use_tabs)
        auto_indent = self.check_autoindent.isChecked()
        settings.set_setting('editor/indent', auto_indent)
        settings.set_setting('editor/minimap', self.check_minimap.isChecked())
        settings.set_setting('editor/minimap-animation',
                             self.check_minimap_animation.isChecked())
        font = self.combo_font.currentFont().family()
        settings.set_setting('editor/font', font)
        font_size = self.spin_size_font.value()
        settings.set_setting('editor/size-font', font_size)
        scheme = self.combo_scheme.currentText().split()[0].lower()
        settings.set_setting('editor/scheme', scheme)
        editor_container = Edis.get_component("principal")
        editor = editor_container.get_active_editor()
        if editor is not None:
            editor.setIndentationsUseTabs(use_tabs)
            editor.load_font(font, font_size)
        #settings.set_setting('editor/show-margin',
                             #self.check_margin.isChecked())
        ##settings.set_setting('editor/width-margin',
                             #self.slider_margin.value())
        #settings.set_setting('editor/show-guides',
                             #self.check_guides.isChecked())
        #settings.set_setting('editor/show-minimap',
                             #self.check_minimap.isChecked())
        #checker_value = self.check_style_checker.isChecked()
        #settings.set_setting('editor/style-checker', checker_value)
        #settings.set_setting('editor/indent',
                             #self.check_indentation.isChecked())
        #settings.set_setting('editor/width-indent',
                             #self.slider_indentation.value())
        #settings.set_setting('editor/cursor',
                             #self.combo_caret.currentIndex())
        #settings.set_setting('editor/caret-width',
                             #self.spin_caret_width.value())
        #settings.set_setting('editor/cursor-period',
                             #self.cursor_slider.value())
        #code_completion = self.check_completion.isChecked()
        #settings.set_setting('editor/completion', code_completion)
        #principal = Edis.get_component("principal")
        #weditor = principal.get_active_editor()
        #if weditor is not None:
            ##weditor.load_font(fuente, int(fuente_tam))
            #weditor.update_options()
            #weditor.update_margin()
            #weditor.update_indentation()
            #weditor.load_checker(checker_value)
            #weditor.active_code_completion(code_completion)


class DisplaySection(QWidget):

    def __init__(self):
        super(DisplaySection, self).__init__()
        EditorConfiguration.install_widget(self.tr("Display"), self)
        container = QVBoxLayout(self)

        # Text wrapping
        group_wrapping = QGroupBox(self.tr("Text Wrapping:"))
        box = QGridLayout(group_wrapping)
        self.check_wrap = QCheckBox(self.tr("Enable text wrapping"))
        box.addWidget(self.check_wrap, 0, 0)
        self.check_margin = QCheckBox(self.tr("Display right margin at:"))
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
        group_extras = QGroupBox(self.tr("Display:"))
        box = QGridLayout(group_extras)
        self.check_line_numbers = QCheckBox(self.tr("Display line numbers"))
        box.addWidget(self.check_line_numbers, 0, 0)
        self.check_current_line = QCheckBox(self.tr("Highlight current line"))
        box.addWidget(self.check_current_line, 0, 1)
        self.check_mark_change = QCheckBox(self.tr("Mark text changes"))
        box.addWidget(self.check_mark_change, 1, 0)
        self.check_match_brace = QCheckBox(
            self.tr("Highlight matching braces"))
        box.addWidget(self.check_match_brace, 1, 1)
        self.check_whitespace = QCheckBox(self.tr("Visualize whitespace"))
        box.addWidget(self.check_whitespace, 2, 0)
        self.check_guides = QCheckBox(self.tr("Visualize indentation guides"))
        box.addWidget(self.check_guides, 2, 1)
        self.check_eof = QCheckBox(self.tr("Display platform end of line"))
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
        EditorConfiguration.install_widget(self.tr("Completion"), self)
        container = QVBoxLayout(self)

        group_complete = QGroupBox(self.tr("Complete:"))
        box = QGridLayout(group_complete)
        box.setContentsMargins(20, 5, 20, 5)
        self.check_bracket = QCheckBox(self.tr("Brackets []"))
        box.addWidget(self.check_bracket, 0, 0)
        self.check_paren = QCheckBox(self.tr("Parentheses ()"))
        box.addWidget(self.check_paren, 0, 1)
        self.check_key = QCheckBox(self.tr("Keys {}"))
        box.addWidget(self.check_key, 1, 0)
        self.check_quote = QCheckBox(self.tr("Double Quotes \" \""))
        box.addWidget(self.check_quote, 1, 1)
        self.check_single_quote = QCheckBox(self.tr("Single Quotes ' '"))
        box.addWidget(self.check_single_quote, 2, 0)

        group_completion = QGroupBox(self.tr("Code Completion:"))
        box = QGridLayout(group_completion)
        box.setContentsMargins(20, 5, 20, 5)
        self.check_completion = QCheckBox(self.tr("Active Code Completion"))
        box.addWidget(self.check_completion, 0, 0)
        self.check_document = QCheckBox(self.tr("Based on Document"))
        box.addWidget(self.check_document, 0, 1)
        self.check_keywords = QCheckBox(self.tr("Keywords"))
        box.addWidget(self.check_keywords, 1, 0)
        self.check_cs = QCheckBox(self.tr("Case Sensitive"))
        box.addWidget(self.check_cs, 1, 1)
        self.check_replace_word = QCheckBox(self.tr("Replace Word"))
        box.addWidget(self.check_replace_word, 2, 0)
        self.check_show_single = QCheckBox(self.tr("Show Single"))
        box.addWidget(self.check_show_single, 2, 1)
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(self.tr("Threshold:")))
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
        self.check_bracket.setChecked(
            settings.get_setting('editor/complete-bracket'))
        self.check_paren.setChecked(
            settings.get_setting('editor/complete-paren'))
        self.check_quote.setChecked(
            settings.get_setting('editor/complete-double-quote'))
        self.check_single_quote.setChecked(
            settings.get_setting('editor/complete-single-quote'))
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
        settings.set_setting('editor/complete-bracket',
            self.check_bracket.isChecked())
        settings.set_setting('editor/complete-paren',
            self.check_paren.isChecked())
        settings.set_setting('editor/complete-double-quote',
            self.check_quote.isChecked())
        settings.set_setting('editor/complete-single-quote',
            self.check_single_quote.isChecked())
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


## Cursor
        #grupo_cursor = QGroupBox(self.tr("Caret:"))
        #box = QGridLayout(grupo_cursor)
        #box.setAlignment(Qt.AlignLeft)
        ## Type
        #box.addWidget(QLabel(self.tr("Type:")), 0, 0)
        #self.combo_caret = QComboBox()
        #self.combo_caret.setFixedWidth(300)
        #caret_types = [
            #self.tr('None'),
            #self.tr('Line'),
            #self.tr('Block')
            #]
        #self.combo_caret.addItems(caret_types)
        #index = settings.get_setting('editor/cursor')
        #self.combo_caret.setCurrentIndex(index)
        #box.addWidget(self.combo_caret, 0, 1, Qt.AlignLeft)
        ## Width
        #box.addWidget(QLabel(self.tr("Width:")), 1, 0)
        #self.spin_caret_width = QSpinBox()
        #self.spin_caret_width.setFixedWidth(300)
        #if index != 1:
            #self.spin_caret_width.setEnabled(False)
        #self.spin_caret_width.setRange(1, 3)
        #self.spin_caret_width.setValue(
            #settings.get_setting('editor/caret-width'))
        #box.addWidget(self.spin_caret_width, 1, 1, Qt.AlignLeft)
        ## Period
        #box.addWidget(QLabel(self.tr("Period (ms):")), 2, 0)
        #self.cursor_slider = QSlider(Qt.Horizontal)
        #self.cursor_slider.setMaximum(500)
        #self.cursor_slider.setFixedWidth(300)
        #box.addWidget(self.cursor_slider, 2, 1, Qt.AlignLeft)
        #lcd_caret = QLCDNumber()
        #lcd_caret.setSegmentStyle(QLCDNumber.Flat)
        #box.addWidget(lcd_caret, 2, 3)