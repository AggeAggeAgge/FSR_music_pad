import sys
import os
from PySide6 import QtCore, QtWidgets, QtGui
import serial
import time
import pygame
import random


arduino = serial.Serial("COM3", 115200)
time.sleep(2)




pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

class VisualizerWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(120)
        self.values = [0] * 20
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyleSheet("background-color: #1a1a1a; border-radius: 10px;")

    def update_values(self, new_values):
        self.values = new_values
        self.update()
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        width = self.width()
        height = self.height()
        bar_width = width / len(self.values)

        for i, val in enumerate(self.values):
            grad = QtGui.QLinearGradient(QtCore.QPointF(0, height), QtCore.QPointF(0, 0))
            
            grad.setColorAt(0.0, QtGui.QColor("#6a11cb"))
            grad.setColorAt(1.0, QtGui.QColor("#2575fc"))
            
            painter.setBrush(grad)
            painter.setPen(QtCore.Qt.NoPen)
            
            bar_height = (val / 100) * (height - 10)
            
            painter.drawRoundedRect(
                int(i * bar_width + 2), 
                int(height - bar_height), 
                int(bar_width - 4), 
                int(bar_height), 
                5, 5
            )





class MyWidget(QtWidgets.QWidget):


    def __init__(self):
        super().__init__() #u

        self.button = QtWidgets.QPushButton("Sound 1")
        self.button2 = QtWidgets.QPushButton("Sound 2")

        self.text = QtWidgets.QLabel("Press button or hit pad", alignment=QtCore.Qt.AlignCenter)
        
        self.visualizer = VisualizerWidget()
        self.current_levels = [0] * 20

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

        layout.addWidget(self.visualizer)

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

        self.vis_timer = QtCore.QTimer()
        self.vis_timer.timeout.connect(self.animate_visualizer)
        self.vis_timer.start(20)

    def update_sounds(self):
        if self.sound_list:
            self.sound1 = pygame.mixer.Sound(os.path.join("sounds", self.dropdown1.currentText()))
            self.sound2 = pygame.mixer.Sound(os.path.join("sounds", self.dropdown2.currentText()))

    def trigger_visualizer_hit(self):
        for i in range(len(self.current_levels)):
            self.current_levels[i] = random.randint(60, 100)

    def animate_visualizer(self):
        self.current_levels = [max(0, x -4) for x in self.current_levels]
        self.visualizer.update_values(self.current_levels)



    def play_sound(self):
        if hasattr(self, "sound1"):
            self.sound1.play()
            self.trigger_visualizer_hit()

    def play_sound2(self):
        if hasattr(self, "sound2"):
            self.sound2.play()
            self.trigger_visualizer_hit()

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

    app.setStyle("Fusion")

    widget = MyWidget()
    widget.setWindowTitle("Drum Pad Interface")
    widget.resize(400, 300)
    widget.show()

    sys.exit(app.exec())