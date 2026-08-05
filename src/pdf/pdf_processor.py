from pathlib import Path
import pytesseract
import subprocess

class PDFProcessor:
    def create_pdf(self, image, output_path):
        if image.mode != "RGB":
            image = image.convert("RGB")

        pdf = pytesseract.image_to_pdf_or_hocr(
            image,
            extension="pdf",
            lang="por"
        )

        with open(output_path, "wb") as f:
            f.write(pdf)

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

