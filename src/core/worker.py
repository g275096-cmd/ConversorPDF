from PySide6.QtCore import QObject, Signal, Slot
from src.core.converter import Converter

class Worker(QObject):
    finished = Signal()
    def __init__(self, converter: Converter):
        super().__init__()
        # Atributo recebe objeto completo (da classe Converter) com todos os métodos
        self.converter = converter

    def run(self):
        self.converter.start()
        self.finished.emit()

