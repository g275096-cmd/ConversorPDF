from PIL import Image, ImageOps
import cv2
import numpy as np
from reportlab.graphics.transform import rotate


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
            220,
            255,
            cv2.THRESH_BINARY
        )

        # Remove pequenas regiões e reforça a região clara do documento
        kernel = np.ones((15,15), np.uint8)

        threshold = cv2.morphologyEx(
            threshold,
            cv2.MORPH_CLOSE,
            kernel
        )
        debug_threshold = Image.fromarray(threshold)
        debug_threshold.save("TC01_threshold.png")

        contours, hierarchy = cv2.findContours(
            threshold,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
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

        # -------------------------------------
        # Cria máscara do documento original
        # -------------------------------------
        document_mask = np.zeros(
            gray.shape,
            dtype=np.uint8
        )

        cv2.drawContours(
            document_mask,
            [document_contour],
            -1,
            255,
            thickness=cv2.FILLED
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

        if angle < -45:
            correction_angle = angle + 90
        else:
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
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=(255, 255, 255)
        )

        # ----------------------
        # Rotaciona a máscara do documento
        rotated_mask = cv2.warpAffine(
            document_mask,
            rotation_matrix,
            (
                image_np.shape[1],
                image_np.shape[0]
            ),
            flags=cv2.INTER_NEAREST,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=0
        )

        print("Centro da imagem: ", image_center)
        print("Matriz de rotação:")
        print(rotation_matrix)

        # Detecta a quantidade de contornos
        # da imagem já mascarada
        contours, hierarchy = cv2.findContours(
            rotated_mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        print("Quantidade de contornos na máscara rotacionada: ", len(contours))

        # Conta a quantidade de novos contorno com a rotated_gray
        for index, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            print(f"Contorno {index}: {area}")

        # =============================================================================
        # Reconhece o contorno de maior área
        # Será útil para situações em que uma digitalização produza outros contornos
        # =============================================================================
        document_contour = max(
            contours,
            key=cv2.contourArea
        )
        document_area = cv2.contourArea(document_contour)

        print("Área do documento após a rotação:", document_area)

        # Mantém a máscara original para preservar as bordas do documento
        refined_mask = rotated_mask.copy()

        refined_mask_debug = Image.fromarray(refined_mask)
        refined_mask_debug.save("TC02_refined_mask.png")

        # Aplica a máscara na imagem
        masked_image = np.full_like(
            rotated,
            255
        )

        # rotated é a imagem colorida rotacionada
        masked_image[refined_mask == 255] = (
            rotated[refined_mask == 255]
        )

        # Agora localiza novamente o documento pela máscara refinada
        contours, hierarchy = cv2.findContours(
            refined_mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        document_contour = max(
            contours,
            key=cv2.contourArea
        )

        # Retângulo delimitador
        x, y, width, height = cv2.boundingRect(document_contour)
        print("Bounding rectangle:")
        print("X:", x)
        print("Y:", y)
        print("Width:", width)
        print("Height:", height)

        # =======================
        # Teste de componentes
        # =======================

        # O debug da imagem mascarada é entregue para avaliação visual
        debug_image = masked_image.copy()
        cv2.drawContours(
            debug_image,
            [document_contour],
            -1,
            (0, 0, 255),
            8
        )

        cv2.rectangle(
            debug_image,
            (x, y),
            (x + width, y + height),
            (0, 255, 0),
            8
        )

        # Torna a image um array NumPy utilizando Pillow
        debug_out = Image.fromarray(debug_image)

        debug_out.save("TC03_contorno_bounding.png")

        # salva imagem mascarada antes do recorte
        mask_image_debug = Image.fromarray(masked_image)
        mask_image_debug.save("TC04_masked_image.png")

        ys, xs = np.where(refined_mask == 255)
        print("X mínimo: ", xs.min())
        print("Y mínimo: ", ys.min())
        print("X máximo: ", xs.max())
        print("Y máximo: ", ys.max())

        print("Largura real: ", xs.max() - xs.min() + 1)
        print("Altura real: ", ys.max() - ys.min() + 1)

        margin = 10

        x = max(0, x - margin)
        y = max(0, y - margin)

        width = min(rotated.shape[1] - x, width + 2 * margin)
        height = min(rotated.shape[0] - y, height + 2 * margin)

        # Teste diagnóstico:
        # utiliza a imagem rotacionada diretamente para verificar
        # se o corte está sendo causado pela aplicação da máscara
        cropped = rotated[y:y + height, x:x + width]

        border_cleanup = 12

        cropped = cropped[border_cleanup:-border_cleanup, border_cleanup:-border_cleanup]


        print("Tamanho após o recorte:", cropped.shape)

        # Converte e salva imagem depois do recorte
        cropped_image = Image.fromarray(cropped)
        cropped_image.save("TC05_cropped.png")

        # Processamento final
        bordered_image = self.add_border(cropped_image)

        return bordered_image

        return cropped_image

    def add_border(self, image):
        bordered = ImageOps.expand(
            image,
            border=236,
            fill="white"
        )
        return bordered

    def save_image(self, image, output_path):
        image.save(output_path)
