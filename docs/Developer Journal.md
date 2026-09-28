# Developer Journal

## Data
20/07/2026

### Objetivos alcançados
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

### Próxima meta
Implementar a geração do PDF/A-2B a partir da imagem processada.

## Data 
30/07/2026

### Objetivo
Integrar o backend com a interface gráfica e torna o processo de conversão mais transparente e intuitiva para o operador

### Implementações
Backend
- estruturada a classe Converter como coordenadora do fluxo lógico de conversão.
- implementado o processamento sequencial dos arquivos TIFF.
- Integração de classes:
- ImageProcessor
- OCRProcessor
- PDFProcessor

### Comunicação BACKEND -> GUI
Foi implementado o uso de callbacks para desacoplar o backend da interface

### Callback de log
A GUI fornece um método responsável apenas por exibir mensagens.
O Backend apenas informa quando deseja registrar eventos.

### Callback de progresso
Implementada comunicação semelhante para atualizar a barra de progresso.
Fluxo:

Converter -> self.progress(...) -> MainWindow.update_progress() -> QProgressBar.setValue()

### Sistemas de Logs
Implementado registro de eventos com: 

- Horário automático;
- níveis de mensagem (categorização de eventos).

### Fluxo de Objetos
O resultado obtido por uma classe se torna posteriormente entrada da próxima.
Exemplo:

ImageProcessor -> imagem -> OCRProcessor -> texto -> PDFProcessor -> PDF final

A classe Converter apenas coordena esse fluxo de aplicação.

### Metas 
- Implementar geração de PDF/A-2B.
- Executar o processamento em QThread.
- Melhorar a barra de progresso.
- Implementar tratamento robusto de exceções.
- Criar configurações do usuário.

## Data
17/08/2026

### Metas concluídas
- Abre arquivos TIFF;
- Adição borda no arquivo;
- Geração de PDF temporário;
- Junção de múltiplos PDFs em um único;
- Remoção dos PDFs temporários.

### Metas pendentes
- Corrigir conversão para PDF/A-2B;
- Aplicar a nomenclatura arquivística final;
- Tornar a barra de progresso dinâmica;
- Aplicar funções de edição nos arquivos TIFF (alinhamento, borda branca, etc.).

### Problemas identificados
1. O arquivo merged_temp.pdf é sobrescrito a cada nova execução.
2. O documento merged_temp.pdf ainda não é convertido para o padrão PDF/A-2B.
3. O nome arquivístico do PDF ainda não foi implementado.

## Data
24/08/2026

### Objetivo
Continuar o desenvolvimento do pipeline de conversão e implementar a conversão do documento unificado para o padrão PDF/A-2B

### Validação
A conversão foi testada com múltiplos arquivos TIFF.
Resultados: 
- Todos os TIFFs foram reunidos num único documento;
- O documento final permaneceu pesquisável e foi identificado como PDF/A-2B pelo ABBYY;
- A camada OCR foi preservada.
A validação confirmou que o pipeline está funcionando corretamente, conforme a especificação.

### Próximas metas:
- Implementar a nomenclatura arquivística automática do PDF final;
- Remover os arquivos temporários somente após a conversão final bem-sucedida;
- Adicionar mensagens dessas etapas ao log de aplicação;
- Continuar o desenvolvimento da barra de progresso;
- Resolver sobrescrita de arquivos intermediários quando houver múltiplas conversões na mesma pasta.

## Data
02/09/2026

### Marco
Implementação inicial do pipeline de edição geométrica das imagens.

O objetivo desta implementação é automatizar parte do procedimento anteriormente realizado manualmente pelo operador
o processo de digitalização.

### Avanços no componente deskew do sistema (OpenCV)
Foi implementado no sistema a funcionalidade deskew para alinhar documentos. O componente responsável conseguiu:
1. Converter a imagem PIL para NumPy.
2. Converter para tons de cinza.
3. Aplicar threshold com Otsu.
4. Encontrar os contornos externos.
5. Identificar o maior contorno como o documento.
6. Usar minAreaRect() para obter orientação do documento.
7. Extrair o ângulo.
8. Criar a matriz de rotação
9. Aplicar warpAffine() na imagem original.

