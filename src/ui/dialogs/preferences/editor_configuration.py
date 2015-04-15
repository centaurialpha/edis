# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
#
# This file is part of Edis
# Copyright 2014-2015 - Edis Team
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

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
    QPushButton,
    QFontDialog,
    QSpacerItem,
    QSizePolicy,
    QFont,
    QLabel,
    QComboBox,
    QSpinBox,
    QTabWidget
    )

# Módulos QtCore
from PyQt4.QtCore import (
    Qt,
    SIGNAL
    )

# Módulos EDIS
# from src import recursos
from src.core import settings
from src.ui.main import Edis


class EditorConfiguration(QTabWidget):

    def __init__(self, parent=None):
        super(EditorConfiguration, self).__init__()
        self.general = GeneralSection()
        self.addTab(self.general, self.tr("General"))
        self.addTab(QWidget(), self.tr("Display"))
        self.addTab(QWidget(), self.tr("Theme"))
        self.addTab(QWidget(), self.tr("Completion"))

    def guardar(self):
        pass


class GeneralSection(QWidget):
    """ Clase Configuracion Editor """

    def __init__(self):
        super(GeneralSection, self).__init__()
        main_container = QVBoxLayout(self)

        # Contiene todos los widgets
        container = QWidget()
        main_grid = QGridLayout(container)

        # Márgen de línea
        group_margen = QGroupBox(self.tr("Margin:"))
        box = QGridLayout(group_margen)
        self.check_margin = QCheckBox(self.tr("Enable"))
        box.addWidget(self.check_margin, 0, 0)
        self.slider_margin = QSlider(Qt.Horizontal)
        self.slider_margin.setMaximum(180)
        self.slider_margin.setFixedWidth(350)
        box.addWidget(self.slider_margin, 0, 1)
        lcd_margen = QLCDNumber()
        lcd_margen.setSegmentStyle(lcd_margen.Flat)
        box.addWidget(lcd_margen, 0, 2)
        main_grid.addWidget(group_margen, 0, 0)

        # Indentación
        group_indentation = QGroupBox(self.tr("Indentation:"))
        box = QGridLayout(group_indentation)
        self.check_indentation = QCheckBox(self.tr("Enable"))
        box.addWidget(self.check_indentation, 0, 0)
        self.slider_indentation = QSlider(Qt.Horizontal)
        self.slider_indentation.setMaximum(20)
        self.slider_indentation.setFixedWidth(350)
        box.addWidget(self.slider_indentation, 0, 1)
        lcd_indentacion = QLCDNumber()
        lcd_indentacion.setSegmentStyle(lcd_indentacion.Flat)
        box.addWidget(lcd_indentacion, 0, 2)
        self.check_guides = QCheckBox(self.tr("Enable indentation guides"))
        box.addWidget(self.check_guides, 1, 0)
        main_grid.addWidget(group_indentation, 0, 1)

        # Agrupación
        main_container.addWidget(container)
        main_container.addItem(QSpacerItem(0, 10, QSizePolicy.Expanding,
                               QSizePolicy.Expanding))
        ## Indentación

        ## Extras
        #group_extras = QGroupBox(self.tr("Extras:"))
        #box = QGridLayout(group_extras)
        #self.check_style_checker = QCheckBox(self.tr("Style checker (beta)"))
        #self.check_style_checker.setChecked(settings.get_setting(
                                            #'editor/style-checker'))
        #self.check_minimap = QCheckBox(self.tr(
            #"Minimap (need restart the editor)"))
        #self.check_minimap.setChecked(
            #settings.get_setting('editor/show-minimap'))
        #box.addWidget(self.check_minimap, 1, 1)
        #box.addWidget(self.check_style_checker, 1, 0)

        ## Tipo de letra
        #grupo_fuente = QGroupBox(self.tr("Font type:"))
        #box = QHBoxLayout(grupo_fuente)
        #self.btn_font = QPushButton()
        #self.btn_font.setObjectName("custom")
        #self.btn_font.setMaximumWidth(250)
        #self._cargar_fuente()
        #box.addWidget(self.btn_font)
        #box.addStretch(1)

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
        ## Code completion
        ##group_completion = QGroupBox(self.tr("Code Completion:"))
        ##box = QVBoxLayout(group_completion)
        ##self.check_completion = QCheckBox(self.tr("Enable code completion"))
        ##self.check_completion.setChecked(
            ##settings.get_setting('editor/completion'))
        ##box.addWidget(self.check_completion)

        #contenedor.addWidget(grupo_margen)
        #contenedor.addWidget(grupo_indentacion)
        #contenedor.addWidget(group_extras)
        #contenedor.addWidget(grupo_fuente)
        #contenedor.addWidget(grupo_cursor)
        ##contenedor.addWidget(group_completion)

        # Conexiones
        #self.connect(self.combo_caret, SIGNAL("currentIndexChanged(int)"),
                     #self._type_changed)
        #self.connect(self.slider_margin, SIGNAL("valueChanged(int)"),
                     #lcd_marge.display)
        #self.connect(self.slider_indentation, SIGNAL("valueChanged(int)"),
                     #lcd_indentation.display)
        #self.connect(self.cursor_slider, SIGNAL("valueChanged(int)"),
                     #lcd_caret.display)
        #self.connect(self.btn_font, SIGNAL("clicked()"),
                     #self._select_font)

        # Configuraciones
        # Márgen
        #self.check_margin.setChecked(
            #settings.get_setting('editor/show-margin'))
        #self.slider_margin.setValue(
            #settings.get_setting('editor/width-margin'))
        ## Indentación
        #self.check_indentation.setChecked(
            #settings.get_setting('editor/indent'))
        #self.slider_indentation.setValue(settings.get_setting(
                                         #'editor/width-indent'))
        #self.check_guides.setChecked(
            #settings.get_setting('editor/show-guides'))
        #self.cursor_slider.setValue(
            #settings.get_setting('editor/cursor-period'))

    def _type_changed(self, index):
        self.spin_caret_width.setEnabled(bool(index))

    def _load_font(self):
        fuente = settings.get_setting('editor/font')
        if not fuente:
            fuente = settings.DEFAULT_FONT
        size = str(settings.get_setting('editor/size-font'))
        texto = fuente + ', ' + size
        self.btn_font.setText(texto)

    def _select_font(self):
        initial_font = QFont(settings.get_setting('editor/font'),
                             settings.get_setting('editor/size-font'))
        seleccion, ok = QFontDialog.getFont(initial_font)
        if ok:
            fuente = seleccion.family()
            size = str(seleccion.pointSize())
            self.btn_font.setText(fuente + ', ' + size)

    def guardar(self):
        """ Guarda las configuraciones del Editor. """

        fuente, fuente_tam = self.btn_font.text().split(',')
        settings.set_setting('editor/font', fuente)
        settings.set_setting('editor/size-font', int(fuente_tam.strip()))
        settings.set_setting('editor/show-margin',
                             self.check_margin.isChecked())
        settings.set_setting('editor/width-margin',
                             self.slider_margin.value())
        settings.set_setting('editor/show-guides',
                             self.check_guides.isChecked())
        settings.set_setting('editor/show-minimap',
                             self.check_minimap.isChecked())
        checker_value = self.check_style_checker.isChecked()
        settings.set_setting('editor/style-checker', checker_value)
        settings.set_setting('editor/indent',
                             self.check_indentation.isChecked())
        settings.set_setting('editor/width-indent',
                             self.slider_indentation.value())
        settings.set_setting('editor/cursor',
                             self.combo_caret.currentIndex())
        settings.set_setting('editor/caret-width',
                             self.spin_caret_width.value())
        settings.set_setting('editor/cursor-period',
                             self.cursor_slider.value())
        code_completion = self.check_completion.isChecked()
        settings.set_setting('editor/completion', code_completion)
        principal = Edis.get_component("principal")
        weditor = principal.get_active_editor()
        if weditor is not None:
            weditor.load_font(fuente, int(fuente_tam))
            weditor.update_options()
            weditor.update_margin()
            weditor.update_indentation()
            weditor.load_checker(checker_value)
            weditor.active_code_completion(code_completion)
