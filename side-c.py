#-*- coding: utf-8 -*-
from PyQt4.QtGui import QApplication

import sys
import ide


def main():
    app = QApplication(sys.argv)
    side = ide.IDE()
    side.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()