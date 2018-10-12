from poloniex import Poloniex
import pandas as pd
from time import time
from time import strptime, localtime, mktime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1852, 771)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton1.setGeometry(QtCore.QRect(1450, 290, 191, 51))
        self.pushButton1.setObjectName("pushButton1")
        self.pushButton1.clicked.connect(self.openFileNameDialog)
        self.lineEdit1 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit1.setGeometry(QtCore.QRect(480, 300, 941, 41))
        self.lineEdit1.setReadOnly(True)
        self.lineEdit1.setObjectName("lineEdit1")
        self.label1 = QtWidgets.QLabel(self.centralwidget)
        self.label1.setGeometry(QtCore.QRect(70, 303, 381, 41))
        self.label1.setObjectName("label1")
        self.comboBox1 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox1.setGeometry(QtCore.QRect(480, 360, 941, 40))
        self.comboBox1.setObjectName("comboBox1")
        self.comboBox1.addItems(timeframes)
        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(70, 370, 371, 34))
        self.label2.setObjectName("label2")
        self.label3 = QtWidgets.QLabel(self.centralwidget)
        self.label3.setGeometry(QtCore.QRect(100, 70, 1571, 161))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label3.setFont(font)
        self.label3.setAlignment(QtCore.Qt.AlignCenter)
        self.label3.setObjectName("label3")
        self.label4 = QtWidgets.QLabel(self.centralwidget)
        self.label4.setGeometry(QtCore.QRect(70, 430, 361, 34))
        self.label4.setObjectName("label4")
        self.comboBox2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox2.setGeometry(QtCore.QRect(480, 430, 941, 40))
        self.comboBox2.setObjectName("comboBox2")
        #self.comboBox2.addItems(pairs)
        self.pushButton2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton2.setGeometry(QtCore.QRect(1450, 420, 201, 51))
        self.pushButton2.setObjectName("pushButton2")
        self.pushButton2.clicked.connect(self.updateTickers)
        self.pushButton3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton3.setGeometry(QtCore.QRect(480, 610, 941, 91))
        self.pushButton3.clicked.connect(self.getHistPrice)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton3.setFont(font)
        self.pushButton3.setObjectName("pushButton3")
        self.label5 = QtWidgets.QLabel(self.centralwidget)
        self.label5.setGeometry(QtCore.QRect(70, 490, 381, 34))
        self.label5.setObjectName("label5")
        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit.setGeometry(QtCore.QRect(1240, 490, 181, 40))
        self.dateEdit.setObjectName("dateEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        #self.openFileNameDialog()
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Poloniex Hist Data"))
        self.pushButton1.setText(_translate("MainWindow", "Choose"))
        self.label1.setText(_translate("MainWindow", "Path for saving historical data"))
        self.label2.setText(_translate("MainWindow", "Select  timeframe in seconds"))
        self.label3.setText(_translate("MainWindow", "Calling Poloniex API\'s for Historical Data"))
        self.label4.setText(_translate("MainWindow", "Choose Tickers"))
        self.pushButton2.setText(_translate("MainWindow", "Update Tickers"))
        self.pushButton3.setText(_translate("MainWindow", "Start Querying Poloniex\'s API\'s"))
        self.label5.setText(_translate("MainWindow", "Select Starting Period"))

    def updateTickers(self, MainWindow):
        self.comboBox2.clear()
        api = Poloniex(jsonNums=float)
        pairs = [pair for pair in api.returnTicker()]
        self.comboBox2.addItems(pairs)
        return pairs
    def openFileNameDialog(self):
        self.lineEdit1.setText(QFileDialog.getExistingDirectory())
    def getHistPrice(self):
        try:
            self.path = self.lineEdit1.text()
            self.timeframe = self.comboBox1.currentText()
            self.ticker = self.comboBox2.currentText()
            self.start = mktime(self.dateEdit.date().toPyDate().timetuple())
            #print(path, timeframe, ticker, start)
            df = pd.DataFrame(api.returnChartData(self.ticker, period=int(self.timeframe), start=self.start))
            #print(df.head())
            df['date'] = pd.to_datetime(df["date"], unit='s')
            df.set_index('date', inplace=True)
            #print(df.tail())
            df.to_excel('{}/{}.xlsx'.format(self.path, self.ticker))
            showdialog("Fatto.")
        except Exception as e:
            showdialog("Eccezione:", e)

def showdialog(text, details="null"):
   msg = QMessageBox()
   msg.setIcon(QMessageBox.Information)
   msg.setText(text)
   msg.setStandardButtons(QMessageBox.Ok)
   msg.setDetailedText(details)
   msg.exec_()

api = Poloniex(jsonNums=float)
pairs = [pair for pair in api.returnTicker()]
#print(pairs)
timeframes = ['300', '900', '1800', '7200', '14400', '86400']
results = list(map(int, timeframes))
