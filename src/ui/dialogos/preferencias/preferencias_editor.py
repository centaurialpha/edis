# -*- coding: utf-8 -*-
# EDIS - Entorno de Desarrollo Integrado Simple para C/C++
#
# This file is part of EDIS
# Copyright 2014-2015 - Gabriel Acosta
# License: GPLv3 (see http://www.gnu.org/licenses/gpl.html)

# Módulos QtGui
from PyQt4.QtGui import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QTabWidget,
    QGroupBox,
    QHBoxLayout,
    QCheckBox,
    QSlider,
    QLCDNumber,
    QPushButton,
    QFontDialog
    )

# Módulos QtCore
from PyQt4.QtCore import (
    Qt,
    QSettings
    )

# Módulos EDIS
from src import recursos
from src.helpers import configuracion


class TabEditor(QWidget):
    """ Tab Editor """

    def __init__(self):
        super(TabEditor, self).__init__()
        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(0, 0, 0, 0)
        self.setObjectName("tabs")
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(3)
        self.configEditor = CaracteristicasEditor()
        self.tabs.addTab(self.configEditor, self.trUtf8("Características"))

        vbox.addWidget(self.tabs)

    def guardar(self):
        for i in range(self.tabs.count()):
            self.tabs.widget(i).guardar()


class CaracteristicasEditor(QWidget):
    """ Clase Configuracion Editor """

    def __init__(self):
        super(CaracteristicasEditor, self).__init__()
        contenedor = QVBoxLayout(self)
        self.esettings = configuracion.ESettings()
        # Márgen de línea
        grupo_margen = QGroupBox(self.tr("Márgen:"))
        box = QGridLayout(grupo_margen)
        self.check_margen = QCheckBox(self.tr("Mostrar"))
        box.addWidget(self.check_margen, 0, 0)
        self.slider_margen = QSlider(Qt.Horizontal)
        self.slider_margen.setMaximum(180)
        box.addWidget(self.slider_margen, 0, 1)
        lcd_margen = QLCDNumber()
        lcd_margen.setStyleSheet("color: #dedede")
        lcd_margen.setSegmentStyle(lcd_margen.Flat)
        box.addWidget(lcd_margen, 0, 2)

        # Indentación
        grupo_indentacion = QGroupBox(self.tr("Indentación:"))
        box = QGridLayout(grupo_indentacion)
        self.check_indentacion = QCheckBox(self.tr("Activar"))
        box.addWidget(self.check_indentacion, 0, 0)
        slider_indentacion = QSlider(Qt.Horizontal)
        slider_indentacion.setMaximum(20)
        box.addWidget(slider_indentacion, 0, 1)
        lcd_indentacion = QLCDNumber()
        lcd_indentacion.setStyleSheet("color: #dedede")
        lcd_indentacion.setSegmentStyle(lcd_indentacion.Flat)
        box.addWidget(lcd_indentacion, 0, 2)
        self.check_guia = QCheckBox(self.tr("Activar guías"))
        box.addWidget(self.check_guia, 1, 0)

        # Tipo de letra
        grupo_fuente = QGroupBox(self.tr("Tipo de letra:"))
        box = QHBoxLayout(grupo_fuente)
        self.btn_fuente = QPushButton()
        self.btn_fuente.setObjectName("custom")
        self.btn_fuente.setMaximumWidth(250)
        self._cargar_fuente()
        box.addWidget(self.btn_fuente)
        box.addStretch(1)

        contenedor.addWidget(grupo_margen)
        contenedor.addWidget(grupo_indentacion)
        contenedor.addWidget(grupo_fuente)

        # Conexiones
        self.slider_margen.valueChanged[int].connect(lcd_margen.display)
        slider_indentacion.valueChanged[int].connect(lcd_indentacion.display)
        self.btn_fuente.clicked.connect(self._seleccionar_fuente)

        # Configuraciones
        # Márgen
        self.check_margen.setChecked(self.esettings.get('editor/margen'))
        self.slider_margen.setValue(self.esettings.get('editor/margenAncho'))
        # Indentación
        self.check_indentacion.setChecked(self.esettings.get(
                                         'editor/indentacion'))
        slider_indentacion.setValue(self.esettings.get(
                                   'editor/indentacionAncho'))
        self.check_guia.setChecked(self.esettings.get('editor/guias'))

    def _cargar_fuente(self):
        fuente = configuracion.FUENTE
        size = str(configuracion.TAM_FUENTE)
        texto = fuente + ', ' + size
        self.btn_fuente.setText(texto)

    def _seleccionar_fuente(self):
        seleccion, ok = QFontDialog.getFont()
        if ok:
            fuente = seleccion.family()
            size = str(seleccion.pointSize())
            configuracion.FUENTE = fuente
            configuracion.TAM_FUENTE = int(size)
            self.btn_fuente.setText(fuente + ', ' + size)

    def guardar(self):
        """ Guarda las configuraciones del Editor. """

        config = QSettings(recursos.CONFIGURACION, QSettings.IniFormat)
        configuracion.FUENTE = self.btn_fuente.text().split(',')[0]
        config.setValue('configuraciones/editor/fuente',
                        configuracion.FUENTE)
        self.esettings.set('editor/margenAncho', self.slider_margen.value())
        config.setValue('editor/margenAncho',
                        self.esettings.get('editor/margenAncho'))
