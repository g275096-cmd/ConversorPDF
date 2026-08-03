from pathlib import Path

class PDFProcessor:
    def create_pdf(self, image, output_path):
        if image.mode != "RGB":
            image = image.convert("RGB")

        image.save(output_path, "PDF", resolution=300.0)
