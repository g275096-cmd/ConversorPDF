# Arquitetura do ConversorPDF

## Objetivo
O conversorPDF é uma aplicação desktop desenvolvido em Python cujo 
propósito pe converter um ou mais arquivos TIFF
em um documento PDF/A-2B pesquisável por meio da aplicação de OCR (Reconhecimento Óptico de Caracteres).

## Arquitetura
O projeto foi dividido em módulos diferentes.
A arquitetura do projeto baseia-se no princípio de "Dividir para conquistar"; ou seja, o sistema é
decomposto em módulos específicos, cada um responsável por exercer uma função no código. Essa organização
favorece a separação de responsabilidades, tornando o código mais legível, reutilizável e de fácil manutenção.

Sem essa organização, o programa se tornaria menos legível e mais difícil de manter. Consequentemente, 
localizar falhas, implementar novas funcionalidades e realizar correções demandaria mais tempo.

src/  
│

├── gui

├── image

├── ocr

├── pdf

├── core

├── utils

└── config

Cada módulo possui responsabilidade única. Isso reduz o acoplamento entre as diferentes partes do sistema
e facilita sua evolução ao longo do desenvolvimento.

gui: responsável pela interface gráfica

image: manipulação das imagens TIFF.

ocr: comunicação com o Tesseract.

pdf: geração de PDF/A-2B.

core: fluxo principal da aplicação.

utils: funções auxiliares.

config: configurações do sistema.

## Princípios adotados
- Separação de responsabilidades;
- Modularização;
- Facilidade de manutenção;
- Legibilidade de código;
- Reutilização de componentes;
- Escalabilidade do projeto.

## Evolução da arquitetura
A arquitetura inicial do sistema considerava a conversão individual de arquivos TIFF para documentos PDF/A-2B.

Durante o desenvolvimento e a validação dos requisitos, foi identificado que múltiplos arquivos TIFF podem representar
páginas de um mesmo documento arquivístico.

A especificação foi então ajustada para que o sistema seja capaz de: 
1. Processar múltiplos arquivos TIFF;
2. Gerar PDFs temporários individuais;
3. Preservar a ordem dos documentos;
4. Unir os PDFs temporários;
5. Converter o documento unificado para PDF/A-2B;
6. Remover os arquivos intermediários após a conclusão bem-sucedida.

Essa alteração introduziu uma nova etapa de agregação no pipeline, implementada pelo método 'merge_pdfs()'.

## Módulo 'image'
Responsável pelo processamento e preparação das imagens TIFF utilizadas no pipeline de conversão.

### Responsabilidades
O módulo pode realizar operações relacionadas à preparação geométrica das imagens, incluindo:
- abertura de imagens;
- detecção do documento principal;
- correção de inclinação;
- remoção do fundo do scanner;
- recorte da área correspondente ao documento;
- padronização das margens;
- salvamento das imagens processadas.

### Observação
A implementação feita é ainda uma primeira versão funcional do pipeline. É necessário passar pelo processo de testes e validação.

A implementação do módulo foi realizada num programa isolado, para experimentar a funcionalidade. Depois será um artefato
validado para a integração no sistema na sua totalidade.


