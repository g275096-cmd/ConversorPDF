import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QProgressBar
from PySide6.QtWidgets import QTextEdit

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

        # Adiciona os componentos soltos ao input_layout horizontal
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

        output_layout.addWidget(saida_text)
        output_layout.addWidget(self.output_edit)
        output_layout.addWidget(self.button_output)

        action_layout = QHBoxLayout()
        self.convert_button = QPushButton("Convert")
        # Adiciona o botão criado no layout de ação
        action_layout.addWidget(self.convert_button)

        # Insere a barra de progresso
        process_label = QLabel("Process: ")

        self.process = QProgressBar()
        self.process.setRange(0, 100)
        self.process.setValue(50)

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
        # A identação dessas duas linhas devem estar dentro da classe, mas fora da __init__
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
