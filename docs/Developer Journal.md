# Developer Journal

## Data
20/07/2026

## Objetivos alcançados
Hoje foi concluída a fase de organização do ambiente de desenvolvedor e da fase inicial de planejamento
e infraestrutura do projeto.

### Ambiente de desenvolvimento
- Instalação do Python 3.12
- Configuração do PyCharm como IDE principal
- Criação do ambiente virtual (.venv)
- Instalação das dependências do projeto
- Configuração do Tesseract OCR
- Configuração do Ghostscript
- Configuração do Git

### Organização do projeto
Foi cira a estrutura inicial do projeto seguindo uma organização modular:
- src
- docs
- resources
- tests
- logs
- output
- temp
- scripts

Essa organização visa facilitar a manutenção, reutilização e escalabilidade do sistema.

### Documentação produzida
Foram criados os seguintes documentos:
- Arquitetura.md
- Fluxo_do_programa.md
- Changelog.md
- Ideias.md
- README.md

Foi construído também um diagrama do fluxo do programa utilizando draw.io.

### Conceitos estudados
Os conceitos estudados foram:
- Ambiente virtual (.venv)
- Git
- Estrutura de projetos Python
- Organização modular
- Arquitetura de Software
- Separação de responsabilidades
- Documentação técnica
- Controle de versões
- Fluxograma de processos

### Decisões do projeto

- Python 3.12 como versão padrão.
- PyCharm como IDE principal.
- PySide6 para a interface gráfica.
- Git para controle de versões.
- GitHub para hospedagem do projeto.
- Tesseract para OCR.
- Ghostscript para geração do PDF/A.

### Próxima etapa

Iniciar o desenvolvimento da interface gráfica do ConversorPDF utilizando PySide6.

## Data
27/07/2026

### Objetivos alcançados
Iniciar o desenvolvimento do backend do ConversorPDF e compreender como organizar o fluxo e lógica
principal da aplicação utilizando orientação a objetos.

### Conceito aprendidos
Compreendi que uma classe representa uma entidade responsável por executar determinada tarefa.
O construtor (__init__) recebe as informações necessárias para inicializar o objeto e armazena
essas informações em atributos utilizando self.
Quando o construtor encerra a execução, os parâmetros recebidos deixam de existir, ficando somente
os atributos disponíveis ao longo de toda a vida do objeto.

Assim, parâmetro é uma informação temporária, enquanto que o atributo é uma informação armazenada
no objeto.

### Estado e Comportamento
Um objeto é composto por Estado, que são os atributos, e Comportamento, que são os métodos. Estado seria as 
informações ou dados que recebe, por exemplo, do usuário. Com tais dados, os métodos podem utilizá-los para
processar as informações

### Organização do backend
A classe Converter atua como coordenadora do fluxo lógico de aplicação.
Não executa uma função específica (como OCR), mas controla a sequência das etapas do processo.

Fluxo planejado:
start() --> validate() --> load_tiff_files() --> OCR --> geração do PDF --> finalização

### Biblioteca pathLib
A classe Path ajuda a manipular diretórios e arquivos.
Logo, ao em vez de trabalhar apenas com strings, um objeto Path oferece métodos específicos para
manipular o sistema de arquivos. 
Conceitos usados:
Path(); iterdir(); suffix; lower()

### Listas em Python
append() adiciona um elemento;

len() retorna a quantidade de elementos.

### Responsabilidade única
validate() apenas verifica se os dados são válidos;
load_tiff_files() apenas localiza os arquivos TIFF;
start() coordena o fluxo da aplicação.

### Dificuldades encontradas
por que utilizar o self em PySide6; diferença entre parâmetros e atributos; quando um método deve
receber parâmetros e quando deve utilizar os atributos do objeto; e utilização da biblioteca pathLib.

### Próxima meta
Localizar todos os arquivos TIFF em converter.py;
iniciar o processamento de cada arquivo;
integrar os módulos de imagem, OCR e geração do PDF.

## Data 
29/07/2026

### Objetivo
Iniciar o processamento real dos arquivos TIFF.

### Implementado
- Criação da classe 'ImageProcessor'.
- Método 'open_image()' utilizando Pillow.
- Método 'add_border()' utilizando 'ImageOps.expand'.
- Método 'save_image()' para salvar a imagem processada.
- Integração entre 'Converter' e 'ImageProcessor'.
- Organização do processamento em 'process_file()'.

### Aprendizados
- A classe 'Converter' coordena o fluxo, mas não processa imagens diretamente.
- A classe 'ImageProcessor' possui responsabilidade única: manipular imagens.
- O 'Converter' mantém uma instância de 'ImageProcessor' como atributo.
- Um método pode retorna um objeto ('image') que será utilizado por outro método.
- A biblioteca Pillow trabalha com objetos 'Image', permitindo modificar a imagem antes de salvá-la.

# Próxima meta
Implementar a geração do PDF/A-2B a partir da imagem processada.

