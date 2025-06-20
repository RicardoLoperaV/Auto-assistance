"""
Bot_asistencias.py

thmartinezv@unal.edu.co

"""
#Bot para el envío automático de asistencias GEA - Universidad Nacional de Colombia Sede Medellín
#Por: Juan Pablo Muñoz Calderón - Tutor Geometría Vectorial y Analítica

import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Read data from Excel file   data.xlsx

data = pd.read_csv('data.csv')

# Initialize the web driver (assuming Chrome in this example)
driver = webdriver.Chrome()

# Open the Google Form
driver.get("https://docs.google.com/forms/d/e/1FAIpQLSddcCxU016sHyXP5UBuZnsNVMMs1yhNxPmpBMHNPdZCnlSRyQ/viewform")
                                                                                                          

input("Log in manually in the browser, then press Enter here to continue...")

print('aaaaaaaaaaaaaaaaaa')

# Iterate over rows in the Excel file
for index, row in data.iterrows():
    # Fill out text boxes
    Num_asignado = row["Numero"]
    Tipo = row["Tipo"]

    checkbox = driver.find_element(By.XPATH, f"//div[@aria-label='Registrar thmartinezv@unal.edu.co como el correo que se incluirá al enviar mi respuesta']")

    if checkbox.get_attribute('aria-checked') == 'false':
        checkbox.click()

    textbox = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "(//input[@type='text'])[1]"))
    )
    #textbox = driver.find_element(By.XPATH, f"//input[@aria-labelledby='i8']")
    textbox.clear()  # Clear existing text
    textbox.send_keys(str(Num_asignado))


    dropdown = driver.find_element(By.XPATH, f"//div[@jsname='wQNmvb' and @role='option']")
    driver.execute_script('arguments[0].click()', dropdown)  # Open dropdown

    option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//div[@jsname='V68bde']/div[@data-value='Thomas Martínez Velásquez']")))
    driver.execute_script('arguments[0].click()', option)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//div[@jsname='d9BH4c']/div[@data-value='Thomas Martínez Velásquez' and @aria-selected='true']")))

    time.sleep(0.1)

    if Tipo==0:
        actividad = driver.find_element(By.XPATH, f"//div[@aria-label='Tutoría con Cita']")

    elif Tipo==1:
        actividad = driver.find_element(By.XPATH, f"//div[@aria-label='Tutoría Abierta']")

    elif Tipo==2:
        actividad = driver.find_element(By.XPATH, f"//div[@aria-label='Taller']")

    driver.execute_script('arguments[0].click()', actividad)

    # Submit the form
    submit_button = driver.find_element(By.XPATH, f"//div[@jsname='M2UYVd']")
    driver.execute_script('arguments[0].click()', submit_button)

    # Optionally, wait for confirmation message
    try:
        confirmation = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//div[@class='c2gzEf']/a[1]"))
        )
        print(f"Form {index + 1} submitted successfully!")
    except:
        print(f"Failed to submit form {index + 1}.")

    # Return to form for the next submission
    next_form = driver.find_element(By.XPATH, f"//div[@class='c2gzEf']/a[2]")
    driver.execute_script('arguments[0].click()', next_form)

print("All forms submitted")

# Close the driver
driver.quit()