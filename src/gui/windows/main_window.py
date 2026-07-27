import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QFileDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ConversorPDF")
        self.setFixedSize(700, 500)\

        main_layout= QVBoxLayout()
        input_layout = QHBoxLayout()
        output_layout = QHBoxLayout()

        # Cria os widgets para o usuário colocar a pasta de entrada
        input_label = QLabel("File input: ")

        input_edit = QLineEdit()
        input_edit.setPlaceholderText("Select input file")

        # Coloca o botão de procurar pasta
        button = QPushButton("Browse")
        button.setFixedSize(70, 40)

        # Adiciona os componentos soltos ao layout2 horizontal
        input_layout.addWidget(input_label)
        input_layout.addWidget(input_edit)
        input_layout.addWidget(button)

        # Criando componentes para a pasta de saída
        saida_text = QLabel("File output: ")

        saida = QLineEdit()
        saida.setPlaceholderText("Select output file")

        button_output = QPushButton("Browse")
        button_output.setFixedSize(70, 40)
        output_layout.addWidget(saida_text)
        output_layout.addWidget(saida)
        output_layout.addWidget(button_output)

        # Inserindo todo o bloco layout2 em layout1
        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)
        main_layout.setSpacing(2)
        main_layout.setContentsMargins(10, 10, 10, 10)

        widget = QWidget()
        widget.setLayout(main_layout) # layout se torna o único layout da janela
        # significa que layout2 só existe dentro de layout1
        self.setCentralWidget(widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()