# Extracción de datos de compras de woocommerce

Este script lo único que hace es unir los datos de tu ecommerce en WP para tener en una hoja las compras realizadas en WooCommerce para poder hacer luego un dashboard por ejemplo en Looker Studio y tener un seguimiento.
Sería bueno marcar un Cron en el PC para que se actualizara de manear automática cada día, cada hora... depende ahí de los movimientos que tenga la web y la importancia de tener los datos actualizados en cada momento.


## Librerías a utilizar

Tenemos varias librearías internas de Python y otras tantas que debemos  importarlas como son:
* collections con Counter y defaultdict
* os

Las externas a python pero dentro del abanico
* pandas
* requests
* dotenv

Las que son externas y están preparadas para el universo de Google
* google.oauth2.service_account
* gspread

Hemos utilizado *dotenv* para que de esta manera no haga falta hacer público los datos que veamos más intenerantes a tener ocultos, como pueden ser la URL de la API de woocommerce por ejemplo.


## Datos introducidos en dotenv

Los datos que hemos introducido en este caso:
* URL: es donde está la URL de la API de woocommerce
* SPREADSHEETS_ID: Id de la hoja de Spreadsheet
* WORKSHEET_NAME: Hoja de Spreadsheet que estamos utilizando, por ejemplo 'Hoja 1'
* CREDS_FILE: Nombre del archivo para los tokens de petición a Google de Google Sheets 

## Instalación de librerías

Para instalar la librerías únicamente necesitas hacer ```pip install -r requirements.txt``` y se instalarán todas las librerías necesarias.


### Consejo

Es aconsejable crear un entorno virtual para hacer estas tareas.
También sería aconsjable la creación de un cron para poder hacer estas peticiones de manera automática en el tiempo o bien utilizar las **actions** de GitHub para hacerlo de manera automática.

```pip install -m venv (nombre del entorno virtual)```