from PIL import Image
import pytesseract
from pygments.lexers import q

image = Image.open(r"G:\Drives compartilhados\Digitalizacao - Bolsistas\Ambiente de Testes\Gabriel\Local de teste - Projeto\Pasta_entrada\BR_SPCEDAE_APA_d1_00026_m0001de0028.tif")
print("IMAGE MODE: ", image.mode)
print("IMAGE SIZE: ", image.size)
pdf = pytesseract.image_to_pdf_or_hocr(
    image,
    extension="pdf",
    lang="por",
)

with open("teste.pdf", "wb") as f:
    f.write(pdf)

print("PDF criado.")