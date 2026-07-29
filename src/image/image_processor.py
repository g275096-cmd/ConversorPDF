from PIL import Image, ImageOps

class ImageProcessor:
    def open_image(self, file):
        image = Image.open(file)
        return image

    def add_border(self, image):
        bordered = ImageOps.expand(
            image,
            border=236,
            fill="black"
        )
        return bordered

    def save_image(self, image, output_path):
        image.save(output_path)
