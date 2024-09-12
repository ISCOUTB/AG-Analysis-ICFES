import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import os

# Función para procesar un lote de datos
def procesar_lote(lote):
    print(lote.describe())  
    return lote

# Función para leer el archivo CSV y procesarlo en múltiples hilos
def procesar_csv_multihilo():

    csv_file = "Results11.csv"
    
    # Tamaño de cada lote de filas
    chunksize = 100000

    # Determinar el número de hilos en función de los núcleos disponibles (depende del equipo que ejecuta)
    num_threads = os.cpu_count()

    # Leer el CSV en lotes
    data_iter = pd.read_csv(csv_file, chunksize=chunksize)
    
    # Procesar los lotes en paralelo
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(procesar_lote, data_iter)

if __name__ == "__main__":
    procesar_csv_multihilo()
