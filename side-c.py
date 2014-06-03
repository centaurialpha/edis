#-*- coding: utf-8 -*-
from PyQt4.QtGui import QApplication

from side_c.interfaz.ide import Ide
import sys


def main():
    app = QApplication(sys.argv)
    side = Ide.IDE()
    side.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()