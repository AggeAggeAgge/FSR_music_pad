import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from playsound3 import playsound
import serial
import time


arduino = serial.Serial(port='COM3', baudrate=115200) 

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()


        self.button = QtWidgets.QPushButton("Sound 1")

        self.text = QtWidgets.QLabel("Press button to play sound", alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.play_sound)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.read_serial)
        self.timer.start(10)  # every 50 ms

    @QtCore.Slot()
    def play_sound(self):
        playsound("sounds/hello-there.mp3")

    def read_serial(self):
        if arduino.in_waiting:
            data = arduino.readline().decode().strip()
            print(data)



if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()
        
    sys.exit(app.exec())