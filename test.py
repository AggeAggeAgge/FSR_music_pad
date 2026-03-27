import sys
import os
import random
import serial
import time
import pygame
from PySide6 import QtCore, QtWidgets, QtGui

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

try:
    arduino = serial.Serial("COM3", 115200, timeout=0.1)
    time.sleep(2)
except Exception as e:
    print(f"Kunde inte ansluta till Arduino på COM3: {e}")
    arduino = None

class VisualizerWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(150) 
        self.values = [0] * 20 

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
            start_p = QtCore.QPointF(0, height)
            end_p = QtCore.QPointF(0, 0)
            grad = QtGui.QLinearGradient(start_p, end_p)
            
            grad.setColorAt(0.0, QtGui.QColor("#8E2DE2"))
            grad.setColorAt(1.0, QtGui.QColor("#4568DC")) 
            
            painter.setBrush(grad)
            painter.setPen(QtCore.Qt.NoPen)
            
            bar_height = (val / 100) * (height - 10)
            
            painter.drawRoundedRect(
                int(i * bar_width + 4), 
                int(height - bar_height), 
                int(bar_width - 8), 
                int(bar_height), 
                6, 6
            )

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Arduino Drum Pad & Visualizer")
        self.text = QtWidgets.QLabel("Väntar på slag...", alignment=QtCore.Qt.AlignCenter)
        self.text.setStyleSheet("font-size: 18px; font-weight: bold; color: #555;")

        self.visualizer = VisualizerWidget()
        self.current_levels = [0] * 20

        self.button = QtWidgets.QPushButton("Testa Ljud 1 (Pad 1)")
        self.button2 = QtWidgets.QPushButton("Testa Ljud 2 (Pad 2)")

        # Leta efter ljudfiler
        if not os.path.exists("sounds"):
            os.makedirs("sounds")
            print("Skapade mappen 'sounds'. Lägg till dina filer där!")

        self.sound_list = [f for f in os.listdir("sounds") if f.endswith((".wav", ".mp3", ".ogg"))]

        self.dropdown1 = QtWidgets.QComboBox()
        self.dropdown1.addItems(self.sound_list)
        self.dropdown2 = QtWidgets.QComboBox()
        self.dropdown2.addItems(self.sound_list)

        # --- Layout ---
        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(15)
        layout.addWidget(self.text)
        layout.addWidget(self.visualizer)
        
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(self.button)
        btn_layout.addWidget(self.button2)
        layout.addLayout(btn_layout)

        layout.addWidget(QtWidgets.QLabel("Välj ljud för Pad 1:"))
        layout.addWidget(self.dropdown1)
        layout.addWidget(QtWidgets.QLabel("Välj ljud för Pad 2:"))
        layout.addWidget(self.dropdown2)

        # --- Signaler ---
        self.button.clicked.connect(self.play_sound)
        self.button2.clicked.connect(self.play_sound2)
        self.dropdown1.currentTextChanged.connect(self.update_sounds)
        self.dropdown2.currentTextChanged.connect(self.update_sounds)

        # --- Timers ---
        # Läser från Arduino var 5:e millisekund
        self.serial_timer = QtCore.QTimer()
        self.serial_timer.timeout.connect(self.read_serial)
        self.serial_timer.start(5)

        self.vis_timer = QtCore.QTimer()
        self.vis_timer.timeout.connect(self.animate_visualizer)
        self.vis_timer.start(20)

        self.update_sounds()

    def update_sounds(self):

        if self.dropdown1.currentText():
            self.sound1 = pygame.mixer.Sound(os.path.join("sounds", self.dropdown1.currentText()))
        if self.dropdown2.currentText():
            self.sound2 = pygame.mixer.Sound(os.path.join("sounds", self.dropdown2.currentText()))


    def animate_visualizer(self):
        self.current_levels = [max(0, x - 4) for x in self.current_levels]
        self.visualizer.update_values(self.current_levels)

    def trigger_visualizer_hit(self):
        self.current_levels = [random.randint(50, 100) for _ in range(20)]

    def play_sound(self):
        if hasattr(self, "sound1"):
            self.sound1.play()
            self.trigger_visualizer_hit()

    def play_sound2(self):
        if hasattr(self, "sound2"):
            self.sound2.play()
            self.trigger_visualizer_hit()

    def read_serial(self):
        if arduino and arduino.in_waiting:
            try:
                data = arduino.readline().decode(errors="ignore").strip()
                if data.startswith("1"):
                    self.play_sound()
                elif data.startswith("2"):
                    self.play_sound2()
            except:
                pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    # Snygga till temat lite
    app.setStyle("Fusion")
    
    window = MyWidget()
    window.resize(450, 500)
    window.show()
    
    sys.exit(app.exec())