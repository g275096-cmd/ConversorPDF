from pathlib import Path
import pytesseract
import subprocess
from pypdf import PdfWriter, PdfReader

class PDFProcessor:
    def create_pdf(self, image, output_path):
        if image.mode != "RGB":
            image = image.convert("RGB")

        print("IMAGE MODE: ", image.mode)
        print("IMAGE SIZE: ", image.size)

        pdf = pytesseract.image_to_pdf_or_hocr(
            image,
            extension="pdf",
            lang="por"
        )

        with open(output_path, "wb") as f:
            f.write(pdf)

    # Método recebe os pdfs temporários em ordem e o arquivo de destino
    def merge_pdfs(self,
                   temp_pdfs,
                   merged_pdf):

        writer = PdfWriter()

        for temp_pdf in temp_pdfs:
            reader = PdfReader(temp_pdf)

            for page in reader.pages:
                writer.add_page(page)

        with open(merged_pdf, "wb") as f:
            writer.write(f)

        print(f"Quantidade de PDFs: {len(temp_pdfs)}")
        print(f"PDF gerado: {merged_pdf}")
        print(f"Arquivo existe? {merged_pdf.exists()}")

    def convert_pdfa(self, input_pdf, output_pdf):
        gs = r"C:\Program Files\gs\gs10.07.1\bin\gswin64c.exe"

        project_root = Path(__file__).resolve().parents[2]

        pdfa_def = project_root / "resources" / "pdfa" / "PDFA_def.ps"
        icc_profile = str(project_root / "resources" / "color" / "default_rgb.icc")


        # Lista de comando próprio do Ghostscript
        command = [
            gs,
            "-dPDFA=2",
            "-dBATCH",
            "-dNOPAUSE",
            "-dNOOUTERSAVE",
            "-sDEVICE=pdfwrite",
            "-sProcessColorModel=DeviceRGB",
            "-sColorConversionStrategy=RGB",
            f"-sOutputFile={output_pdf}",
            f"--permit-file-read={icc_profile}",
            str(pdfa_def),
            str(input_pdf),
        ]
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        print("STDOUT:")
        print(result.stdout)
        print("STDERR:")
        print(result.stderr)
        result.check_returncode()