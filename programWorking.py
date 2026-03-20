import sys
import os
from PySide6 import QtCore, QtWidgets
import serial
import time
import pygame


arduino = serial.Serial("COM3", 115200)
time.sleep(2)


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()


class MyWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__() #u

        self.button = QtWidgets.QPushButton("Sound 1")
        self.button2 = QtWidgets.QPushButton("Sound 2")

        self.text = QtWidgets.QLabel("Press button or hit pad", alignment=QtCore.Qt.AlignCenter)
        
        self.sound_list = [f for f in os.listdir("sounds") if f.endswith((".wav", ".mp3", ".ogg"))]

        self.dropdown1 = QtWidgets.QComboBox()
        self.dropdown1.addItems(self.sound_list)

        self.dropdown2 = QtWidgets.QComboBox()
        self.dropdown2.addItems(self.sound_list)

        self.update_sounds() #u

        self.dropdown1.currentTextChanged.connect(self.update_sounds)
        self.dropdown2.currentTextChanged.connect(self.update_sounds)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.text)
        layout.addWidget(self.button)
        layout.addWidget(self.button2)

        layout.addWidget(QtWidgets.QLabel("Pad 1 Sound:"))
        layout.addWidget(self.dropdown1)

        layout.addWidget(QtWidgets.QLabel("Pad 2 Sound:"))
        layout.addWidget(self.dropdown2)

        self.button.clicked.connect(self.play_sound)
        self.button2.clicked.connect(self.play_sound2)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.read_serial)
        self.timer.start(5)

    def update_sounds(self):
        if self.sound_list:
            self.sound1 = pygame.mixer.Sound(os.path.join("sounds", self.dropdown1.currentText()))
            self.sound2 = pygame.mixer.Sound(os.path.join("sounds", self.dropdown2.currentText()))

    def play_sound(self):
        if hasattr(self, "sound1"):
            self.sound1.play()

    def play_sound2(self):
        if hasattr(self, "sound2"):
            self.sound2.play()

    def read_serial(self):
        if arduino.in_waiting:
            data = arduino.readline().decode(errors="ignore").strip()

            if data.startswith("1"):
                print(data)
                if hasattr(self, "sound1"):
                    self.sound1.play()    
            
            if data.startswith("2"):
                print(data)
                if hasattr(self, "sound2"):
                    self.sound2.play()



if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(400, 300)
    widget.show()

    sys.exit(app.exec())