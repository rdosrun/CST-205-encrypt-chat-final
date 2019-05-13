from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QApplication, QPushButton,QVBoxLayout,QMainWindow, QLineEdit, QHBoxLayout
import sys
from PyQt5.QtCore import pyqtSlot, QUrl, Qt
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtGui import QIcon
import sys,time
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QScrollBar,QSplitter,QTableWidgetItem,QTableWidget,QComboBox,QVBoxLayout,QGridLayout,QDialog,QWidget, QPushButton, QApplication, QMainWindow,QAction,QMessageBox,QLabel,QTextEdit,QProgressBar,QLineEdit
from PyQt5.QtCore import QCoreApplication
import socket
from threading import Thread 
from socketserver import ThreadingMixIn 
import test_client_chat
import encrypt_header
import json 
from _thread import *
import threading 



#This class creates the gui for selecting names 
class Start(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.lbl1 = QLabel("Your name for today?")
        #creates a buttons 
        self.btn = QPushButton("Connect to person", self)
        self.btn2 = QPushButton("This name", self)
        self.textbox = QLineEdit(self)
        self.textbox2 = QLineEdit(self)
        
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        vbox.addWidget(self.textbox)
        vbox.addWidget(self.btn)
        vbox.addWidget(self.lbl1)
        vbox.addWidget(self.textbox2)
        vbox.addWidget(self.btn2)
        
        vbox.addWidget(self.lbl1)
        self.setLayout(vbox)
        self.btn.clicked.connect(self.on_click)
        self.btn2.clicked.connect(self.on_click_2)

        self.setWindowTitle('Encrpted Chat')
        self.show()
 
    @pyqtSlot()
    def on_click(self):
        #creates new chat window and get other users info from server
        #begins listening 
        tmp_key = test_client_chat.con_2_person(self.textbox.text())
        print("tmp_key:",tmp_key)
        self.displaySecond = Window(self.textbox.text(),tmp_key)
        self.displaySecond.show()

    def on_click_2(self):
        self.lbl1.setText(self.textbox2.text())
    
class Window(QDialog):
    #creates chat box
    def __init__(self, name,tmp_key):
        super().__init__()
        self.name = name
        self.flag=0
        self.key = tmp_key
        self.chatTextField=QLineEdit(self)
        self.chatTextField.resize(480,100)
        self.chatTextField.move(10,350)
        self.btnSend=QPushButton("Send",self) 
        #creates send button
        self.btnSend.resize(480,30)
        self.btnSendFont=self.btnSend.font()
        self.btnSendFont.setPointSize(15)
        self.btnSend.setFont(self.btnSendFont)
        self.btnSend.move(10,460)
        self.btnSend.setStyleSheet("background-color: #606060")
        self.btnSend.clicked.connect(self.send)
        self.chatBody=QVBoxLayout(self)
        # self.chatBody.addWidget(self.chatTextField)
        # self.chatBody.addWidget(self.btnSend)
        # self.chatWidget.setLayout(self.chatBody)
        splitter=QSplitter(QtCore.Qt.Vertical)
 
        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
 
        splitter.addWidget(self.chat)
        splitter.addWidget(self.chatTextField)
        splitter.setSizes([400,100])
 
        splitter2=QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter)
        splitter2.addWidget(self.btnSend)
        splitter2.setSizes([200,10])
 
        self.chatBody.addWidget(splitter2)
        self.setWindowTitle(name)
        self.resize(500, 500)
        #starts listening for responces from server
        self.listen_thread = threading.Thread(target = test_client_chat.listen, args = (self,tmp_key,7),daemon=True)
        self.listen_thread.start()
        print("line 102")

    def update(self,message):
        #updates screen messages
        text="<"+self.name+"> "+message
        font=self.chat.font()
        font.setPointSize(13)
        self.chat.setFont(font)
        textFormatted='{:>80}'.format(text)
        self.chat.append(textFormatted)
        self.chatTextField.setText("")
       

    def send(self):        
        text=self.chatTextField.text()
        test_client_chat.send_message(text,self.name,self.key)
        font=self.chat.font()
        font.setPointSize(13)
        self.chat.setFont(font)
        textFormatted='{:>80}'.format(text)
        self.chat.append(textFormatted)
        #global conn
        #conn.send(text.encode("utf-8"))
        self.chatTextField.setText("")
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Start() 
    sys.exit(app.exec_())