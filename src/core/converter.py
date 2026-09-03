from pathlib import Path
from src.image.image_processor import ImageProcessor
from src.pdf.pdf_processor import PDFProcessor
from src.ocr.ocr_processor import OcrProcessor

# arquivo py coordenador do fluxo de processo
# Lógica: ler (e conhecer) os caminhos de entrada e saída; se ambos válidos, então inicia a conversão

class Converter:
    # __ini__ construtor guarda o estado (atributos) do objeto
    # self é a referência ao próprio objeto
    def __init__(self,
                 input_folder,
                 output_folder,
                 log_callback,
                 process_callback):
        # entrada e saída são parâmetros que o init precisa
        # Elas só existem enquanto o init está em execução
        # Porém, os atributos delas continuam existindo
        # self.entrada é o atributo do objeto (lado esquerdo); input_folder é o parâmetro recebido (lado direito)
        # É importante ter os atributos para o construtor usar nos métodos
        # Atributos são os parâmetros guardados para os métodos utilizarem
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.log = log_callback
        self.progress = process_callback
        self.image_processor = ImageProcessor() # cria um atributo da classe e a instância é armazenada no atributo
        self.pdf_processor = PDFProcessor() # Cria atributo da classe PDFProcessor()
        self.ocr_processor = OcrProcessor() # Cria atributo da classe OcrProcessor()
        # O valor da instância pelo objeto no método da classe é atribuído ao atributo

    # Valida se usuário inseriu as pastas de entrada e de saída
    def validate(self):
        if self.input_folder == "" or self.output_folder == "":
            return False
        else:
            return True

    def start(self):
        self.log("Starting conversion", "INFO")

        if not self.validate():
            print("Input folder is invalid.", "ERROR")
            return False

        files = self.load_tiff_files()

        self.log(f"{len(files)} files found.", "INFO")

        total = len(files)

        if len(files) == 0:
            self.log("No tiff files found.", "ERROR")
            return False

        # Lista que guarda os pdfs temporários
        temp_pdfs = []

        for index, file in enumerate(files, start=1):
            self.log(f"Processing {file.name}...", "INFO")

            temp_pdf = self.process_file(file)
            temp_pdfs.append(temp_pdf)


            progress = int(index / total * 100)
            self.progress(progress, f"Processing {file.name}")

        merged_pdf = Path(self.output_folder) / "merged_temp.pdf"
        pdfa_output = Path(self.output_folder) / "final_pdfa.pdf"

        self.pdf_processor.merge_pdfs(
            temp_pdfs,
            merged_pdf,
        )
        self.pdf_processor.convert_pdfa(
            merged_pdf,
            pdfa_output
        )

        print("PDFs temporários: ")

        for pdf in temp_pdfs:
            print(pdf)

        self.pdf_processor.remove_temp_pdfs(temp_pdfs)

        self.log("Conversion sucessfully completed.", "SUCCESS")

        return True

    # Etapa de carregamento dos arquivos TIFF
    def load_tiff_files(self):
        # folder assume como objeto Path
        # Recebe uma pasta e retorna uma lista de arquivos TIFF
        folder = Path(self.input_folder)

        tiff_files = []

        # Percorre o conteúdo da pasta (Path)
        for file in folder.iterdir():
            # Reconhece a extensão do arquivo e a padroniza
            if file.suffix.lower() in (".tif", ".tiff"):
                # Adiciona um elemento ao final da lista
                tiff_files.append(file)

        return sorted(tiff_files, key=lambda file: file.name)

# Explicação do bloco abaixo:
# Método recebe um arquivo file. Esse arquivo é uma instância que chama uma função do método de uma classe
# Nessa classe, o método é feito e retorna o objeto ao atributo da classe Converter
# Por fim, é armazenada na variável image
# Depois, essa última imagem novamente chama através de um atributo, mas instância de outra classe, uma função especialista
# E retorna essa nova imagem processada para a mesma variável de antes
# Mas para evitar confusão, a classe Converter importa as instância das classes especialistas
# Agora para o OCR, a variável text recebe a instância de uma classe especialista que chama uma função daquele método
# O método retorna um objeto (ou string, depende do tipo de dado). E a instância (objeto) é armazenado no atributo, onde a var text recebe esse valor da image

    def process_file(self, file):
        self.log("Opening file...", "INFO")
        image = self.image_processor.open_image(file)

        self.log("Adding border...", "INFO")
        image = self.image_processor.add_border(image)

        self.log("Extracting text...", "INFO")

        self.log("Generating PDF...", "INFO")

        temp_pdf = Path(self.output_folder) / (file.stem + "_temp.pdf")
        final_pdf = Path(self.output_folder) / (file.stem + ".pdf")

        self.pdf_processor.create_pdf(
            image,
            temp_pdf
        )

        self.log(f"{file.name} -> {final_pdf.name}")

        return temp_pdf

    # Método responsável por nomear o PDF com a convenção do centro arquivístico
    def build_output_path(self, file):
        pass