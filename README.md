# Auto-assistance
**Descripción**
Este proyecto nace de la necesidad de eliminar el trabajo manual y los errores asociados a la carga de listas de asistencia. Mediante técnicas de OCR (Reconocimiento Óptico de Caracteres) y la integración con Google Forms, se logra capturar automáticamente los nombres (o identificadores) de las personas presentes y registrarlos en un formulario digital, listo para ser procesado y almacenado en la nube.

**Objetivos**
- **Reducir tiempo y esfuerzo**: Eliminar la tarea manual de transcribir listados de asistencia.

- **Minimizar errores**: Aprovechar OCR para extraer datos con alta precisión.

- **Integración fluida**: Enviar automáticamente los datos extraídos a un Google Form, manteniendo el flujo de trabajo en la plataforma favorita del equipo.

**Cómo funciona**
1. Lectura de entrada: El usuario proporciona una imagen o PDF con la lista de asistencia.

2. Extracción OCR: El sistema detecta y extrae los nombres (o IDs) de los asistentes.

3. Validación: Se coteja la lista extraída con un archivo maestro (CSV/JSON) para corregir errores.

4. Relleno de formulario: Cada registro validado se envía automáticamente al Google Form configurado.

5. Reporte: Se genera un log con el estado de cada envío y se almacena junto con la imagen original.
