import sqlite3
import PyQt5,sys
from PyQt5 import QtGui,QtWidgets,uic,QtSql,QtSql,QtCore,Qt
from PyQt5.QtWidgets import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def veritabaniSorgu(cümlecik,tip):
    vt=sqlite3.connect("FirstDataBase.db")
    im=vt.cursor()
    im.execute(cümlecik)
    if tip==1:
        veriler=im.fetchall()
        return veriler
    vt.commit()

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('FirstGui.ui', self) # Load the .ui file
        self.veriTabloyaYaz()
        self.kullaniciBilgYaz()
        self.buttonProgramDurumDegistir.clicked.connect(self.programDurumDegistir)
        #self.buttonDersEkle.clicked.connect(self.dersEkle)
        self.buttonBilgiGuncelle.clicked.connect(self.bilgiGuncelle)
        self.show()

    def veriTabloyaYaz(self):
        vtVeriler = veritabaniSorgu("""Select * from dersler""", 1)
        for i in vtVeriler:
            button = QPushButton('Dersi Sil')
            button.setIcon(QtGui.QIcon('logo\sil.jpg'))
            rowPosition = self.tableDerslerWidget.rowCount()
            self.tableDerslerWidget.setRowCount(rowPosition+1)
            button.clicked.connect(lambda ch,j=int(rowPosition): self.DersSil(j,vtVeriler))
            self.tableDerslerWidget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(str(i[0])))
            self.tableDerslerWidget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(str(i[1])))
            self.tableDerslerWidget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(str(i[2])))
            self.tableDerslerWidget.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(str(i[3])))
            self.tableDerslerWidget.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(str(i[4])))
            self.tableDerslerWidget.setCellWidget(rowPosition,5,button)
    def kullaniciBilgYaz(self):
        vtVeriler=veritabaniSorgu("""Select * from kullanici""", 1)
        self.textAlKullaniciAd.setText(vtVeriler[0][0])
        self.textAlKullaniciSifre.setText(vtVeriler[0][1])
    def DersSil(self,j,i):
        vt = sqlite3.connect("FirstDataBase.db")
        im = vt.cursor()
        sql_delete_query = "DELETE FROM dersler WHERE dersAdi=?"
        data = str(i[j][0])
        print(data)
        im.execute(sql_delete_query, data)
        vt.commit()
        self.tabloBosalt()
        self.veriTabloyaYaz()
    #def dersEkle(self):
    def tabloBosalt(self):
        self.tableDerslerWidget.setRowCount(0)
    def bilgiGuncelle(self):
        vt = sqlite3.connect("FirstDataBase.db")
        im = vt.cursor()
        sql_update_query = """Update kullanici set kullaniciAdi = ?,sifre = ?"""
        data=(self.textAlKullaniciAd.toPlainText(),self.textAlKullaniciSifre.toPlainText())
        im.execute(sql_update_query,data)
        vt.commit()
    def programDurumDegistir(self):
        if self.labelDurumYaz.text()=='':
            self.labelDurumYaz.setStyleSheet("background-color: green;")
            self.labelDurumYaz.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
            self.labelDurumYaz.setText("Çalışıyor..")
            self.seleniumKismi()
            self.buttonProgramDurumDegistir.setText("Programı Sonlandır")
        else:
            self.labelDurumYaz.setStyleSheet("background-color: rgb(255,0,0);")
            self.labelDurumYaz.setText("")
            self.buttonProgramDurumDegistir.setText("Programı Çalıştır")

    def seleniumKismi(self):
        driver = webdriver.Chrome('./operadriver.exe')
        driver.get("https://www.python.org")
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()







