"""
preprocessImagenPipeLine.py

"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

def preprocess_for_ocr(image_path):
    """
    Aplica un pipeline de pre-procesamiento a una imagen para mejorar el rendimiento del OCR.
    """
    # 1. Cargar la imagen
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: No se pudo cargar la imagen en {image_path}")
        return None
        
    # 2. Convertir a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 3. Binarización Adaptativa: Es el paso más importante para limpiar el fondo.
    #    - ADAPTIVE_THRESH_GAUSSIAN_C: El método de umbral.
    #    - THRESH_BINARY_INV: Invierte el resultado (texto en blanco, fondo en negro). Lo haremos así para facilitar la eliminación de líneas.
    #    - Block Size (e.g., 15): El tamaño del vecindario para calcular el umbral. Debe ser un número impar.
    #    - C (e.g., 11): Una constante que se resta de la media.
    binary_inv = cv2.adaptiveThreshold(
        gray,
        maxValue=255,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType=cv2.THRESH_BINARY_INV,
        blockSize=15, # Ajustar según el tamaño del texto
        C=11         # Ajustar para afinar la detección
    )

    # 4. Eliminación de líneas de la tabla (Paso Avanzado pero muy útil)
    # Crear una copia para no modificar la imagen binarizada original
    no_lines = binary_inv.copy()

    # --- Eliminar líneas horizontales ---
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1)) # Kernel para detectar líneas horizontales
    detected_lines = cv2.morphologyEx(binary_inv, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    
    # Dilatar las líneas detectadas para asegurarse de que se borren por completo
    cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(no_lines, [c], -1, (0,0,0), 3) # "Pintar" de negro sobre las líneas (recuerda que está invertida)

    # --- Eliminar líneas verticales ---
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25)) # Kernel para detectar líneas verticales
    detected_lines = cv2.morphologyEx(binary_inv, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    
    cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(no_lines, [c], -1, (0,0,0), 3)

    # 5. Invertir la imagen de vuelta a texto negro sobre fondo blanco
    processed_image = cv2.bitwise_not(no_lines)
    
    # Opcional: Aplicar un filtro de mediana para eliminar el ruido restante
    processed_image = cv2.medianBlur(processed_image, 3)

    return processed_image

# --- Uso del script ---
image_path = 'Dato1.png'
processed_image = preprocess_for_ocr(image_path)

cv2.imwrite("Dato1preprocess.png", processed_image)

if processed_image is not None:
    # Mostrar la imagen original vs la procesada para comparar
    original_image = cv2.imread(image_path)
    plt.figure(figsize=(15, 10))
    plt.subplot(1, 2, 1)
    plt.title('Original')
    plt.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.title('Procesada para OCR')
    plt.imshow(processed_image, cmap='gray')
    plt.axis('off')
    plt.show()


