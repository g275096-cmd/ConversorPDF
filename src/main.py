from pypdf import PdfReader, PdfWriter

pdfs = [
    r"G:\Drives compartilhados\Digitalizacao - Bolsistas\Ambiente de Testes\Gabriel\TestesBordas\Teste0001.tif",
]

writer = PdfWriter()

for pdf in pdfs:
    reader = PdfReader(pdf)

    for page in reader.pages:
        print(page.extract_text())

    for page in reader.pages:
        writer.add_page(page)

with open("test.pdf", "wb") as f:
    writer.write(f)