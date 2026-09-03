import sys
from weakref import finalize

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QProgressBar
from PySide6.QtWidgets import QTextEdit
from rich import progress
from src.core import converter
from src.core.converter import Converter
from datetime import datetime
from src.core.worker import Worker
from PySide6.QtCore import QThread


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ConversorPDF")
        self.setFixedSize(700, 500)

        main_layout= QVBoxLayout()
        input_layout = QHBoxLayout()
        output_layout = QHBoxLayout()

        # Cria os widgets para o usuário colocar a pasta de entrada
        input_label = QLabel("File input: ")

        self.input_edit = QLineEdit()
        self.input_edit.setPlaceholderText("Select input file")

        # Coloca o botão de procurar pasta
        self.button_input = QPushButton("Browse")
        self.button_input.setFixedSize(70, 40)

        # Conecta o clique do botão ao método
        self.button_input.clicked.connect(self.select_input_file)

        # Adiciona os componentes soltos ao input_layout horizontal
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_edit)
        input_layout.addWidget(self.button_input)

        # Criando componentes para a pasta de saída
        saida_text = QLabel("File output: ")

        self.output_edit = QLineEdit()
        self.output_edit.setPlaceholderText("Select output file")

        self.button_output = QPushButton("Browse")
        self.button_output.setFixedSize(70, 40)
        self.button_output.clicked.connect(self.select_output_file)

        # Cria botão Convert
        self.convert_button = QPushButton("Convert")

        output_layout.addWidget(saida_text)
        output_layout.addWidget(self.output_edit)
        output_layout.addWidget(self.button_output)

        action_layout = QHBoxLayout()
        # Cria botão Convert
        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convert)

        # Adiciona o botão criado no layout de ação
        action_layout.addWidget(self.convert_button)

        # Insere a barra de progresso
        process_label = QLabel("Process: ")
        self.current_file_label = QLabel("File: waiting")

        self.process = QProgressBar()
        self.process.setRange(0, 100)
        self.process.setValue(0)

        self.process.setStyleSheet("""
    QProgressBar {
        border: 1px solid gray;
        border-radius: 5px;
        text-align: center;
        min-height: 25px;
    }

    QProgressBar::chunk {
        background-color: #4A90E2;
    }
    """)

        # OU self.process.setFixedHeight(25)

        # Adiciona à interface a área de log
        log_label = QLabel("Log:")
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setFixedHeight(180)

        # Inserindo os blocos layout no layout principal na interface
        main_layout.addLayout(input_layout)
        main_layout.addLayout(output_layout)
        main_layout.setSpacing(2)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Adiciona ao layout principal o log e a barra de carregamento
        main_layout.addWidget(self.current_file_label)
        main_layout.addWidget(process_label)
        main_layout.addWidget(self.process)
        main_layout.addWidget(log_label)
        main_layout.addWidget(self.log)
        main_layout.addLayout(action_layout)

        widget = QWidget()
        widget.setLayout(main_layout) # layout se torna o único layout da janela
        # significa que layout2 só existe dentro de layout1
        self.setCentralWidget(widget)

    def select_input_file(self):
        # A indentação dessas duas linhas devem estar dentro da classe, mas fora da __init__
        # Queremos que o usuário clique no botão para abrir o gerenciador de arquivos
        # E não abrí-lo automaticamente logo após o programa iniciar
        folder = QFileDialog.getExistingDirectory(self,"Select input folder")
        print(folder)

        if folder:
            self.input_edit.setText(folder)

    # Os botões devem estar separados por métodos
    # Se dois botões estiverem no mesmo método, não importa qual botão o usuário clicar, ambos aparecerão
    def select_output_file(self):
        folder_output = QFileDialog.getExistingDirectory(self, "Select output folder")
        print(folder_output)
        if folder_output:
            self.output_edit.setText(folder_output)

    # Cria método que interage com o backend
    def convert(self):
        self.log.clear()
        input_folder = self.input_edit.text()
        output_folder = self.output_edit.text()

        converter = Converter(input_folder,
                              output_folder,
                              self.add_log,
                              self.update_progress
                              )
        # Objeto recebe a classe com todos os métodos de outra classe
        self.worker = Worker(converter)

        self.thread = QThread()
        # Primeiro liga o objeto worker à função
        self.worker.moveToThread(self.thread)

        # Quando thread tiver começado ele conecta e executa ao método run()
        # E conectar os demais sinais
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.thread.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.conversion_finished)

        # Chama a função à aplicação somente após as conexões
        self.thread.start()

        print("Thread iniciada")

    # Método responsável por finalizar a conversão na interface (executa quando a Thread termina)
    # Restaura o estado da GUI para permitir uma nova conversão (liberando as referências da conversão no final)
    def conversion_finished(self):
        print("Conversão finalizada")
        self.convert_button.setEnabled(True)

        # Renova as referências dos objetos da classe
        self.worker = None
        self.thread = None

        # Imprime última mensagem após o processo
        self.add_log(
            "Application ready for a new conversion.",
            "SUCCESS"
        )

    # Método Log
    # Ele recebe o texto e imprime na tela
    def add_log(self, message, level="INFO"):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.log.append(f"[{current_time}] [{level}] {message}")

    # Método exclusiva para a barra de progresso
    def update_progress(
            self,
            value,
            message
    ):
        self.process.setValue(value)
        self.current_file_label.setText(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()