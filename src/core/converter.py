from pathlib import Path
from src.image.image_processor import ImageProcessor

# arquivo py coordenador do fluxo de processo
# Lógica: ler (e conhecer) os caminhos de entrada e saída; se ambos válidos, então inicia a conversão

class Converter:
    # __ini__ construtor guarda o estado (atributos) do objeto
    # self é a referência ao próprio objeto
    def __init__(self, input_folder, output_folder):
        # entrada e saida são parâmetros que o init precisa
        # Elas só existem enquanto o init está em execução
        # Porém, os atributos delas continuam existindo
        # self.entrada é o atributo do objeto (lado esquerdo); input_folder é o parâmetro recebido (lado direito)
        # É importante ter os atributos para o construtor usar nos métodos
        # Atributos são os parâmetros guardados para os métodos utilizarem
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.image_processor = ImageProcessor() # cria um atributo da classe

    # Valida se usuário inseriu as pastas de entrada e de saída
    def validate(self):
        if self.input_folder == "" or self.output_folder == "":
            return False
        else:
            return True

    def start(self):
        if not self.validate():
            print("Input folder is invalid")
            return False

        files = self.load_tiff_files()
        print(files)

        if len(files) == 0:
            print("No tiff files found")
            return False

        for file in files:
            self.process_file(file)

        print("Conversion finished")
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

        return tiff_files

    def process_file(self, file):
        image = self.image_processor.open_image(file)
        image = self.image_processor.add_border(image)
        output_file = Path(self.output_folder) / file.name
        self.image_processor.save_image(image, output_file)

        print(file.name)
        print(image.size)

        processor = ImageProcessor()
        image = processor.open_image(file)