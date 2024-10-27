#Importamos las librerias necesarias (time, selenium, pandas, webdriver)
from time import sleep  

from selenium import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

from pandas import DataFrame


#Ingresamos los siguientes argumentos al webdriver para evitar que se nos detecte como un bot
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=opts
)

#Inicializamos variables
webPath = 'https://www.airbnb.com/'
location = 'Barcelona, España'
itemHeader = ["Tipo de alojamiento", "Localidad", "Descripcion", "Precio (S/)", "Calificacion", "Cantidad de Resenas"]
itemList = []
#itemList.append(itemHeader)

#Cargamos la web, luego esperamos a que carguen los elementos de la pagina
driver.get(webPath)
sleep(2) 

#Guardamos la instancia de la pestana original, esto nos permitira regresar al momento de abrir pestanas adicionales en caso se requiera.
originalTab = driver.window_handles[0]

#Obtenemos los items necesarios para la busqueda principal que son la barra de busqueda y el boton de busqueda.
searchBar = driver.find_element(By.ID, 'bigsearch-query-location-input')
searchButton = driver.find_element(By.XPATH, '//button[@data-testid="structured-search-input-search-button"]')

#Realizamos la busqueda de estadias en Barcelona. Esperamos a que carguen los items.
searchBar.send_keys(location)
sleep(1)
searchButton.click()
sleep(4)

#Obtenemos el boton siguiente, que permite cargar el proximo grupo de alojamientos
nextButton = driver.find_elements(By.CLASS_NAME, 'atm_26_zbnr2t_9xuho3')[1]

#Por cada pagina realizaremos las siguientes instrucciones, acotando los resultados a al menos 100
while len(itemList)<100:
    #Obtenemos todos los alojamientos en la pagina actual
    spaces = driver.find_elements(By.XPATH, '//div[@data-testid="card-container"]')

    #Por cada alojamiento realizaremos las siguientes instrucciones
    for space in spaces:
        try:
            #Buscamos el titulo del anuncio
            cardTitle = space.find_element(By.XPATH, './/div[@data-testid="listing-card-title"]')

            #Debido a que el contenedor padre no tiene un ID por el que obtenerlo directamente, lo hacemos a traves del titulo
            dataCard = cardTitle.find_element(By.XPATH, "..")

            #Obtenemos los contenedores necesarios
            cardSubtitles = dataCard.find_elements(By.XPATH, './/div[@data-testid="listing-card-subtitle"]')
            cardPrice = dataCard.find_element(By.XPATH, './/div[@data-testid="price-availability-row"]').find_element(By.CLASS_NAME, "_11jcbg2")
            cardRating = dataCard.find_element(By.CLASS_NAME, "r4a59j5")

            #Obtenemos la informacion
            typeOfSpace = cardTitle.text.split(" en ",1)[0]                                 #Tipo de alojamiento
            location = cardTitle.text.split(" en ",1)[1]                                    #Sitio
            subtitle = cardSubtitles[0].text.splitlines()[0]                                #Descripcion
            price = cardPrice.text.replace("S/","").replace(" ","")                         #Precio
            rate = cardRating.text.splitlines()[1].split(" (")[0]                           #Calificacion
            reviewsCount = cardRating.text.splitlines()[1].split(" (")[1].split(")")[0]     #Cantidad de resenas

            #Unificamos en un objeto
            itemData = [typeOfSpace, location, subtitle, price, rate, reviewsCount]

            #Validamos los datos y agregamos a la lista a exportar
            if (typeOfSpace == ''):
                pass
            elif (location != 'Barcelona'):
                pass
            elif (subtitle == ''):
                pass
            elif (price == 0 or price == '') :
                pass
            elif (rate == 0 or rate == '') :
                pass
            elif (reviewsCount == 0 or reviewsCount == '') :
                pass
            else:
                itemList.append(itemData)
        except Exception: 
            pass
    
    #Cargamos el siguiente grupo de alojamientos
    nextButton.click()
    sleep(3)

#Cerramos el Web Driver
driver.quit()

#Agregamos los datos a un DataFrame
itemListDF = DataFrame(itemList, columns=itemHeader)

#Exportamos la informacion a .csv
itemListDF.to_csv('Lista_de_Alojamientos_Barcelona.csv', index=False)


