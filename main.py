from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from poloniexAPI import *
import sys
from scipy.sparse.csgraph import _validation  

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()


def main():
    app = QApplication(sys.argv)
    instance = Main()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
