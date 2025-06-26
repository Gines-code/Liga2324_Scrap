import os
import subprocess

for jornada in ['30','31']:
    # Configurar variables de entorno
    os.environ["jornada_datos"] = jornada

    # Ejecutar el script
    subprocess.run(["python", "C:/Users/Gines/Desktop/webscrap_liga/Scraping_liga_2425.py"])
    print("Scraping finalizado")

    # Ejecutar el notebook
    subprocess.run(["python", "C:/Users/Gines/Desktop/webscrap_liga/sql_liga24-25.py"])
    print("SQL finalizado")
