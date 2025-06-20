"""
pdf_to_png.py

"""

from pdf2image import convert_from_path
import cv2
import numpy as np
import os

# Ruta al archivo PDF escaneado
file = 'Dato1.pdf'
path = r"C:\Users\Acer\Documents\python\Asistencia automatica\research\_DataSet_"
pdf_path = os.path.join(path, file)


# Convertir la primera página del PDF en una imagen PIL
pages = convert_from_path(pdf_path, dpi=300)

# Elegir la primera página (puedes iterar si hay más)
pil_image = pages[0]

# Convertir la imagen PIL a formato OpenCV (BGR)
cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)


#cv2.imshow("Imagen del PDF", cv_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("Dato1.png", cv_image)