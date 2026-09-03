import cv2
from src.image.image_processor import ImageProcessor

processor = ImageProcessor()
input_file = r"G:\Drives compartilhados\Digitalizacao - Bolsistas\Ambiente de Testes\Gabriel\Local de teste - Projeto\Pasta_entrada\Teste0003.tif"

image = processor.open_image(input_file)
result = processor.deskew(image)

processor.save_image(
    result,
    "teste_deskew.png"
)

print("Teste concluído com sucesso")

