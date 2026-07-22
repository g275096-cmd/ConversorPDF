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