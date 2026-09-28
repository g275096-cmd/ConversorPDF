import cv2
from pathlib import Path
from src.image.image_processor import ImageProcessor

processor = ImageProcessor()
input_file = r"G:\Drives compartilhados\Digitalizacao - Bolsistas\Ambiente de Testes\BR_SPCEDAE_NURC_II_1_D2_00099_m0008de0043.tif"

output_folder = Path(__file__).parent / "Saída Testes"
output_folder.mkdir(exist_ok=True)

image = processor.open_image(input_file)
result = processor.deskew(image)

processor.save_image(
    result,
    str(output_folder / "TC03_teste_deskew.png")
)

print("Teste concluído com sucesso")
print(f"Saída: {output_folder / 'TC03_teste_deskew.png'}")

