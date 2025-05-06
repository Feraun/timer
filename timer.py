from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtMultimedia import QSound
from win32api import GetSystemMetrics
import time
import sys

class Window(QWidget):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self, parent)


        self.setWindowTitle("Таймер")
        self.setGeometry(0, 0, GetSystemMetrics(0), GetSystemMetrics(1))
        self.setMinimumSize(1200, 500)

        #кнопка старта
        self.btn_start = QtWidgets.QPushButton(self)
        self.btn_start.setText("Старт")
        self.btn_start.move(50, 50)
        self.btn_start.clicked.connect(self.start_timer)

        #кнопка сброса
        self.btn_reset = QtWidgets.QPushButton(self)
        self.btn_reset.setText("Сброс")
        self.btn_reset.move(50, 300)
        self.btn_reset.clicked.connect(self.reset)

        #место ввода
        self.input_text = QtWidgets.QTextEdit(self)
        self.input_text.setText("15")
        self.input_text.setFont(QFont("Arial", 18))
        self.input_text.move(40, 100)
        self.input_text.setMaximumSize(100, 40)
        self.input_text.setAlignment(Qt.AlignCenter)
        self.input_text.toPlainText()

        #место вывода времени
        self.timer1 = QtWidgets.QLabel(self)
        self.timer1.setAlignment(Qt.AlignCenter)
        self.timer1.setText("00:00")
        self.timer1.move(100, 40)
        

        #галочка звука
        self.audio = QtWidgets.QCheckBox(self)
        self.audio.setText("Включить звук")
        self.audio.move(40, 175)

        self.blink = False

        #таймер, благодаря которому все работает
        self.timer = QTimer(self)                            
        self.timer.timeout.connect(self.showTime)                   
        self.timer.setInterval(1000)
        self.time = 0

    #функция масштабируемости
    def resizeEvent(self, e):
        w = e.size().width()
        h = e.size().height()
        
        #размер окна вывода времени
        c = int(GetSystemMetrics(1) - 50)
        self.timer1.resize(w-350, h-200)
        
        #положение окна вывода времени
        self.timer1.move(int(w/10), int(h/11))
        
        #размер шрифта цифр
        p = int(w / 5)
        self.timer1.setFont(QFont("Arial", p))
        
        QtWidgets.QWidget.resizeEvent(self, e)


    #функция кнопки старта
    def start_timer(self):
        text1 = str(self.input_text.toPlainText())

        #перехват ошибки, дабы неправильный ввод(буквы, запятая, пробелы) обнулялся
        try:
            text2 = float(text1)
        except ValueError:
            text2 = 0
            self.input_text.setText("0")
            self.btn_start.setText("Старт")
            self.input_text.setAlignment(Qt.AlignCenter)
            
            
        text3 = float(text2)
        text = text3 * 60

        if self.btn_start.text() == "Старт":
            if not self.time: self.time = text
            self.timer.start()
            self.btn_start.setText("Стоп")
        else:
            self.timer.stop()
            self.btn_start.setText("Старт")


    #ГЛАВНАЯ ФУНКЦИЯ, благодаря ей таймер и работает
    def showTime(self):

            if self.time > 0:
                self.time -= 1
                text1 = self.time

                #превращение в MM:SS
                ty_res = time.gmtime(text1)
                res = time.strftime("%M:%S", ty_res)
                self.timer1.setText(res)

                #делает цифры красными
                if self.time < 61:
                    self.timer1.setStyleSheet("color: #FF0000")
                
                #заставляет цифры мигать
                if self.time < 30:
                    if self.blink == False:
                        self.timer1.hide()
                        self.blink = True
                    else:
                        self.timer1.show()
                        self.blink = False


                if self.time == 0:
                    self.timer1.setText("00:00")
                    self.btn_start.setText("Старт")
                    if self.audio.checkState():
                        QSound.play('C:\\....\\pisc.wav') #писк при нуле


    #функция кнопки сброса
    def reset(self):
        self.timer.stop()       
        self.btn_start.setText("Старт")
        self.timer1.setText(str("00:00"))
        self.timer1.setStyleSheet("color: #000000")

    


if __name__ == "__main__":
    app = QApplication(sys.argv) 
    app.setWindowIcon(QtGui.QIcon('C:\\....\\icon.ico'))
    
    window = Window()
    window.setWindowIcon(QtGui.QIcon('C:\\....\\icon.ico'))
    
    window.show()
    sys.exit(app.exec())
