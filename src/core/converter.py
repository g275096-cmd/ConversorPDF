from pathlib import Path

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

           # Processo ainda precisa ser implementado
        pass

        files = self.load_tiff_files()
        print(len(files))

        for file in files:
            print(file)

    # Etapa de carregamento dos arquivos TIFF
    def load_tiff_files(self):
        # folder assume como objeto Path
        # Recebe uma pasta e retorna uma lista de arquivos TIFF
        folder = Path(self.input_folder)

        tiff_files = []

        # Percorre o conteúdo da pasta (Path)
        for file in folder.iterdir():
            # Reconhece a extensão do arquivo e a padroniza
            if file.suffix.lower() in (".TIFF", "*.tiff"):
                # Adiciona um elemento ao final da lista
                tiff_files.append(file)


            return tiff_files


