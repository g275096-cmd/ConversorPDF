import pytesseract
class OcrProcessor:
    def extract_text(self, image):
        print("OCR iniciado")
        text = pytesseract.image_to_string(image,
                                           lang="por"
                                           )
        print("Texto reconhecido")
        print(repr(text))

        return text