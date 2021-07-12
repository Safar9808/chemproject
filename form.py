from ui_form import *
from AIBN import *
from HIn import *
from RH import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pyqtgraph as pg
import scipy
from scipy.interpolate import *
import numpy as np
import random, sys
from scipy.optimize import curve_fit

class Form(Ui_Form, QWidget):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.oxygenButton.clicked.connect(self.setTabIndex)
        self.inhibButton.clicked.connect(self.setTabIndex) 
        self.speedButton.clicked.connect(self.setTabIndex)
        self.ordersButton.clicked.connect(self.setTabIndex)
        self.extentButton.clicked.connect(self.setTabIndex)
        self.kinetButton.clicked.connect(self.setTabIndex)
        self.table1.setVerticalHeaderLabels(['t', 'Δ[O\u2082] '])
        self.task1Graph.setLabels(left='Δ[O\u2082], mol/l', bottom='t, min')
        self.table2.setVerticalHeaderLabels(['[HIn]\u2080 ', 't'])
        self.task2Graph.setLabels(left='t, min', bottom='[HIn]\u2080 \u00B710\u00B3, mol/l')
        self.table3.setVerticalHeaderLabels(['[HIn]\u2080 ', 'W'])
        self.task3Graph.setLabels(left='W\u00B710\u2075, mol/(l\u00B7s)', bottom='[HIn]\u2080 \u00B710\u00B3, mole/l')
        self.x1 = []
        self.x2 = []
        self.x3 = []
        self.y1 = []
        self.y2 = []
        self.y3 = []
        self.x11 = []
        self.x21 = []
        self.x31 = []
        self.y11 = []
        self.y21 = []
        self.y31 = []
        self.dataTable4.setColumnWidth(0, 60)
        self.dataTable4.setColumnWidth(1, 90)
        self.dataTable4.setColumnWidth(2, 90)
        self.dataTable4.setColumnWidth(3, 70)
        self.dataTable4.setColumnWidth(4, 70)
        self.dataTable4.setColumnWidth(5, 70)        
        self.dataTable5.setColumnWidth(0, 60)
        self.dataTable5.setColumnWidth(1, 90)
        self.dataTable5.setColumnWidth(2, 90)
        self.dataTable5.setColumnWidth(3, 70)
        self.dataTable5.setColumnWidth(4, 70)
        self.dataTable5.setColumnWidth(5, 70)        
        self.dataTable6.setColumnWidth(0, 60)
        self.dataTable6.setColumnWidth(1, 90)
        self.dataTable6.setColumnWidth(2, 90)
        self.dataTable6.setColumnWidth(3, 70)
        self.dataTable6.setColumnWidth(4, 70)
        self.dataTable6.setColumnWidth(5, 70)
        self.dataTable4.setHorizontalHeaderLabels(['[HIn]', 'W, mol/(l\u00B7s)', 'Wok, mol/(l\u00B7s)', 'Tau, s','f','F'])
        self.dataTable5.setHorizontalHeaderLabels(['[AIBN]', 'W, mol/(l\u00B7s)', 'Wok, mol/(l\u00B7s)', 'Tau, s','Wi','F'])
        self.dataTable6.setHorizontalHeaderLabels(['[RH]', 'W, mol/(l\u00B7s)', 'Wok, mol/(l\u00B7s)', 'Tau, s','f','F'])
        self.Oop = ['', '', '']
        self.Sr = ['', '', '']

    def setTabIndex(self):
        index = self.buttonsBox.layout().indexOf(self.sender())
        self.taskTabWidget.setCurrentIndex(index)

    @pyqtSlot()
    def on_uploadRB1_clicked(self):
        num = self.sender().objectName()[-1]
        self.findChild(QPushButton, 'openButton' + num).setText('Open')
        self.findChild(QPushButton, 'openButton' + num).setEnabled(True)
        self.findChild(QTableWidget, 'table' + num).setEnabled(False)
        self.findChild(QComboBox, 'oxydMode' + num).setEnabled(False)
        self.findChild(QComboBox, 'inhib1_' + num).setEnabled(False)
        self.findChild(QComboBox, 'temp' + num).setEnabled(False)
        self.findChild(QComboBox, 'inhib2_' + num).setEnabled(False)
        self.findChild(QComboBox, 'hdrc' + num).setEnabled(False)
        self.findChild(QComboBox, 'AIBN' + num).setEnabled(False)

    @pyqtSlot()
    def on_uploadRB2_clicked(self):
        self.on_uploadRB1_clicked()

    @pyqtSlot()
    def on_uploadRB3_clicked(self):
        self.on_uploadRB1_clicked()    

    @pyqtSlot()
    def on_manualRB1_clicked(self):
        num = self.sender().objectName()[-1]
        self.findChild(QPushButton, 'openButton' + num).setEnabled(False)
        self.findChild(QTableWidget, 'table' + num).setEnabled(True)
        self.findChild(QComboBox, 'oxydMode' + num).setEnabled(False)
        self.findChild(QComboBox, 'inhib1_' + num).setEnabled(False)
        self.findChild(QComboBox, 'temp' + num).setEnabled(False)
        self.findChild(QComboBox, 'inhib2_' + num).setEnabled(False)
        self.findChild(QComboBox, 'hdrc' + num).setEnabled(False)
        self.findChild(QComboBox, 'AIBN' + num).setEnabled(False)

    @pyqtSlot()
    def on_manualRB2_clicked(self):
        self.on_manualRB1_clicked()

    @pyqtSlot()
    def on_manualRB3_clicked(self):
        self.on_manualRB1_clicked()

    @pyqtSlot()
    def on_selectRB1_clicked(self):
        num = self.sender().objectName()[-1]
        self.findChild(QPushButton, 'openButton' + num).setEnabled(False)
        self.findChild(QTableWidget, 'table' + num).setEnabled(False)
        self.findChild(QComboBox, 'oxydMode' + num).setEnabled(True)
        self.findChild(QComboBox, 'inhib1_' + num).setEnabled(True)
        self.findChild(QComboBox, 'temp' + num).setEnabled(True)
        self.findChild(QComboBox, 'inhib2_' + num).setEnabled(True)
        self.findChild(QComboBox, 'hdrc' + num).setEnabled(True)
        self.findChild(QComboBox, 'AIBN' + num).setEnabled(True)

    @pyqtSlot()
    def on_selectRB2_clicked(self):
        num = self.sender().objectName()[-1]
        self.findChild(QPushButton, 'openButton' + num).setEnabled(False)
        self.findChild(QTableWidget, 'table' + num).setEnabled(False)
        self.findChild(QComboBox, 'oxydMode' + num).setEnabled(True)
        self.findChild(QComboBox, 'inhib1_' + num).setEnabled(True)
        self.findChild(QComboBox, 'temp' + num).setEnabled(False)
        self.findChild(QComboBox, 'inhib2_' + num).setEnabled(False)
        self.findChild(QComboBox, 'hdrc' + num).setEnabled(False)
        self.findChild(QComboBox, 'AIBN' + num).setEnabled(False)

    @pyqtSlot()
    def on_selectRB3_clicked(self):
        self.on_selectRB2_clicked()

    def floatTryParse(self, value):
        try:
            return float(value), True
        except ValueError:
            return value, False

    @pyqtSlot()
    def on_startButton1_clicked(self):
        num = self.sender().objectName()[-1]
        if self.findChild(QRadioButton, 'manualRB' + num).isChecked():
            x = []
            y = []
            tw = self.findChild(QTableWidget, 'table' + num)
            for i in range(20):
                _x, isX = self.floatTryParse('' if not(tw.item(0, i)) else tw.item(0, i).text())
                _y, isY = self.floatTryParse('' if not(tw.item(1, i)) else tw.item(1, i).text())
                if isX and isY:
                   x.append(_x)
                   y.append(_y)
            globals()['x' + num + '1']  =   x
            globals()['y' + num + '1']  =   y
            globals()['x' + num] = []
            globals()['y' + num] = []         
            x_min = min(x)
            x_max = max(x)
            i = x_min
            if num == '1' : 
                def fit(x,A1,A2,x0,dx):    
                    return (A1-A2)/(1+np.exp((x-x0)/dx))+A2
                def ftau(x):
                    return ktau*x+btau
                A1 = max(y)
                A2 = min(y)
                dx = (x_max - x_min) / 20
                x0=x_max-5
                sigma = np.ones(len(x))
                sigma[[0,-1]] = 0.01
                pfit, perr = curve_fit(fit,x,y,(A1,A2,x0,dx),sigma,maxfev=10**6)
                globals()['yftau']=[]
                globals()['xftau']=[]
                globals()['yfw']=[]
                globals()['xfw']=[]
                
                if x_max<=pfit[2]:
                    ktau=(fit(x[-1],*pfit)-fit(x[-3],*pfit))/(x[-1]-x[-3])
                    btau=y[-1]-ktau*x[-1]
                    x2tau=x[-2]
                else:
                    ktau=(pfit[1]-pfit[0])/(4*pfit[3])
                    btau=(pfit[0]+pfit[1])/2-ktau*pfit[2]
                    x2tau=pfit[2]
                globals()['tau']=round(-1*btau/ktau, 2)
                globals()['W']=round((fit(x[2],*pfit)-fit(x[1],*pfit))/(x[2]-x[1]), 4)
                while i < x_max:
                    globals()['y' + num].append(fit(i, *pfit))
                    globals()['x' + num].append(i)
                    if  i>=tau and i<=x2tau:
                        globals()['yftau'].append(ftau(i))
                        globals()['xftau'].append(i)
                    i += 0.01
            elif num =='2':
                pf = np.polyfit(np.array(x), np.array(y), 1)
                p= np.poly1d(pf)
                while i < x_max:
                    globals()['y' + num].append(p(i))
                    globals()['x' + num].append(i)
                    i += (x_max-x_min)/100
            elif num=='3':
                pf = np.polyfit(np.array(x), np.array(y), 3)
                p= np.poly1d(pf)    
                while i < x_max:
                    globals()['y' + num].append(p(i))
                    globals()['x' + num].append(i)
                    i += (x_max-x_min)/100

        elif self.findChild(QRadioButton, 'selectRB' + num).isChecked():
            prefix = 'Task ' + str(self.taskTabWidget.currentIndex() + 1) + '\\'
            text = self.findChild(QComboBox, 'inhib1_' + num).currentText()
            if self.taskTabWidget.currentIndex() == 0:
            	if text == '2-Aminothiazole':
            		prefix += 'AT' + '\\' + 'AT' + '_'
            	elif text == '2-Amino-4-methylthiazole':
            		prefix += 'MeAT' + '\\' + 'MeAT' + '_'
            	elif text == '2-Amino-4 (1-naphtyl) thiazole':
            		prefix += 'NfAT' + '\\' + 'NfAT' + '_'
            	elif text == '2-Amino-4-phenylthiazole':
            		prefix += 'PhAT' + '\\' + 'PhAT' + '_'              
            else:
            	if text == '2-Aminothiazole':
            		prefix += 'AT'
            	elif text == '2-Amino-4-methylthiazole':
            		prefix += 'MeAT'
            	elif text == '2-Amino-4 (1-naphtyl) thiazole':
            		prefix += 'NfAT'
            	elif text == '2-Amino-4-phenylthiazole':
            		prefix += 'PhAT'
            if self.findChild(QComboBox, 'temp' + num).currentIndex() == 1:
                self.fopen(prefix + 't70.DAT', '\t')
            elif self.findChild(QComboBox, 'temp' + num).currentIndex() == 2:
                self.fopen(prefix + 't75.DAT', '\t')
            elif self.findChild(QComboBox, 'temp' + num).currentIndex() == 3:
                self.fopen(prefix + 't85.DAT', '\t')
            elif self.findChild(QComboBox, 'temp' + num).currentIndex() == 4:
                self.fopen(prefix + 't90.DAT', '\t')
            elif self.findChild(QComboBox, 'inhib2_' + num).currentIndex() == 1:
                self.fopen(prefix + 'HIn1.DAT', '\t')
            elif self.findChild(QComboBox, 'inhib2_' + num).currentIndex() == 2:
                self.fopen(prefix + 'HIn2.DAT', '\t')
            elif self.findChild(QComboBox, 'inhib2_' + num).currentIndex() == 3:
                self.fopen(prefix + 'HIn3.DAT', '\t')
            elif self.findChild(QComboBox, 'inhib2_' + num).currentIndex() == 4:
                self.fopen(prefix + 'HIn4.DAT', '\t')
            elif self.findChild(QComboBox, 'inhib2_' + num).currentIndex() == 5:
                self.fopen(prefix + 'HIn5.DAT', '\t')
            elif self.findChild(QComboBox, 'inhib2_' + num).currentIndex() == 6:
                self.fopen(prefix + 'HIn6.DAT', '\t')
            elif self.findChild(QComboBox, 'inhib2_' + num).currentIndex() == 7:
                self.fopen(prefix + 'HIn7.DAT', '\t')
            elif self.findChild(QComboBox, 'hdrc' + num).currentIndex() == 1:
                self.fopen(prefix + 'RH1,8.DAT', '\t')
            elif self.findChild(QComboBox, 'hdrc' + num).currentIndex() == 2:
                self.fopen(prefix + 'RH3,6.DAT', '\t')
            elif self.findChild(QComboBox, 'hdrc' + num).currentIndex() == 3:
                self.fopen(prefix + 'RH5,4.DAT', '\t')
            elif self.findChild(QComboBox, 'AIBN' + num).currentIndex() == 1:
                self.fopen(prefix + 'AIBN1.DAT', '\t')
            elif self.findChild(QComboBox, 'AIBN' + num).currentIndex() == 2:
                self.fopen(prefix + 'AIBN3.DAT', '\t')
            elif self.taskTabWidget.currentIndex() in [1, 2]:
                self.fopen(prefix + '.DAT', '\t')

        if ('x' + num in globals()) and ('y' + num in globals()) and (len(globals()['x' + num]) > 0) and (len(globals()['y' + num]) > 0):
            self.findChild(PlotWidget, 'task' + num + 'Graph').plot(globals()['x' + num], globals()['y' + num],
                pen=pg.mkPen(color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), width=1))
            self.findChild(PlotWidget, 'task' + num + 'Graph').plot(globals()['x' + num + '1'], globals()['y' + num + '1'],
                pen=None, symbol='o', symbolSize=4)
            if num=='1':
            	self.findChild(PlotWidget, 'task' + num + 'Graph').plot(globals()['xftau'], globals()['yftau'], pen=pg.mkPen(color='w', width=0.2))
            	self.findChild(QLabel, 'W'+ num).setText(str(globals()['W']))
            	self.findChild(QLabel, 'tau' + num).setText(str(globals()['tau']))            

    def fopen(self, fname, delim = ' '):
        x = []
        y = []
        with open(fname, 'r') as f:
            for line in f.readlines():
                line = line.replace(',', '.')
                s = str.split(line, delim)
                _x, isX = self.floatTryParse(s[0])
                _y, isY = self.floatTryParse(s[1])
                if isX and isY:
                    x.append(_x)
                    y.append(_y)                 
        x_min = min(x)
        x_max = max(x)
        i = x_min
        num = self.sender().objectName()[-1]
        globals()['x' + num] = []
        globals()['y' + num] = []
        globals()['x' + num + '1'] =x
        globals()['y' + num + '1'] = y
        if num == '1' :
            def fit(x,A1,A2,x0,dx):    
                return (A1-A2)/(1+np.exp((x-x0)/dx))+A2
            def ftau(x):
                return ktau*x+btau
            A1 = max(y)
            A2 = min(y)
            dx = (x_max - x_min) / 20
            x0=x_max-5
            sigma = np.ones(len(x))
            sigma[[0,-1]] = 0.01
            pfit, perr = curve_fit(fit,x,y,(A1,A2,x0,dx),sigma,maxfev=10**6)
            globals()['yftau']=[]
            globals()['xftau']=[]
            
            if x_max<=pfit[2]:
                ktau=(fit(x[-1],*pfit)-fit(x[-3],*pfit))/(x[-1]-x[-3])
                btau=y[-1]-ktau*x[-1]
                x2tau=x[-2]
            else:
                ktau=(pfit[1]-pfit[0])/(4*pfit[3])
                btau=(pfit[0]+pfit[1])/2-ktau*pfit[2]
                x2tau=pfit[2]
            globals()['tau']=round(-1*btau/ktau, 2)
            globals()['W']=round((fit(x[2],*pfit)-fit(x[1],*pfit))/(x[2]-x[1]), 4)
            while i < x_max:
                globals()['y' + num].append(fit(i, *pfit))
                globals()['x' + num].append(i)
                if  i>=tau :
                    globals()['yftau'].append(ftau(i))
                    globals()['xftau'].append(i)
                i += 0.01
                
        elif num == '2':
            pf = np.polyfit(np.array(x), np.array(y), 1)
            p = np.poly1d(pf)
            while i < x_max:
                globals()['y' + num].append(p(i))
                globals()['x' + num].append(i)
                i += (x_max-x_min)/100 

        elif  num=='3':
            pf = np.polyfit(np.array(x), np.array(y), 3)
            p = np.poly1d(pf)   
            while i < x_max:
                globals()['y' + num].append(p(i))
                globals()['x' + num].append(i)
                i += (x_max-x_min)/100      

    @pyqtSlot()
    def on_startButton2_clicked(self):
        self.on_startButton1_clicked()

    @pyqtSlot()
    def on_startButton3_clicked(self):
        self.on_startButton1_clicked()
    
    @pyqtSlot()
    def on_openButton1_clicked(self):
        try:
            num = self.sender().objectName()[-1]
            fname = QFileDialog.getOpenFileName(self, 'Open file', 'Task ' + num, 'DAT files (*.DAT, *.dat);;Text files(*.txt)')[0]
            if fname:
                if (fname[-2] == 'A') or (fname[-2] == 'a'):
                    self.fopen(fname, '\t')
                else:
                    self.fopen(fname)
                self.findChild(QPushButton, 'openButton' + num).setText('File uploaded')
        except Exception:
            QMessageBox.critical(self, 'Error', 'Invalid input')
            
    @pyqtSlot()
    def on_openButton2_clicked(self):
        self.on_openButton1_clicked()

    @pyqtSlot()
    def on_openButton3_clicked(self):
        self.on_openButton1_clicked()

    @pyqtSlot()
    def on_clearButton1_clicked(self):
        num = self.sender().objectName()[-1]
        self.findChild(PlotWidget, 'task' + num + 'Graph').clear()
        self.findChild(QLabel, 'W'+ num).clear()
        self.findChild(QLabel, 'tau'+ num).clear()

    @pyqtSlot()
    def on_clearButton2_clicked(self):
        num = self.sender().objectName()[-1]
        self.findChild(PlotWidget, 'task' + num + 'Graph').clear()

    @pyqtSlot()
    def on_clearButton3_clicked(self):
        num = self.sender().objectName()[-1]
        self.findChild(PlotWidget, 'task' + num + 'Graph').clear()

    @pyqtSlot(int)
    def on_temp1_currentIndexChanged(self, index):
        if self.temp1.currentIndex() > 0:
            self.inhib2_1.setCurrentIndex(0)
            self.hdrc1.setCurrentIndex(0)
            self.AIBN1.setCurrentIndex(0)

    @pyqtSlot(int)
    def on_inhib2_1_currentIndexChanged(self, index):
        if self.inhib2_1.currentIndex() > 0:
            self.temp1.setCurrentIndex(0)
            self.hdrc1.setCurrentIndex(0)
            self.AIBN1.setCurrentIndex(0)

    @pyqtSlot(int)
    def on_hdrc1_currentIndexChanged(self, index):
        if self.hdrc1.currentIndex() > 0:
            self.temp1.setCurrentIndex(0)
            self.inhib2_1.setCurrentIndex(0)
            self.AIBN1.setCurrentIndex(0)

    @pyqtSlot(int)
    def on_AIBN1_currentIndexChanged(self, index):
        if self.AIBN1.currentIndex() > 0:
            self.temp1.setCurrentIndex(0)
            self.inhib2_1.setCurrentIndex(0)
            self.hdrc1.setCurrentIndex(0)

    @pyqtSlot(int)
    def on_temp2_currentIndexChanged(self, index):
        self.temp2.setCurrentIndex(0)
        self.inhib2_2.setCurrentIndex(0)
        self.hdrc2.setCurrentIndex(0)
        self.AIBN2.setCurrentIndex(0)

    @pyqtSlot(int)
    def on_inhib2_2_currentIndexChanged(self, index):
        self.on_temp2_currentIndexChanged(0)
        
    @pyqtSlot(int)
    def on_hdrc2_currentIndexChanged(self, index):
        self.on_temp2_currentIndexChanged(0)

    @pyqtSlot(int)
    def on_AIBN2_currentIndexChanged(self, index):
        self.on_temp2_currentIndexChanged(0)

    @pyqtSlot(int)
    def on_temp3_currentIndexChanged(self, index):
        self.temp3.setCurrentIndex(0)
        self.inhib2_3.setCurrentIndex(0)
        self.hdrc3.setCurrentIndex(0)
        self.AIBN3.setCurrentIndex(0)

    @pyqtSlot(int)
    def on_inhib3_2_currentIndexChanged(self, index):
        self.on_temp3_currentIndexChanged(0)
        
    @pyqtSlot(int)
    def on_hdrc3_currentIndexChanged(self, index):
        self.on_temp3_currentIndexChanged(0)

    @pyqtSlot(int)
    def on_AIBN3_currentIndexChanged(self, index):
        self.on_temp3_currentIndexChanged(0)

    @pyqtSlot()
    def on_speedButton4_clicked(self):
        try:
            num = self.sender().objectName()[-1]
            ind = int(num) - 4
            Oop = QFileDialog.getOpenFileName(self, 'Open Oop file', 'Task ' + num, 'DAT files(*.DAT)')[0]
            if Oop:
                self.Oop[ind] = Oop
                if self.Oop[ind] and self.Sr[ind]:
                    if ind == 0:
                        R, W, Wok, tau, fi, Ft, f, n, nf, fk7, k2k6, k2k7, k7, Sa_f, Sa_n, Sa_nf,Sa_k2k6, Sa_k2k7, Sa_k7, Sa_fk7 = HIn(self.Oop[ind], self.Sr[ind])
                    elif ind == 1:
                        R, W, Wok, tau, fi, Ft, f, n, nf, fk7, k2k6, k2k7, k7, Sa_f, Sa_n, Sa_nf,Sa_k2k6, Sa_k2k7, Sa_k7, Sa_fk7 = AIBN(self.Oop[ind], self.Sr[ind])
                    else:
                        R, W, Wok, tau, fi, Ft, f, n, nf, fk7, k2k6, k2k7, k7, Sa_f, Sa_n, Sa_nf,Sa_k2k6, Sa_k2k7, Sa_k7, Sa_fk7 = RH(self.Oop[ind], self.Sr[ind])   
                    self.findChild(QLabel, 'fValue' + num).setText(str(round(f,4)))
                    self.findChild(QLabel, 'nValue' + num).setText(str(round(n,4)))
                    self.findChild(QLabel, 'nfValue' + num).setText(str(round(nf,4)))
                    self.findChild(QLabel, 'fk7Value' + num).setText(str(round(fk7/10000,4))+'\u00B710\u2074')
                    self.findChild(QLabel, 'k2k6Value' + num).setText(str(round(k2k6*10000,4))+'\u00B710\u207B\u2074')
                    self.findChild(QLabel, 'k2k7Value' + num).setText(str(round(k2k7*10000,4))+'\u00B710\u207B\u2074')
                    self.findChild(QLabel, 'k7Value' + num).setText(str(round(k7/10000,4))+'\u00B710\u2074')
                    self.findChild(QLabel, 'Sa_fValue' + num).setText(str(round(Sa_f,4)))
                    self.findChild(QLabel, 'Sa_nValue' + num).setText(str(round(Sa_n,4)))
                    self.findChild(QLabel, 'Sa_nfValue' + num).setText(str(round(Sa_nf,4)))
                    self.findChild(QLabel, 'Sa_k2k6Value' + num).setText(str(round(Sa_k2k6*10000,4))+'\u00B710\u207B\u2074')
                    self.findChild(QLabel, 'Sa_k2k7Value' + num).setText(str(round(Sa_k2k7*10000,4))+'\u00B710\u207B\u2074')
                    self.findChild(QLabel, 'Sa_k7Value' + num).setText(str(round(Sa_k7/10000,4))+'\u00B710\u2074')
                    self.findChild(QLabel, 'Sa_fk7Value' + num).setText(str(round(Sa_fk7/10000,4))+'\u00B710\u2074')
                    self.findChild(QTableWidget, 'dataTable' + num).setRowCount(len(W))
                    for i in range(len(W)):
                        self.findChild(QTableWidget, 'dataTable' + num).setItem(i, 0, QTableWidgetItem(str(R[i])))
                        self.findChild(QTableWidget, 'dataTable' + num).setItem(i, 1, QTableWidgetItem(str(round(W[i]*100000,4))+'\u00B710\u207B\u2075'))
                        self.findChild(QTableWidget, 'dataTable' + num).setItem(i, 2, QTableWidgetItem(str(round(Wok[i]*100000,4))+'\u00B710\u207B\u2075'))
                        self.findChild(QTableWidget, 'dataTable' + num).setItem(i, 3, QTableWidgetItem(str(tau[i])))
                        if ind==1:
                            self.findChild(QTableWidget, 'dataTable' + num).setItem(i, 4, QTableWidgetItem(str(round(fi[i]*100000,4))+'\u00B710\u207B\u2075'))
                        else:
                            self.findChild(QTableWidget, 'dataTable' + num).setItem(i, 4, QTableWidgetItem(str(round(fi[i],4))))
                        self.findChild(QTableWidget, 'dataTable' + num).setItem(i, 4, QTableWidgetItem(str(round(fi[i],4))))
                        self.findChild(QTableWidget, 'dataTable' + num).setItem(i, 5, QTableWidgetItem(str(round(Ft[i],4))))
                        
        except Exception:
            QMessageBox.critical(self, 'Error', 'Invalid input'+str(k2k6))

    @pyqtSlot()
    def on_speedButton5_clicked(self):
        self.on_speedButton4_clicked()

    @pyqtSlot()
    def on_speedButton6_clicked(self):
        self.on_speedButton4_clicked()

    @pyqtSlot()
    def on_paramsButton4_clicked(self):
        try:
            num = self.sender().objectName()[-1]
            ind = int(num) - 4
            Sr = QFileDialog.getOpenFileName(self, 'Open Sr file', 'Task ' + num, 'DAT files(*.DAT)')[0]
            if Sr:
                self.Sr[ind] = Sr
                if self.Oop[ind] and self.Sr[ind]:
                    if ind == 0:
                        R, W, Wok, tau, fi, Ft, f, n, nf, fk7, k2k6, k2k7, k7, Sa_f, Sa_n, Sa_nf,Sa_k2k6, Sa_k2k7, Sa_k7, Sa_fk7 = HIn(self.Oop[ind], self.Sr[ind])
                    elif ind == 1:
                        R, W, Wok, tau, fi, Ft, f, n, nf, fk7, k2k6, k2k7, k7, Sa_f, Sa_n, Sa_nf,Sa_k2k6, Sa_k2k7, Sa_k7, Sa_fk7 = AIBN(self.Oop[ind], self.Sr[ind])
                    else:
                        R, W, Wok, tau, fi, Ft, f, n, nf, fk7, k2k6, k2k7, k7, Sa_f, Sa_n, Sa_nf,Sa_k2k6, Sa_k2k7, Sa_k7, Sa_fk7 = RH(self.Oop[ind], self.Sr[ind])    
                    self.findChild(QLabel, 'fValue' + num).setText(str(round(f,4)))
                    self.findChild(QLabel, 'nValue' + num).setText(str(round(n,4)))
                    self.findChild(QLabel, 'nfValue' + num).setText(str(round(nf,4)))
                    self.findChild(QLabel, 'fk7Value' + num).setText(str(round(fk7/10000,4))+'\u00B710\u2074')
                    self.findChild(QLabel, 'k2k6Value' + num).setText(str(round(k2k6*10000,4))+'\u00B710\u207B\u2074')
                    self.findChild(QLabel, 'k2k7Value' + num).setText(str(round(k2k7*10000,4))+'\u00B710\u207B\u2074')
                    self.findChild(QLabel, 'k7Value' + num).setText(str(round(k7/10000,4))+'\u00B710\u2074')
                    self.findChild(QLabel, 'Sa_fValue' + num).setText(str(round(Sa_f,4)))
                    self.findChild(QLabel, 'Sa_nValue' + num).setText(str(round(Sa_n,4)))
                    self.findChild(QLabel, 'Sa_nfValue' + num).setText(str(round(Sa_nf,4)))
                    self.findChild(QLabel, 'Sa_k2k6Value' + num).setText(str(round(Sa_k2k6*10000,4))+'\u00B710\u207B\u2074')
                    self.findChild(QLabel, 'Sa_k2k7Value' + num).setText(str(round(Sa_k2k7*10000,4))+'\u00B710\u207B\u2074')
                    self.findChild(QLabel, 'Sa_k7Value' + num).setText(str(round(Sa_k7/10000,4))+'\u00B710\u2074')
                    self.findChild(QLabel, 'Sa_fk7Value' + num).setText(str(round(Sa_fk7/10000,4))+'\u00B710\u2074')
                    self.findChild(QTableWidget, 'dataTable' + num).setRowCount(len(W))
                    for i in range(len(W)):
                        self.findChild(QTableWidget, 'dataTable' + num).setItem(i, 0, QTableWidgetItem(str(R[i])))
                        self.findChild(QTableWidget, 'dataTable' + num).setItem(i, 1, QTableWidgetItem(str(round(W[i]*100000,4))+'\u00B710\u207B\u2075'))
                        self.findChild(QTableWidget, 'dataTable' + num).setItem(i, 2, QTableWidgetItem(str(round(Wok[i]*100000,4))+'\u00B710\u207B\u2075'))
                        self.findChild(QTableWidget, 'dataTable' + num).setItem(i, 3, QTableWidgetItem(str(tau[i])))
                        if ind==1:
                            self.findChild(QTableWidget, 'dataTable' + num).setItem(i, 4, QTableWidgetItem(str(round(fi[i]*100000,4))+'\u00B710\u207B\u2075'))
                        else:
                            self.findChild(QTableWidget, 'dataTable' + num).setItem(i, 4, QTableWidgetItem(str(round(fi[i],4))))
                        self.findChild(QTableWidget, 'dataTable' + num).setItem(i, 5, QTableWidgetItem(str(round(Ft[i],4))))
             	    
        except Exception:
            QMessageBox.critical(self, 'Error', 'Invalid input')
    
    @pyqtSlot()
    def on_paramsButton5_clicked(self):
        self.on_paramsButton4_clicked()

    @pyqtSlot()
    def on_paramsButton6_clicked(self):
        self.on_paramsButton4_clicked()
