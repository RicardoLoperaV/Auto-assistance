"""
Bot_asistencias2.py

"""

import pandas as pd
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# --- Configuración para parecer menos bot ---

def get_undetected_driver():
    options = Options()
    # 1. User-Agent aleatorio: Simula diferentes navegadores y sistemas operativos
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/125.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36",
    ]
    options.add_argument(f"user-agent={random.choice(user_agents)}")

    # 2. Evitar la detección de "webdriver" (método JavaScript)
    options.add_argument("--disable-blink-features=AutomationControlled")

    # 3. Desactivar barras de información y extensiones (común en bots)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # 4. Modos "headless" o "incógnito" pueden ser detectados. Es mejor evitarlos si no son estrictamente necesarios para el inicio de sesión.
    # Si vas a iniciar sesión manualmente, no uses headless al principio.

    driver = webdriver.Chrome(options=options)

    # 5. Ejecutar scripts para ocultar aún más la huella de Selenium
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]})") # Simular plugins
    driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})") # Simular lenguajes

    return driver

# --- Leer datos del archivo CSV ---
try:
    data = pd.read_csv('data.csv')
except FileNotFoundError:
    print("Error: El archivo 'data.csv' no se encontró. Asegúrate de que esté en el mismo directorio que el script.")
    exit()

# --- Inicializar el web driver ---
driver = get_undetected_driver()

# --- Abrir el Google Form ---
form_url = "https://docs.google.com/forms/d/e/1FAIpQLSddcCxU016sHyXP5UBuZnsNVMMs1yhNxPmpBMHNPdZCnlSRyQ/viewform"
driver.get(form_url)

print("Por favor, inicia sesión manualmente en el navegador y luego presiona Enter aquí para continuar...")
input() # Espera la entrada del usuario

print('Continuando con el llenado del formulario...')

# --- Iterar sobre las filas del archivo Excel ---
for index, row in data.iterrows():
    try:
        Num_asignado = row["Numero"]
        Tipo = row["Tipo"]

        # 6. Esperas variables: No siempre el mismo tiempo
        time.sleep(random.uniform(1, 3))

        # 7. Usar WebDriverWait para elementos críticos
        # Checkbox para el correo (asegurarse de que la página se haya cargado)
        try:
            checkbox = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@aria-label, 'Registrar') and contains(@aria-label, 'correo')]"))
            )
            if checkbox.get_attribute('aria-checked') == 'false':
                checkbox.click()
                time.sleep(random.uniform(0.5, 1.5)) # Pequeña pausa después de interactuar
        except Exception as e:
            print(f"No se pudo encontrar o interactuar con el checkbox del correo para la fila {index}: {e}")

        # Campo de texto para el número asignado
        textbox = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "(//input[@type='text'])[1]"))
        )
        textbox.clear()
        # 8. Simular escritura humana: Escribir carácter por carácter con pausas
        for char in str(Num_asignado):
            textbox.send_keys(char)
            time.sleep(random.uniform(0.05, 0.2)) # Pausa entre caracteres

        time.sleep(random.uniform(0.5, 1.5))

        # Desplegable para seleccionar el nombre
        dropdown_trigger = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@jsname='wQNmvb' and @role='option']"))
        )
        # 9. Usar ActionChains para clics más "humanos"
        ActionChains(driver).move_to_element(dropdown_trigger).click().perform()

        time.sleep(random.uniform(0.5, 1.5))

        # Opción dentro del desplegable
        # Asegúrate de que 'Thomas Martínez Velásquez' sea el texto exacto visible para el usuario.
        # Si el texto es dinámico, podrías necesitar una estrategia más robusta para encontrar el elemento.
        option_xpath = f"//div[@jsname='V68bde']/div[@data-value='Thomas Martínez Velásquez']"
        option = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
        ActionChains(driver).move_to_element(option).click().perform()

        # Esperar a que la opción esté seleccionada (opcional, pero buena práctica)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, f"//div[@jsname='d9BH4c']/div[@data-value='Thomas Martínez Velásquez' and @aria-selected='true']")))

        time.sleep(random.uniform(0.5, 1.5))

        # Seleccionar el tipo de actividad
        actividad_xpath = ""
        if Tipo == 0:
            actividad_xpath = "//div[@aria-label='Tutoría con Cita']"
        elif Tipo == 1:
            actividad_xpath = "//div[@aria-label='Tutoría Abierta']"
        elif Tipo == 2:
            actividad_xpath = "//div[@aria-label='Taller']"
        else:
            print(f"Advertencia: Tipo de actividad desconocido para la fila {index}. Saltando.")
            continue # Saltar esta iteración si el tipo no es válido

        actividad = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, actividad_xpath))
        )
        ActionChains(driver).move_to_element(actividad).click().perform()

        time.sleep(random.uniform(0.5, 1.5))

        # Enviar el formulario
        submit_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@jsname='M2UYVd']"))
        )
        ActionChains(driver).move_to_element(submit_button).click().perform()

        # Opcionalmente, esperar el mensaje de confirmación
        try:
            confirmation = WebDriverWait(driver, 20).until( # Aumentar tiempo de espera para la confirmación
                EC.visibility_of_element_located((By.XPATH, "//div[@class='c2gzEf']/a[1]"))
            )
            print(f"Formulario {index + 1} enviado exitosamente!")
        except Exception as e:
            print(f"Error al esperar la confirmación del formulario {index + 1}: {e}")
            print(f"Falló el envío del formulario {index + 1}. Puede que necesites ajustar los selectores o los tiempos de espera.")

        # Volver al formulario para la siguiente presentación
        # Esto es crítico: si la confirmación no aparece, este botón podría no existir.
        try:
            next_form = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='c2gzEf']/a[2]"))
            )
            ActionChains(driver).move_to_element(next_form).click().perform()
        except Exception as e:
            print(f"No se pudo encontrar el botón 'Enviar otra respuesta' para la fila {index}. El formulario puede no haberse enviado o la página cambió: {e}")
            # Si no se encuentra el botón, intentamos volver a la URL del formulario original
            driver.get(form_url)
            time.sleep(random.uniform(2, 5)) # Pausa para que cargue la página

        # 10. Pausas más largas y aleatorias entre formularios
        time.sleep(random.uniform(3, 7))

    except Exception as e:
        print(f"Ocurrió un error inesperado al procesar la fila {index + 1}: {e}")
        print("Intentando continuar con la siguiente fila...")
        # En caso de error, puedes optar por recargar la página para limpiar el estado
        driver.get(form_url)
        time.sleep(random.uniform(2, 5))


print("Todos los formularios procesados.")

# Cerrar el driver
driver.quit()