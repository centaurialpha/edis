#-*- coding: utf-8 -*-
import time

from PyQt4.QtGui import QPlainTextEdit
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QTextCharFormat
from PyQt4.QtGui import QTextCursor

from PyQt4.QtCore import QProcess
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import Qt

from side_c import recursos


class EjecutarWidget(QWidget):

    def __init__(self):
        super(EjecutarWidget, self).__init__()
        layoutV = QVBoxLayout(self)
        layoutV.setSpacing(0)
        layoutV.setContentsMargins(0, 0, 0, 0)
        self.output = SalidaWidget(self)
        layoutV.addWidget(self.output)
        self.setLayout(layoutV)

        # Proceso
        self.proceso = QProcess(self)

        # Conexión
        self.connect(self.proceso, SIGNAL("readyReadStandardOutput()"),
            self.output.salida_estandar)
        self.connect(self.proceso, SIGNAL("readyReadStandardError()"),
            self.output.error_estandar)
        self.connect(self.proceso, SIGNAL(
            "finished(int, QProcess::ExitStatus)"), self.ejecucion_terminada)
        self.connect(self.proceso, SIGNAL("error(QProcess::ProcessError)"),
            self.ejecucion_error)

    def correr_compilacion(self, nombre_ejecutable, path):
        """ Se corre el comando gcc para la compilación """

        self.output.setCurrentCharFormat(self.output.formato_ok)

        comando = 'gcc -Wall -o %s %s' % (nombre_ejecutable, path)
        self.proceso.start(comando)
        self.output.setPlainText('Compilando: %s (%s)\n' % (path, time.ctime()))
        self.output.moveCursor(QTextCursor.Down)
        self.output.moveCursor(QTextCursor.Down)

    def ejecucion_terminada(self, codigoError, exitStatus):
        """ valores de codigoError
            0 = Cuando se compila bien, aún con advertencias
            1 = Error en la compilación
        """

        formato = QTextCharFormat()

        self.output.textCursor().insertText('\n')
        if exitStatus == QProcess.NormalExit and codigoError == 0:
            formato.setForeground(Qt.green)
            self.output.textCursor().insertText(
                self.trUtf8("Compilacion Terminada!"), formato)

        else:
            formato.setForeground(Qt.red)
            self.output.textCursor().insertText(
                self.trUtf8("No hubo compilación!"), formato)
        self.output.textCursor().insertText('\n')
        self.output.moveCursor(QTextCursor.Down)

    def ejecucion_error(self, error):
        pass


class SalidaWidget(QPlainTextEdit):

    def __init__(self, parent):
        QPlainTextEdit.__init__(self, parent)
        self._parent = parent
        self.setReadOnly(True)

        # Formato para la salida estándar
        self.formato_ok = QTextCharFormat()
        self.formato_ok.setForeground(Qt.blue)

        # Formato para la salida de error
        self.error_f = QTextCharFormat()
        self.error_f.setForeground(Qt.red)

        # Se carga el estilo
        self.cargar_estilo()

    def cargar_estilo(self):
        """ Carga estilo de color de QPlainTextEdit """

        tema = 'QPlainTextEdit {color: %s; background-color: %s;}' \
        % (recursos.COLOR_EDITOR['texto'],
        recursos.COLOR_EDITOR['fondo-input'])

        self.setStyleSheet(tema)

    def salida_estandar(self):

        cp = self._parent.proceso
        text = cp.readAllStandardOutput().data()
        self.textCursor().insertText(text, self.error_f)

    def error_estandar(self):

        codificacion = 'utf-8'
        cursor = self.textCursor()
        proceso = self._parent.proceso
        texto = proceso.readAllStandardError().data().decode(codificacion)
        cursor.insertText(texto, self.error_f)