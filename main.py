from collections import Counter, defaultdict
import os

import pandas as pd
import requests
from dotenv import load_dotenv

from google.oauth2.service_account import Credentials
import gspread

load_dotenv()

def get_data_from_url(url: str) -> dict:
    """Realiza la solicitud GET y defvuelve los datos JSON si es tiene éxito

    Args:
        url (str): URL de donde vamos a extraer la información
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error al obtener los datos: {response.status_code}  - {response.text}")
    
def process_data(data: dict) -> pd.DataFrame:
    """Procesa los datos JSON y devuelve un DataFrame listo para escribir en GSheets."""
    contador_productos = Counter()
    nombres_productos = {}
    suma_precios = defaultdict(float)

    for entry in data.get('datos', []):
        if entry:  # Ignorar entradas vacías
            producto_id = entry['producto']
            nombre_producto = entry['nombre']
            precio_producto = float(entry['precio'])

            contador_productos[producto_id] += 1
            nombres_productos[producto_id] = nombre_producto
            suma_precios[producto_id] += precio_producto

    #Crear lista de diccionarios para el DataFrame
    resultados = [
        {
            'Producto ID': producto_id,
            'Nombre': nombres_productos[producto_id],
            'Cantidad de Pedidos': cantidad,
            'Total Precio': suma_precios[producto_id]
        }
        for producto_id, cantidad in contador_productos.items()
    ]

    return pd.DataFrame(resultados)

def update_google_sheets(df: pd.DataFrame, sheet_id: str, worksheet_name: str, creds_file: str) -> None:
    """Actualiza una hoja de Google Sheets con un DataFrame"""
    SCOPES=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
                ]

    creds = Credentials.from_service_account_file(
        creds_file,
        scopes=SCOPES,
        )

    client = gspread.authorize(creds)

    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.worksheet(worksheet_name)

    #Borrar el contenido de la hoja
    worksheet.clear()

    #Escribir los datos en la hoja de cálculo
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

    print("Datos en Gsheet actualizados")

if __name__ == "__main__":
    #Configuración:
    URL=os.getenv("URL")
    SPREADSHEETS_ID=os.getenv("SPREADSHEETS_ID")
    WORKSHEET_NAME=os.getenv("WORKSHEET_NAME")
    CREDS_FILE=os.getenv("CREDS_FILE")

    #Flujo de trabajo principal
    try:
        data=get_data_from_url(URL)
        df=process_data(data)
        update_google_sheets(df,SPREADSHEETS_ID,WORKSHEET_NAME,CREDS_FILE)
    except Exception as e:
        print(f"Algo no marcha bien, error: {e}")
