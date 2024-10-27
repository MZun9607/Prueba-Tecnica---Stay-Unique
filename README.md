# Prueba-Tecnica---Stay-Unique

## Descripción
En este proyecto se incluyen los scripts para realizar el proceso de scraping y de limpieza de datos solicitados por la prueba, así como los archivos generados.

## Estructura del Proyecto
1. Scraping de Datos
2. Procesos de ETL y EDA
3. Consolidación de Datos

## Instrucciones de Configuración
1. Clona el repositorio:
   ```sh
   git clone https://github.com/

2. Instala las dependencias:
   pip install selenium
   pip install webdriver-manager
   pip install pandas

## Ejecución de scripts
1. python airbnb.py
2. python ETL_EDA.py

## Limpieza de datos
1. Filtrado: Se eliminaron filas con valores nulos.
2. Transformación: Se estandarizaron las propiedades y formatos de fecha.

## Pipeline
1. Extracción: Obtención de datos desde scraping de la página Airbnb y archivos .csv
2. Transformación: Limpieza y normalización de datos. Cálculo de monto por noche (Booking) y monto por noche promedio (Properties).
3. Carga: Consolidación de los datos limpios en archivos .csv

## Retos o problemas encontrados
1. Manejo de ids y clases en el scraping:
   Durante la inspección de los objetos de la web de Airbnb, se observó que muchos elementos importantes no contaban con "id", por lo que se tuvo que trabajar con XPATH y en algunos casos, con clases e identificar el elemento desde una lista.
2. Integración de datos: Se encontraron diferencias en los formatos de datos que fueron resueltas mediante transformaciones personalizadas.

## Archivos finales
1. Lista_de_Alojamientos_Barcelona.csv : Archivo con datos obtenidos del scraping.
2. PropertiesClean.csv : Archivo con información limpia de propiedades.
3. Bookings_Clean.csv : Archivo con información limpia de reservas.
4. Propiedades_Costo_Por_Noche.csv : Archivo con promedio de costo por noche por propiedad.
