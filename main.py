import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QWidget
)
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtCore import Qt, QTimer
from gerber_parser import parse_gerber
from arduino_comm import send_to_arduino

class GerberViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.paths = []
        self.current_step = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_step)

    def load_paths(self, paths):
        self.paths = paths
        self.current_step = 0
        self.update()

    def simulate(self):
        self.current_step = 0
        self.timer.start(30)

    def update_step(self):
        self.current_step += 1
        if self.current_step >= len(self.paths):
            self.timer.stop()
        self.update()

    def paintEvent(self, event):
        if not self.paths:
            return
        qp = QPainter(self)
        qp.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(Qt.GlobalColor.blue, 2)
        qp.setPen(pen)

        last = None
        for i in range(min(self.current_step, len(self.paths))):
            x, y, cmd = self.paths[i]
            x *= 10
            y *= 10
            if cmd == 'draw' and last:
                qp.drawLine(last[0], last[1], x, y)
            last = (x, y)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulador de Impressora PCB")
        self.viewer = GerberViewer()

        open_btn = QPushButton("Abrir Gerber")
        open_btn.clicked.connect(self.abrir_gerber)

        sim_btn = QPushButton("▶️ Simular")
        sim_btn.clicked.connect(self.viewer.simulate)

        enviar_btn = QPushButton("📤 Enviar Arduino")
        enviar_btn.clicked.connect(self.enviar_serial)

        layout = QVBoxLayout()
        layout.addWidget(self.viewer)
        layout.addWidget(open_btn)
        layout.addWidget(sim_btn)
        layout.addWidget(enviar_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.comandos = []

    def abrir_gerber(self):
        path, _ = QFileDialog.getOpenFileName(self, "Abrir Gerber", "", "Gerber Files (*.gbr)")
        if path:
            self.comandos = parse_gerber(path)
            self.viewer.load_paths(self.comandos)

    def enviar_serial(self):
        send_to_arduino('/dev/ttyUSB0', self.comandos)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.resize(1000, 800)
    win.show()
    sys.exit(app.exec())