## Data
28/09/2026

### Marco histórico
Correção da função deskew(), recorte e bordas

### Problema identificado
Com os primeiros testes do ConversosPDF pela interface GUI, o processamento de imagens apresentou um problema referente ao recorte da página.

O problema mais evidente era que no PDFA final, algumas páginas tiveram o seu cabeçalho recortado, retirando o código arquivístico do documento. Outro problema evidente percebido foi na existência de faixas do fundo do scanner em algumas páginas do documento.

Então, o objetivo passou a ser:
- Corrigir a inclinação da página;
- Identificar corretamente os limites do documento;
- Preservar as extremidades da folha;
- Não cortar cabeçalhos ou o código da página;
- Eliminar o fundo do scanner
- Produzir uma imagem adequada para a geração do PDF/A - 2B.

A partir disso a função deskew() passou a ser depurada em cada trecho. Foram gravadas imagens intermediárias a fim de descobrir em qual estágio o conteúdo estava sendo perdido. 
Foram criados arquivos de diagnósticos "Teste de Componentes":
- TC01_threshold.png;
- TC01_refined_mask.png;
- TC01_cropped.png; etc.

Em seguida, adotou-se o processamento de imagem em tons de cinza. 

``
python >> gray = cv2.cvtColor(imagem_np, cv2.COLOR_RGB2GRAY)
``

Com essa aplicação, visa abordar uma estratégia utilizada para aumentar a intensidade de contraste para delimitar a forma do que era realmente documento de borda de scanner, eliminando canais de cores, R, G e B.

Na sequência, adotou-se o trecho abaixo:

```
python >>> kernel = np.ones((15,15), np.uint8)
python >>> threshold = vc2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel)
```
A ideia é manter o tratamento da máscara para reforçar a região clara do documento e reduzir pequenas regiões/irregularidades antes da aplicação dos contornos.

### - Correção da inclinação
```cv2.minAreaRect()``` foi então usado para obter a orientação geométrica da folha.
O valor do ângulo retornada, calculou-se o ângulo de correção (angle) e aplicada uma rotação com ```cv2.warAffine()```.

```text
rotated_mask = cv2.warAffine(document, mask, rotation_matrix, (...), flags=cv2.BORDER_CONSTANT, borderValue=0)
```

Este comando acima permitiu que pudesse ser analisado separadametne a imagem efetivamente rotacionada, e a região que o algoritmo considerava pertencente ao documento.

Em seguida, avançou para etapas de identificação da causa do corte de bordas (pequenas faixas presentes nas extremidades das páginas do PDFA), e para a sessão com teste de recorte (TC01_cropped).

Nos testes mais recente feitos pela interface gráfica, observou-se uma melhora importante nos seguintes requisitos:
- algumas páginas que tinha seu cabeçalho recortado agora passaram a preservá-lo;
- a região superior do documento passou a ser mantida de forma mais consistente;
- o documento contina sendo convertido para o PDF/A - 2B e permanece pesquisável;
- a margem branca continua sendo um requisito funcional para o resultado final.

Porém, ainda existe partes pendentes. Ei-las:
- eliminar de maneira consistente as faixas pretas do fundo do scanner presente em algumas páginas do PDF, principalmente ocorrendo em testes em lote;
- validar o comportamento em uma bateria maior de TIFFs, considerando as diferentes dimensões e características que os documentos podem apresentar.

### Estado atual: parcialmente concluída
Atualmente, o programa entrega um comportamento funcional. Ele avançou na correção do recorte e das correções de detecção de contorna, criação e rotação de máscaras. Foram realizados diversos testes de componentes para identificar falhas de tratamento. Apesar de algumas melhoras, ainda falta refinar e tornar consistente a eliminação das faixas do fundo de scanner. 

A próxima etapa visa investigar e corrigir erros relacionado ao acabamento das imagens. 