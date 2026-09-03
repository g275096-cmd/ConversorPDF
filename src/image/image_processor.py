from PIL import Image, ImageOps
import cv2
import numpy as np

class ImageProcessor:
    def open_image(self, file):
        image = Image.open(file)
        return image

    # Método para alinhar o arquivo
    def deskew(self, image):
        image_np = np.array(image)

        gray = cv2.cvtColor(
            image_np,
            cv2.COLOR_RGB2GRAY
        )

        print("Gray shape:", gray.shape)

        _, threshold = cv2.threshold(
            gray,
            0,255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        contours, hierarchy = cv2.findContours(
            threshold,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,

        )

        print("Quantidade de contornos:", len(contours))

        # Inspeciona as áreas de contornos
        for index, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            print(f"Contorno {index}: {area}")

        document_contour = max(
            contours,
            key=cv2.contourArea
        )

        document_area = cv2.contourArea(document_contour)

        print("Área do documento:", document_area)

        # Identifica a orientação geométrica do documento
        rect = cv2.minAreaRect(document_contour)
        print("Retângulo mínimo:", rect)

        (center_x, center_y), (width, height), angle = rect

        print("Centro:", center_x, center_y)
        print("Largura:", width)
        print("Altura:", height)
        print("Ângulo:", angle)

        image_center = (
            image_np.shape[1] // 2,
            image_np.shape[0] // 2
        )

        correction_angle = angle
        print("Ângulo de correção:", correction_angle)

        # Matriz de rotação
        rotation_matrix = cv2.getRotationMatrix2D(
            image_center,
            correction_angle,
            1.0
        )

        # Rotação efetiva
        rotated = cv2.warpAffine(
            image_np,
            rotation_matrix,
        (
                image_np.shape[1],
                image_np.shape[0]
            ),
        )

        print("Centro da imagem: ", image_center)
        print("Matriz de rotação:")
        print(rotation_matrix)

        # Com o documento rotacionado, faz novamente sua detecção
        rotated_gray = cv2.cvtColor(
            rotated,
            cv2.COLOR_RGB2GRAY
        )

        _, rotated_threshold = cv2.threshold(
            rotated_gray,
            0, 255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        contours, hierarchy = cv2.findContours(
            rotated_threshold,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        print("Quantidade de contornos após a rotação: ", len(contours))

        # Conta a quantidade de novos contorno com a rotated_gray
        for index, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            print(f"Contorno {index}: {area}")

        # Reconhece o contorno de maior área
        # Será útil para situações em que uma digitalização produza outros contornos
        document_contour = max(
            contours,
            key=cv2.contourArea
        )

        document_area = cv2.contourArea(document_contour)

        print("Área do documento após a rotação:", document_area)

        # Retângulo delimitador
        x, y, width, height = cv2.boundingRect(document_contour)
        print("Bounding rectangle:")
        print("X:", x)
        print("Y:", y)
        print("Width:", width)
        print("Height:", height)

        cropped = rotated[y:y + height, x:x + width]

        print("Tamanho após o recorte:", cropped.shape)

        cropped_image = Image.fromarray(cropped)

        bordered_image = self.add_border(cropped_image)

        return bordered_image

    def add_border(self, image):
        bordered = ImageOps.expand(
            image,
            border=236,
            fill="white"
        )
        return bordered

    def save_image(self, image, output_path):
        image.save(output_path)
