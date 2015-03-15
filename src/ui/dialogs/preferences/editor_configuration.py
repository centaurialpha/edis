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
    QRadioButton,
    QFont
    )

# Módulos QtCore
from PyQt4.QtCore import Qt

# Módulos EDIS
#from src import recursos
from src.helpers.configurations import ESettings
from src.helpers import configurations
from src.ui.main import Edis


class EditorConfiguration(QWidget):
    """ Clase Configuracion Editor """

    def __init__(self):
        super(EditorConfiguration, self).__init__()
        contenedor = QVBoxLayout(self)

        # Márgen de línea
        grupo_margen = QGroupBox(self.tr("Margin:"))
        box = QGridLayout(grupo_margen)
        self.check_margin = QCheckBox(self.tr("Enable"))
        box.addWidget(self.check_margin, 0, 0)
        self.slider_margin = QSlider(Qt.Horizontal)
        self.slider_margin.setMaximum(180)
        box.addWidget(self.slider_margin, 0, 1)
        lcd_margen = QLCDNumber()
        lcd_margen.setStyleSheet("color: #dedede")
        lcd_margen.setSegmentStyle(lcd_margen.Flat)
        box.addWidget(lcd_margen, 0, 2)

        # Indentación
        grupo_indentacion = QGroupBox(self.tr("Indentation:"))
        box = QGridLayout(grupo_indentacion)
        self.check_indentation = QCheckBox(self.tr("Enable"))
        box.addWidget(self.check_indentation, 0, 0)
        self.slider_indentation = QSlider(Qt.Horizontal)
        self.slider_indentation.setMaximum(20)
        box.addWidget(self.slider_indentation, 0, 1)
        lcd_indentacion = QLCDNumber()
        lcd_indentacion.setStyleSheet("color: #dedede")
        lcd_indentacion.setSegmentStyle(lcd_indentacion.Flat)
        box.addWidget(lcd_indentacion, 0, 2)
        self.check_guides = QCheckBox(self.tr("Enable indentation guides"))
        box.addWidget(self.check_guides, 1, 0)

        # Extras
        group_extras = QGroupBox(self.tr("Extras:"))
        box = QGridLayout(group_extras)
        self.check_style_checker = QCheckBox(self.tr("Style checker"))
        self.check_style_checker.setChecked(ESettings.get(
                                            'editor/style-checker'))
        self.check_minimap = QCheckBox(self.tr(
            "Minimap (need restart the editor)"))
        self.check_minimap.setChecked(ESettings.get('editor/show-minimap'))
        box.addWidget(self.check_minimap, 1, 1)
        box.addWidget(self.check_style_checker, 1, 0)

        # Tipo de letra
        grupo_fuente = QGroupBox(self.tr("Font type:"))
        box = QHBoxLayout(grupo_fuente)
        self.btn_font = QPushButton()
        self.btn_font.setObjectName("custom")
        self.btn_font.setMaximumWidth(250)
        self._cargar_fuente()
        box.addWidget(self.btn_font)
        box.addStretch(1)

        # Cursor
        grupo_cursor = QGroupBox(self.tr("Cursor type:"))
        box = QVBoxLayout(grupo_cursor)
        tipos_cursor = [
            self.tr('None'),
            self.tr('Line'),
            self.tr('Block')
            ]
        self.radio_cursor = []
        [self.radio_cursor.append(QRadioButton(cursor))
            for cursor in tipos_cursor]
        for ntipo, radiob in enumerate(self.radio_cursor):
            box.addWidget(radiob)
            if ntipo == ESettings.get('editor/cursor'):
                radiob.setChecked(True)

        contenedor.addWidget(grupo_margen)
        contenedor.addWidget(grupo_indentacion)
        contenedor.addWidget(group_extras)
        contenedor.addWidget(grupo_fuente)
        contenedor.addWidget(grupo_cursor)
        contenedor.addItem(QSpacerItem(0, 10, QSizePolicy.Expanding,
                           QSizePolicy.Expanding))

        # Conexiones
        self.slider_margin.valueChanged[int].connect(lcd_margen.display)
        self.slider_indentation.valueChanged[int].connect(
            lcd_indentacion.display)
        self.btn_font.clicked.connect(self._seleccionar_fuente)

        # Configuraciones
        # Márgen
        self.check_margin.setChecked(ESettings.get('editor/show-margin'))
        self.slider_margin.setValue(ESettings.get('editor/width-margin'))
        # Indentación
        self.check_indentation.setChecked(ESettings.get('editor/indent'))
        self.slider_indentation.setValue(ESettings.get(
                                         'editor/width-indent'))
        self.check_guides.setChecked(ESettings.get('editor/show-guides'))

    def _cargar_fuente(self):
        fuente = ESettings.get('editor/font')
        if not fuente:
            fuente = configurations.DEFAULT_FONT
        size = str(ESettings.get('editor/size-font'))
        texto = fuente + ', ' + size
        self.btn_font.setText(texto)

    def _seleccionar_fuente(self):
        initial_font = QFont(ESettings.get('editor/font'),
            ESettings.get('editor/size-font'))
        seleccion, ok = QFontDialog.getFont(initial_font)
        if ok:
            fuente = seleccion.family()
            size = str(seleccion.pointSize())
            self.btn_font.setText(fuente + ', ' + size)

    def guardar(self):
        """ Guarda las configuraciones del Editor. """

        fuente, fuente_tam = self.btn_font.text().split(',')
        ESettings.set('editor/font', fuente)
        ESettings.set('editor/size-font', int(fuente_tam.strip()))
        ESettings.set('editor/show-margin', self.check_margin.isChecked())
        ESettings.set('editor/width-margin', self.slider_margin.value())
        ESettings.set('editor/show-guides', self.check_guides.isChecked())
        ESettings.set('editor/show-minimap', self.check_minimap.isChecked())
        checker_value = self.check_style_checker.isChecked()
        ESettings.set('editor/style-checker', checker_value)
        ESettings.set('editor/indent', self.check_indentation.isChecked())
        ESettings.set('editor/width-indent', self.slider_indentation.value())
        for ntipo, radio in enumerate(self.radio_cursor):
            if radio.isChecked():
                tipo = ntipo
        ESettings.set('editor/cursor', tipo)
        principal = Edis.get_componente("principal")
        weditor = principal.get_active_editor()
        if weditor is not None:
            weditor.cargar_fuente(fuente, int(fuente_tam))
            weditor.actualizar()
            weditor.actualizar_margen()
            weditor.actualizar_indentacion()
            weditor.load_checker(checker_value)