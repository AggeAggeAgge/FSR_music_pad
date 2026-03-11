import sys
from PySide6 import QtCore, QtWidgets
import serial
import time
import pygame

arduino = serial.Serial('COM3', 115200)
time.sleep(2) 

pygame.mixer.init()
sound = pygame.mixer.Sound("sounds/whatsapp.mp3")


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.button = QtWidgets.QPushButton("Sound 1")
        self.text = QtWidgets.QLabel("Press button or hit pad", alignment=QtCore.Qt.AlignCenter)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.text)
        layout.addWidget(self.button)

        self.button.clicked.connect(self.play_sound)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.read_serial)
        self.timer.start(5) 
        
    def play_sound(self):
        sound.play()

    def read_serial(self):
        if arduino.in_waiting:
            data = arduino.readline().decode(errors="ignore").strip()

            if data.startswith("HIT"):
                print(data)
                sound.play()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())