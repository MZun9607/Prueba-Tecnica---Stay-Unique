from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from pandas import to_datetime

#Iniciamos con el proceso de extraccion de la informacion, leemos los archivos .csv
bookings = read_csv("Bookings.csv")
properties = read_csv("Properties.csv")

#Realizamos limpieza y transformacion de datos, nos enfocaremos en los datos de Airbnb
#Eliminamos informacion con campos vacios, irreales o que no utilicemos y estandarizamos valores. 
#Guardamos la informacion en nuevos Dataframe y exportamos a .csv
bookingsClean = bookings.dropna(inplace=False)
propertiesClean = properties.dropna(inplace=False)

bookingsClean = bookingsClean[bookingsClean['Channel'] == "Airbnb"]
bookingsClean = bookingsClean[bookingsClean['RoomRate'] != 0]
bookingsClean = bookingsClean[bookingsClean['NumNights'] != 0]
bookingsClean = bookingsClean[bookingsClean['Revenue'] != 0]
bookingsClean = bookingsClean[bookingsClean['TotalPaid'] != 0]
bookingsClean['BookingCreatedDate'] = to_datetime(bookingsClean['BookingCreatedDate'], format='mixed', dayfirst=True).dt.strftime('%d/%m/%Y')
bookingsClean['ArrivalDate'] = to_datetime(bookingsClean['ArrivalDate'], format='mixed', dayfirst=True).dt.strftime('%d/%m/%Y')
bookingsClean['DepartureDate'] = to_datetime(bookingsClean['DepartureDate'], format='mixed', dayfirst=True).dt.strftime('%d/%m/%Y')

propertiesClean = propertiesClean[propertiesClean['RealProperty']== "Yes"]
propertiesClean = propertiesClean[propertiesClean['NumBedrooms']!= 0]
propertiesClean = propertiesClean[propertiesClean['Square']!= 0]
propertiesClean = propertiesClean[propertiesClean['Capacity']!= 0]
propertiesClean.loc[propertiesClean['PropertyType']=="Apa", 'PropertyType'] = "Apartment"
propertiesClean['ReadyDate'] = to_datetime(propertiesClean['ReadyDate'], format='mixed', dayfirst=True).dt.strftime('%d/%m/%Y')

bookingsClean.to_csv('Bookings_Clean.csv', index=False)
propertiesClean.to_csv('PropertiesClean.csv', index=False)

#Inicializamos una nueva lista de propiedades para la exportacion
propertiesList = DataFrame()

#Realizamos el siguiente calculo para obtener el precio por noche de cada reservacion realizada
bookingsClean['PaidPerNight'] = bookingsClean['RoomRate'] / bookingsClean['NumNights']

#Con el precio por noche, calculamos en promedio el coste por noche de cada propiedad. La anadimos a la tabla de propiedades para comparar.
for index, prop in propertiesClean.iterrows():
    bookingFromProp = bookingsClean[bookingsClean['PropertyId'] == prop['PropertyId']]
    if not bookingFromProp.empty:  #Comprobamos si hay resultados
        propertyMean = DataFrame([prop])
        propertyMean['MeanPerNight'] = round(bookingFromProp['PaidPerNight'].mean(),2)
        propertiesList = concat([propertiesList, propertyMean], ignore_index=True)

#Exportamos la informacion a .csv
propertiesList.to_csv('Propiedades_Costo_Por_Noche.csv', index=False)
