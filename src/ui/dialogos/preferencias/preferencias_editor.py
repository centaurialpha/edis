# -*- coding: utf-8 -*-
# EDIS - a simple cross-platform IDE for C
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
    QFontDialog,
    QSpacerItem,
    QSizePolicy,
    QRadioButton
    )

# Módulos QtCore
from PyQt4.QtCore import Qt

# Módulos EDIS
#from src import recursos
from src.helpers.configuracion import ESettings
from src.helpers import configuracion
from src.ui.edis_main import EDIS


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
        self.slider_indentacion = QSlider(Qt.Horizontal)
        self.slider_indentacion.setMaximum(20)
        box.addWidget(self.slider_indentacion, 0, 1)
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

        # Cursor
        grupo_cursor = QGroupBox(self.tr("Tipo de cursor:"))
        box = QVBoxLayout(grupo_cursor)
        tipos_cursor = [
            self.tr('Invisible'),
            self.tr('Línea'),
            self.tr('Bloque')
            ]
        self.radio_cursor = []
        [self.radio_cursor.append(QRadioButton(cursor))
            for cursor in tipos_cursor]
        for ntipo, radiob in enumerate(self.radio_cursor):
            box.addWidget(radiob)
            if ntipo == ESettings.get('editor/tipoCursor'):
                radiob.setChecked(True)

        contenedor.addWidget(grupo_margen)
        contenedor.addWidget(grupo_indentacion)
        contenedor.addWidget(grupo_fuente)
        contenedor.addWidget(grupo_cursor)
        contenedor.addItem(QSpacerItem(0, 10, QSizePolicy.Expanding,
                           QSizePolicy.Expanding))

        # Conexiones
        self.slider_margen.valueChanged[int].connect(lcd_margen.display)
        self.slider_indentacion.valueChanged[int].connect(
            lcd_indentacion.display)
        self.btn_fuente.clicked.connect(self._seleccionar_fuente)

        # Configuraciones
        # Márgen
        self.check_margen.setChecked(ESettings.get('editor/margen'))
        self.slider_margen.setValue(ESettings.get('editor/margenAncho'))
        # Indentación
        self.check_indentacion.setChecked(ESettings.get(
                                          'editor/indentacion'))
        self.slider_indentacion.setValue(ESettings.get(
                                         'editor/indentacionAncho'))
        self.check_guia.setChecked(ESettings.get('editor/guias'))

    def _cargar_fuente(self):
        fuente = ESettings.get('editor/fuente')
        if not fuente:
            fuente = configuracion.FUENTE
        size = str(ESettings.get('editor/fuenteTam'))
        texto = fuente + ', ' + size
        self.btn_fuente.setText(texto)

    def _seleccionar_fuente(self):
        seleccion, ok = QFontDialog.getFont()
        if ok:
            fuente = seleccion.family()
            size = str(seleccion.pointSize())
            self.btn_fuente.setText(fuente + ', ' + size)

    def guardar(self):
        """ Guarda las configuraciones del Editor. """

        fuente, fuente_tam = self.btn_fuente.text().split(',')
        ESettings.set('editor/fuente', fuente)
        ESettings.set('editor/fuenteTam', int(fuente_tam.strip()))
        ESettings.set('editor/margen', self.check_margen.isChecked())
        ESettings.set('editor/margenAncho', self.slider_margen.value())
        ESettings.set('editor/guias', self.check_guia.isChecked())
        ESettings.set('editor/indentacionAncho',
                      self.slider_indentacion.value())
        for ntipo, radio in enumerate(self.radio_cursor):
            if radio.isChecked():
                tipo = ntipo
        ESettings.set('editor/tipoCursor', tipo)
        principal = EDIS.componente("principal")
        weditor = principal.devolver_editor()
        if weditor is not None:
            weditor.cargar_fuente(fuente, int(fuente_tam))
            weditor.actualizar()
            weditor.actualizar_margen()
            weditor.actualizar_indentacion()