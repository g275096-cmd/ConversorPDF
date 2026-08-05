from PIL import Image
import pytesseract

image = Image.open(r"G:\Drives compartilhados\Digitalizacao - Bolsistas\Ambiente de Testes\Gabriel\Local de teste - Projeto\Pasta_entrada\Teste0001.tif")

pdf = pytesseract.image_to_pdf_or_hocr(
    image,
    extension="pdf",
    lang="por",
)

with open("teste.pdf", "wb") as f:
    f.write(pdf)

print("PDF criado.")