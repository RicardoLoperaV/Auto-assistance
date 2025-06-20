"""
output_Dato1.py

"""

from paddleocr import PaddleOCR
import os

# Inicializar OCR en español
ocr = PaddleOCR(use_angle_cls=True, lang='es')


file = 'Dato1.png'
path = r"C:\Users\Acer\Documents\python\Asistencia automatica\research\PaddleOCR\intento3\procesamientoImagen"
file = os.path.join(path, file)

# Realizar OCR
result = ocr.predict(file)

for res in result:
    res.print()
    res.save_to_img("output_Dato1")
    res.save_to_json("output_Dato1")

