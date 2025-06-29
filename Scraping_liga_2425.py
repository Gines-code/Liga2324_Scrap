from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time #Esta libreria sirve para hacer acciones cada cierto tiempo
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

import os
import warnings

warnings.filterwarnings('ignore')

start_time = time.time()

####### PROYECTO PARA SACAR DATOS DE LA LIGA #######
#options = webdriver.ChromeOptions()
options = Options()
options.add_argument('--start-maximized') #Sirve para determinar el formato en que quiero que se abra
#options.headless = True
#options.binary_location = r"C:\Users\gines\Desktop\webscrap_liga\chrome-win64\chrome.exe"
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
#service = Service(r'C:/Users/Gines/Desktop/webscrap_liga/chrome-win64/chromedriver.exe')
service = Service(ChromeDriverManager().install())

#driver = webdriver.Chrome(executable_path=r'C:/Users/Gines/Desktop/webscrap_liga/chrome-win64/chromedriver.exe',options=options) #sirve para importar el driver para poder entrar a la pagina web
driver = webdriver.Chrome(service = service,options=options)

url23 = "https://www.laliga.com/es-GB/laliga-easports/resultados/2024-25/jornada-1"  #Esta es la url a la que voy a acceder
#url23 = "https://www.laliga.com/es-GB/laliga-easports/resultados/2024-25/jornada-30"
driver.get(url23)
time.sleep(3) #wait until page charges (aguanto 5 seg hasta que la web cargue)
ActionChains(driver).key_down(Keys.TAB).key_up(Keys.TAB).perform()
ActionChains(driver).key_down(Keys.TAB).key_up(Keys.TAB).perform()
ActionChains(driver).key_down(Keys.TAB).key_up(Keys.TAB).perform()
ActionChains(driver).key_down(Keys.TAB).key_up(Keys.TAB).perform()
# ActionChains(driver).key_down(Keys.TAB).key_up(Keys.TAB).perform()
time.sleep(2)
ActionChains(driver).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
time.sleep(2)
try:
    jornada_datos = os.getenv("jornada_datos", 38)
    jornada_datos = int(jornada_datos)
except:
    jornada_datos = 18
jornada_datos_str = str(jornada_datos)
ruta_datos = f'C:/Users/Gines/Desktop/webscrap_liga/datos24-25/jornada_{jornada_datos_str}/'
J=35
j_ini= 0
file_path_ej = ruta_datos + 'ejemp.csv'

os.makedirs(os.path.dirname(file_path_ej), exist_ok=True)


###1###   LEER HISTORICO DE RESULTADOS DE LA PAGINA DE LA LIGA


#Defino las listas (variables dependientes de mi DF)
fecha=list()
hora=list()
local=list()
gol_local=list()
gol_visitante=list()
visitante=list()
arbitro=list()
jornada=list()
tiempo=list()

j= j_ini + 2
J=17 #sumar 2 mas que la jornada actual
while j<(jornada_datos + 2):  #Bucle que recorre las jornadas con los resultados
    pages1=driver.find_element(By.XPATH,"//table[@class='styled__TableStyled-sc-43wy8s-1 ffaSZZ']")
    print(pages1.text)  #Texto con los resultados de todos los partidos de las jornadas X


    texto=pages1.text  #Esta en formato STR
    #print(type(texto))
    list_text=texto.split(sep='\n')  #Transformo el texto en  lista separando por saltos de línea
    #print(list_text)  #Lista con toda la información de la jornada
    list_text = [elemento for elemento in list_text if not elemento.startswith('Hist')]
    list_text = [elemento for elemento in list_text if not elemento.startswith('FECHA HORARIO')]
    list_text = [elemento for elemento in list_text if not elemento.startswith('Horario')]
    list_text = [elemento for elemento in list_text if not elemento.startswith('*Horario')]
    list_text = [elemento for elemento in list_text if not elemento.startswith('* Horario')]
    ##
    list_text = [elemento for elemento in list_text if not elemento.startswith('*')]
    #print(list_text)



    #Separo por elementos de la lista que me interesen
    N=len(list_text)
    print('longitud lista de una jornada')
    print(N)
    print(j)
    print(type(list_text))
    list_text = list(list_text)

    i=0
    while i < N:  #Bucle que recorre la lista con los resultados
        if list_text[i] == 'APLZ':
            list_text.insert(i+1, '-')
            list_text.insert(i+2,'-1')
            gol_local.append('-1')
            N=len(list_text)
        elif list_text[i] == 'VS':
            # list_text.insert(i+1, '-')
            list_text.insert(i+1,'-1')
            list_text.insert(i+1,'-1')
            gol_local.append('-1')
            N=len(list_text)
        elif i % 9==0:
            fecha.append(list_text[i])
        elif i%9==1:
            hora.append(list_text[i])
        elif i%9==2:
            local.append(list_text[i])
        elif i%9==3:
            gol_local.append(list_text[i])
        elif i%9==5:
            gol_visitante.append(list_text[i])
        elif i%9==6:
            visitante.append(list_text[i])
        elif i%9==7:
            arbitro.append(list_text[i])
            jornada.append(j-1)
        i=i+1
    print(list_text)

    # driver.find_elements(By.XPATH, "//ul[@class='styled__ItemsList-sc-d9k1bl-2 hbLeMB']")[2].click()
    print(len(driver.find_elements(By.XPATH, "//div[@class='styled__SelectedItem-sc-d9k1bl-1 bspoVB']")))
    #driver.find_elements(By.XPATH, "//p[@class='styled__TextStyled-sc-1mby3k1-0 XgneW']")[3].click()
    #driver.find_elements(By.XPATH, "//div[@class='styled__SelectedItem-sc-d9k1bl-1 bspoVB']")[0].click()
    #Clika en el banner de las jornadas
    time.sleep(2)
    

    print('longitud lista')
    print(len(driver.find_elements(By.XPATH, "//li[@class='styled__Item-sc-d9k1bl-3 eXotyy']")))
    print(j)

    #abre la jornada j
    try:
        driver.find_elements(By.XPATH, "//li[@class='styled__Item-sc-d9k1bl-3 eXotyy']")[j].click()
    except:
        print('Se acaba de recoger datos de la jornada')
    #Clika en la jornada j, para irse a esa jornada
    time.sleep(2)
    j=j+1
#print(j)

print(fecha)
print(hora)
print(local)
print(arbitro)
print(gol_local)
print(len(fecha))
print(len(hora))
print(len(local))
print(len(gol_local))
print(len(gol_visitante))
print(len(visitante))
print(len(arbitro))
print(len(jornada))

###Dataframe metiendo todos los datos de los resultados###
df_resultados= pd.DataFrame({"fecha": fecha, "hora": hora,"local":local,"visitante":visitante,"gol_local":gol_local,"gol_visitante":gol_visitante,"arbitro":arbitro,"jornada":jornada})
print(df_resultados)

# (se debe cambiar la ruta del csv!!!!!)

#función para eliminar datos de un csv
try:
    file = open(ruta_datos + "resultados.xlsx", "w")
    file.close()
    #función para meter datos a un csv
    df_resultados.to_excel(ruta_datos + 'resultados.xlsx')
except:
    #función para meter datos a un csv
    df_resultados.to_excel(ruta_datos + 'resultados.xlsx')



###2###     COGER CLASIFICACION POR JORNADA

#con esto hago click en clasificacion para irme a la pantalla de clasificacion
#driver.find_elements(By.XPATH,"//span[@class='styled__SubMenuItem-sc-1yo1ylr-1 dXSqAa']")[2].click()
element=driver.find_element(By.XPATH,"//div[@class='styled__CompetitionMenuItem-sc-7qz1ev-3 kmvAYy']")
ActionChains(driver).move_to_element(element).perform()
time.sleep(1.7)
# print(len(driver.find_elements(By.XPATH,"//p[@class='styled__TextRegularStyled-sc-1raci4c-0 pWrTZ']")))
print(len(driver.find_elements(By.XPATH,"//p[@class='styled__TextStyled-sc-1mby3k1-0 kNfrPo']")))

#Se clicka en la clasificacion
#driver.find_elements(By.XPATH,"//p[@class='styled__TextStyled-sc-1mby3k1-0 kNfrPo']")[2].click()
driver.find_elements(By.XPATH,"//a[@class='styled__SubMenuItemStyled-sc-1yo1ylr-6 ebhLYB']")[2].click()
time.sleep(2.3)

#clicko en la jornada para sacar las jornadas
print(len(driver.find_elements(By.XPATH,"//p[@class='styled__TextStyled-sc-1mby3k1-0 XgneW']")))
#driver.find_elements(By.XPATH,"//p[@class='styled__TextStyled-sc-1mby3k1-0 XgneW']")[1].click()

time.sleep(4)

# Se clicka en la jornada 1 (esta empieza en el elemento 244)
print(len(driver.find_elements(By.XPATH,"//li[@class='styled__Item-sc-d9k1bl-3 VNATM']")))
driver.find_elements(By.XPATH,"//li[@class='styled__Item-sc-d9k1bl-3 VNATM']")[244 + j_ini].click()
#cliko en la jornada 1

time.sleep(4)
####Voy a meter todos los elementos de la clasificacion en una lista####
    #Variables de interés
posicion=list()
equipo=list()
puntos=list()
jornada=list()
PG=list()
PE=list()
PP=list()
GF=list()
GC=list()
DG=list()
PJ = list()

j=j_ini
N_clasi = 15
while j < jornada_datos:
    lista_clasi=list()
    lclasi=list()
    print(j)
    clasificacion=driver.find_element(By.XPATH,"//div[@class='styled__ContentTabs-sc-7p309w-3 ghLiOY']").text
    lista_clasi=clasificacion.split(sep='\n')

    lista_clasi = [elemento for elemento in lista_clasi if not elemento.startswith('Leyenda')]
    lista_clasi = [elemento for elemento in lista_clasi if not elemento.startswith('CHAMPIONS')]
    lista_clasi = [elemento for elemento in lista_clasi if not elemento.startswith('EUROPA')]
    lista_clasi = [elemento for elemento in lista_clasi if not elemento.startswith('CONFERENCE')]
    lista_clasi = [elemento for elemento in lista_clasi if not elemento.startswith('DESCENSO')]
    lista_clasi = [elemento for elemento in lista_clasi if not elemento.startswith('RELEGATION')]
    print(lista_clasi)
    R=len(lista_clasi)
    print(R)
    r=10
    while r<R:
            if r % 10==0:
                posicion.append(lista_clasi[r])
            if r % 10==1:
                equipo.append(lista_clasi[r])
            elif r%10==2:
                puntos.append(lista_clasi[r])
            elif r%10==3:
                PJ.append(lista_clasi[r])
            elif r%10==4:
                PG.append(lista_clasi[r])
            elif r%10==5:
                PE.append(lista_clasi[r])
            elif r%10==6:
                PP.append(lista_clasi[r])
            elif r%10==7:
                GF.append(lista_clasi[r])
            elif r%10==8:
                GC.append(lista_clasi[r])
            elif r%10==9:
                DG.append(lista_clasi[r])
                jornada.append(j+1)
            r=r+1
    
    #clicka banner jornadas
    #driver.find_elements(By.XPATH,"//p[@class='styled__TextStyled-sc-1mby3k1-0 XgneW']")[3].click()
    time.sleep(1.2)
    print(driver.find_elements(By.XPATH,"//li[@class='styled__Item-sc-d9k1bl-3 VNATM']"))
    # clicka en la jornada
    if j != (N_clasi-1):
        try:
            driver.find_elements(By.XPATH,"//li[@class='styled__Item-sc-d9k1bl-3 VNATM']")[244 + j].click()
            #driver.find_elements(By.XPATH,"//li[@class='styled__Item-sc-d9k1bl-3 VNATM']")[j].click()
            time.sleep(1.1)
        except:
            print('Se acaba de recoger datos de clasificacion')

    j= j+1
print(posicion)
print(len(posicion))
print(len(equipo))
print(len(puntos))
print(len(jornada))

#Se sacan los puntos por partido jugado
puntos = [int(a) / int(b) if int(b) != 0 else 0 for a, b in zip(puntos, PJ)]
PG = [int(a) / int(b) if int(b) != 0 else 0 for a, b in zip(PG, PJ)]
PE = [int(a) / int(b) if int(b) != 0 else 0 for a, b in zip(PE, PJ)]
PP = [int(a) / int(b) if int(b) != 0 else 0 for a, b in zip(PP, PJ)]
GF = [int(a) / int(b) if int(b) != 0 else 0 for a, b in zip(GF, PJ)]
GC = [int(a) / int(b) if int(b) != 0 else 0 for a, b in zip(GC, PJ)]
DG = [int(a) / int(b) if int(b) != 0 else 0 for a, b in zip(DG, PJ)]



#Dataframe con todos los datos por jornada
df_clasi= pd.DataFrame({"posicion": posicion, "equipo": equipo,"puntos":puntos,"jornada":jornada,"PJ":PJ,"PG":PG,"PE":PE,"PP":PP,"GF":GF,"GC":GC,"DG":DG})
print(df_clasi)

try:
    #función para eliminar datos de un csv
    file = open(ruta_datos + "clasificacion.xlsx", "w")
    file.close()
    #función para meter datos a un csv
    df_clasi.to_excel(ruta_datos + 'clasificacion.xlsx')
except:
    df_clasi.to_excel(ruta_datos + 'clasificacion.xlsx')



# #Clicko en el banner para cerrar las jornadas de clasificacion#
try:
    driver.find_element(By.XPATH,"//i[@class='styled__IconRegularContainer-sc-1lapsw7-0 fVlOEb font-laliga icon-triangle_down undefined']").click()
    time.sleep(1)
except:
    time.sleep(1)


###### CLASIFIACION DE PARTIDOS SOLO EN CASA ######
driver.find_elements(By.XPATH,"//div[@class='styled__TabItem-sc-7p309w-11 hLvUaq']")[0].click()
# element=driver.find_elements(By.XPATH,"//div[@class='styled__CompetitionMenuItem-sc-7qz1ev-3 kmvAYy']")[0]
# ActionChains(driver).move_to_element(element).perform()
time.sleep(1.7)

#Pincho en partidos en casa
time.sleep(2.1)

##EMPIEZO BUCLE##
driver.find_elements(By.XPATH,"//p[@class='styled__TextStyled-sc-1mby3k1-0 XgneW']")[3].click()
#clicko en la jornada para sacar las jornadas
time.sleep(2)

j=31
print(len(driver.find_elements(By.XPATH,"//li[@class='styled__Item-sc-d9k1bl-3 VNATM']")))
driver.find_elements(By.XPATH,"//li[@class='styled__Item-sc-d9k1bl-3 VNATM']")[244 + j].click()
#cliko en la jornada 1
time.sleep(2.1)
####Voy a meter todos los elementos de la clasificacion en una lista####
    #Variables de interés
posicion=list()
equipo=list()
puntos=list()
jornada=list()
PJ = list()
PG=list()
PE=list()
PP=list()
GF=list()
GC=list()
DG=list()
j=j_ini
casa_clasi=15 #Numero de jornadas (¡¡AUTOMATIZAR!!)
while j<jornada_datos:  #Bucle con la clasificacion por jornada
    clasificacion = driver.find_element(By.XPATH,"//div[@class='styled__ContentTabs-sc-7p309w-3 ghLiOY']").text
    #clasificacion = driver.find_element(By.XPATH,"//div[@class='styled__StandingTableBody-sc-e89col-5 kIvDwR']").text
    lista_clasi=clasificacion.split(sep='\n')

    lista_clasi = [elemento for elemento in lista_clasi if not elemento.startswith('Leyenda')]
    lista_clasi = [elemento for elemento in lista_clasi if not elemento.startswith('CHAMPIONS')]
    lista_clasi = [elemento for elemento in lista_clasi if not elemento.startswith('EUROPA')]
    lista_clasi = [elemento for elemento in lista_clasi if not elemento.startswith('CONFERENCE')]
    lista_clasi = [elemento for elemento in lista_clasi if not elemento.startswith('DESCENSO')]
    lista_clasi = [elemento for elemento in lista_clasi if not elemento.startswith('RELEGATION')]
    print(lista_clasi)


    R=len(lista_clasi)
    r=10
    while r<R:
        if r % 10==0:
            posicion.append(lista_clasi[r])
        if r % 10==1:
            equipo.append(lista_clasi[r])
        elif r%10==2:
            puntos.append(lista_clasi[r])
        elif r%10==3:
            PJ.append(lista_clasi[r])
        elif r%10==4:
            PG.append(lista_clasi[r])
        elif r%10==5:
            PE.append(lista_clasi[r])
        elif r%10==6:
            PP.append(lista_clasi[r])
        elif r%10==7:
            GF.append(lista_clasi[r])
        elif r%10==8:
            GC.append(lista_clasi[r])
        elif r%10==9:
            DG.append(lista_clasi[r])
            jornada.append(j+1)
        r=r+1
    #clicka banner jornadas
    driver.find_elements(By.XPATH,"//p[@class='styled__TextStyled-sc-1mby3k1-0 XgneW']")[3].click()
    time.sleep(1.2)
    # clicka en la jornada
    if j != (casa_clasi-1):
        try:
            driver.find_elements(By.XPATH,"//li[@class='styled__Item-sc-d9k1bl-3 VNATM']")[244 + j].click()
            time.sleep(1.1)
        except:
            print('Se acaba de recoger datos de clasificacion local')
    j=j+1

#Se sacan los puntos por partido jugado
puntos = [int(a) / int(b) if int(b) != 0 else 0 for a, b in zip(puntos, PJ)]
PG = [int(a) / int(b) if int(b) != 0 else 0 for a, b in zip(PG, PJ)]
PE = [int(a) / int(b) if int(b) != 0 else 0 for a, b in zip(PE, PJ)]
PP = [int(a) / int(b) if int(b) != 0 else 0 for a, b in zip(PP, PJ)]
GF = [int(a) / int(b) if int(b) != 0 else 0 for a, b in zip(GF, PJ)]
GC = [int(a) / int(b) if int(b) != 0 else 0 for a, b in zip(GC, PJ)]
DG = [int(a) / int(b) if int(b) != 0 else 0 for a, b in zip(DG, PJ)]

#Dataframe con todos los datos por jornada
df_clasi_casa= pd.DataFrame({"posicion": posicion, "equipo": equipo,"puntos":puntos,"PJ":PJ,"jornada":jornada,"PG":PG,"PE":PE,"PP":PP,"GF":GF,"GC":GC,"DG":DG})
print(df_clasi_casa)


try:
    #función para eliminar datos de un csv
    file = open(ruta_datos + "clasi_casa.xlsx", "w")
    file.close()
    #función para meter datos a un csv
    df_clasi_casa.to_excel(ruta_datos + 'clasi_casa.xlsx')
except:
    df_clasi_casa.to_excel(ruta_datos + 'clasi_casa.xlsx')


###### CLASIFIACION DE PARTIDOS SOLO FUERA ######
#driver.find_elements(By.XPATH,"//div[@class='styled__TabItem-sc-7p309w-9 lrfIX']")[1].click()
driver.find_elements(By.XPATH,"//div[@class='styled__TabItem-sc-7p309w-11 hLvUaq']")[1].click()
#Pincho en partidos en casa
time.sleep(2)

##EMPIEZO BUCLE##
driver.find_elements(By.XPATH,"//p[@class='styled__TextStyled-sc-1mby3k1-0 XgneW']")[3].click()
#clicko en la jornada para sacar las jornadas
time.sleep(2.1)

j=31
print(len(driver.find_elements(By.XPATH,"//li[@class='styled__Item-sc-d9k1bl-3 VNATM']")))
driver.find_elements(By.XPATH,"//li[@class='styled__Item-sc-d9k1bl-3 VNATM']")[244 + j].click()
#cliko en la jornada 1
time.sleep(2.3)
####Voy a meter todos los elementos de la clasificacion en una lista####
    #Variables de interés
posicion=list()
equipo=list()
puntos=list()
jornada=list()
PJ = list()
PG=list()
PE=list()
PP=list()
GF=list()
GC=list()
DG=list()
j=j_ini
fuera_clasi=15 #Numero de jornadas (¡¡AUTOMATIZAR!!)
while j<jornada_datos:  #Bucle con la clasificacion por jornada
    clasificacion = driver.find_element(By.XPATH,"//div[@class='styled__ContentTabs-sc-7p309w-3 ghLiOY']").text
    lista_clasi=clasificacion.split(sep='\n')

    lista_clasi = [elemento for elemento in lista_clasi if not elemento.startswith('Leyenda')]
    lista_clasi = [elemento for elemento in lista_clasi if not elemento.startswith('CHAMPIONS')]
    lista_clasi = [elemento for elemento in lista_clasi if not elemento.startswith('EUROPA')]
    lista_clasi = [elemento for elemento in lista_clasi if not elemento.startswith('CONFERENCE')]
    lista_clasi = [elemento for elemento in lista_clasi if not elemento.startswith('DESCENSO')]
    lista_clasi = [elemento for elemento in lista_clasi if not elemento.startswith('RELEGATION')]
    print(lista_clasi)


    R=len(lista_clasi)
    r=10
    while r<R:
        if r % 10==0:
            posicion.append(lista_clasi[r])
        if r % 10==1:
            equipo.append(lista_clasi[r])
        elif r%10==2:
            puntos.append(lista_clasi[r])
        elif r%10==3:
            PJ.append(lista_clasi[r])
        elif r%10==4:
            PG.append(lista_clasi[r])
        elif r%10==5:
            PE.append(lista_clasi[r])
        elif r%10==6:
            PP.append(lista_clasi[r])
        elif r%10==7:
            GF.append(lista_clasi[r])
        elif r%10==8:
            GC.append(lista_clasi[r])
        elif r%10==9:
            DG.append(lista_clasi[r])
            jornada.append(j+1)
        r=r+1
    #clicka banner jornadas
    driver.find_elements(By.XPATH,"//p[@class='styled__TextStyled-sc-1mby3k1-0 XgneW']")[3].click()
    time.sleep(1.2)
    # clicka en la jornada
    if j != (casa_clasi-1):
        try:
            driver.find_elements(By.XPATH,"//li[@class='styled__Item-sc-d9k1bl-3 VNATM']")[244 + j].click()
            time.sleep(1.1)
        except:
            print('Se acaba de recoger datos de clasificacion fuera')
    j=j+1

#Se sacan los puntos por partido jugado
puntos = [int(a) / int(b) if int(b) != 0 else 0 for a, b in zip(puntos, PJ)]
PG = [int(a) / int(b) if int(b) != 0 else 0 for a, b in zip(PG, PJ)]
PE = [int(a) / int(b) if int(b) != 0 else 0 for a, b in zip(PE, PJ)]
PP = [int(a) / int(b) if int(b) != 0 else 0 for a, b in zip(PP, PJ)]
GF = [int(a) / int(b) if int(b) != 0 else 0 for a, b in zip(GF, PJ)]
GC = [int(a) / int(b) if int(b) != 0 else 0 for a, b in zip(GC, PJ)]
DG = [int(a) / int(b) if int(b) != 0 else 0 for a, b in zip(DG, PJ)]

#Dataframe con todos los datos por jornada
df_clasi_fuera= pd.DataFrame({"posicion": posicion, "equipo": equipo,"puntos":puntos,"PJ":PJ,"jornada":jornada,"PG":PG,"PE":PE,"PP":PP,"GF":GF,"GC":GC,"DG":DG})
print(df_clasi_fuera)


try:
    #función para eliminar datos de un csv
    file = open(ruta_datos + "clasi_fuera.xlsx", "w")
    file.close()
    #función para meter datos a un csv
    df_clasi_casa.to_excel(ruta_datos + 'clasi_fuera.xlsx')
except:
    df_clasi_casa.to_excel(ruta_datos + 'clasi_fuera.xlsx')



end_time = time.time()

# tiempo de ejecucion
execution_time = end_time - start_time
print(f"Tiempo de ejecución: {execution_time} segundos")


"""
#####PARTIDOS FUERA DE CASA######

driver.find_element(By.XPATH,"//ul[@class='styled__ListTabs-bcjnby-2 jRIEjJ']/li[3]").click()
#Pincho en partidos fuera de casa
time.sleep(4)

driver.find_elements(By.XPATH,"//div[@class='styled__SelectedItem-d9k1bl-1 iLBmRg']")[0].click()
#clicko en la jornada para sacar las jornadas
time.sleep(4)

driver.find_elements(By.XPATH,"//li[@class='styled__Item-d9k1bl-3 idoxA']")[0].click()
#cliko en la jornada 1
time.sleep(4)
####Voy a meter todos los elementos de la clasificacion en una lista####
    #Variables de interés
posicion=list()
equipo=list()
puntos=list()
jornada=list()
PG=list()
PE=list()
PP=list()
GF=list()
GC=list()
DG=list()
j=0
#J=33 #Numero de jornadas (¡¡AUTOMATIZAR!!)
while j<J-1:  #Bucle con la clasificacion por jornada
    lista_clasi=list()
    lclasi=list()

    E=20  #Numero de equipos
    e=0
    while e<E:
        clasificacion=driver.find_elements(By.XPATH,"//div[@class='styled__ContainerAccordion-e89col-11 HquGF']")[e].text
        #Distinto al anterior ya que ahora clasificacion es una lista.
        lclasi=clasificacion.split(sep='\n')
        lista_clasi=lista_clasi+lclasi
        e=e+1
    #print(lista_clasi)



    R=len(lista_clasi)
    r=0
    while r<R:
        if r % 10==0:
            posicion.append(lista_clasi[r])
        if r % 10==1:
            equipo.append(lista_clasi[r])
        elif r%10==2:
            puntos.append(lista_clasi[r])
        elif r%10==3:
            jornada.append(lista_clasi[r])
        elif r%10==4:
            PG.append(lista_clasi[r])
        elif r%10==5:
            PE.append(lista_clasi[r])
        elif r%10==6:
            PP.append(lista_clasi[r])
        elif r%10==7:
            GF.append(lista_clasi[r])
        elif r%10==8:
            GC.append(lista_clasi[r])
        elif r%10==9:
            DG.append(lista_clasi[r])
        r=r+1
    driver.find_elements(By.XPATH,"//div[@class='styled__SelectedItem-d9k1bl-1 iLBmRg']")[0].click()
    #clicko en la jornada para sacar las jornadas
    time.sleep(2)

    driver.find_elements(By.XPATH,"//li[@class='styled__Item-d9k1bl-3 idoxA']")[j].click()
    time.sleep(2)
    j=j+1
lista_clasi=list()
lclasi=list()

E=20  #Numero de equipos
e=0
while e<E:
        clasificacion=driver.find_elements(By.XPATH,"//div[@class='styled__ContainerAccordion-e89col-11 HquGF']")[e].text
        #Distinto al anterior ya que ahora clasificacion es una lista.
        lclasi=clasificacion.split(sep='\n')
        lista_clasi=lista_clasi+lclasi
        e=e+1
#print(lista_clasi)



R=len(lista_clasi)
r=0
while r<R:
        if r % 10==0:
            posicion.append(lista_clasi[r])
        if r % 10==1:
            equipo.append(lista_clasi[r])
        elif r%10==2:
            puntos.append(lista_clasi[r])
        elif r%10==3:
            jornada.append(lista_clasi[r])
        elif r%10==4:
            PG.append(lista_clasi[r])
        elif r%10==5:
            PE.append(lista_clasi[r])
        elif r%10==6:
            PP.append(lista_clasi[r])
        elif r%10==7:
            GF.append(lista_clasi[r])
        elif r%10==8:
            GC.append(lista_clasi[r])
        elif r%10==9:
            DG.append(lista_clasi[r])
        r=r+1

#Dataframe con todos los datos por jornada
df_clasi_fuera= pd.DataFrame({"posicion": posicion, "equipo": equipo,"puntos":puntos,"jornada":jornada,"PG":PG,"PE":PE,"PP":PP,"GF":GF,"GC":GC,"DG":DG})
print(df_clasi_fuera)



#función para eliminar datos de un csv
file = open("clasi_fuera.xlsx", "w")
file.close()
#función para meter datos a un csv
df_clasi_fuera.to_excel('clasi_fuera.xlsx')



                ##### COJO MAS ESTADISTICAS #####

#Pincho en estadisticas
driver.find_element(By.XPATH,"//div[@class='styled__OtherLinksMenuItem-kjni92-2 frNOcH'][3]/a[@class='link']").click()
time.sleep(4)


## GOLEADORES ##

#Hacer bucle con todas las pag.

#String con los goleadores
goleadores_str=driver.find_element(By.XPATH,"//table[@class='styled__TableStyled-sc-57jgok-1 bgbrFU']")

#lo transformo a lista
goleadores_lista=list()
goleadores_lista=goleadores_str.text.split(sep='\n')

#bucle para hacer listas de las caracteristicas de los goleadores
puesto=list()
jugador=list()
equipo_jugador=list()
n_goles=list()
partidos_jugados=list()
porcentaje=list()
g=5 #Empiezo en 5 ya que lo primero es header
while g<len(goleadores_lista):
    if g%6==5:
        puesto.append(goleadores_lista[g])
    elif g%6==0:
        jugador.append(goleadores_lista[g])
    elif g%6==1:
        equipo_jugador.append(goleadores_lista[g])
    elif g%6==2:
        n_goles.append(goleadores_lista[g])
    elif g%6==3:
        partidos_jugados.append(goleadores_lista[g])
    elif g%6==4:
        porcentaje.append(goleadores_lista[g])
    g=g+1


df_goleadores=pd.DataFrame({"puesto":puesto,"jugador":jugador,"equipo":equipo_jugador,"goles":n_goles,"partidos_jugados":partidos_jugados,"porcentaje":porcentaje})
print(df_goleadores)

#función para eliminar datos de un csv
file = open("goleadores.xlsx", "w")
file.close()
#función para meter datos a un csv
df_clasi_fuera.to_excel('goleadores.xlsx')

##Amarillas
driver.find_element(By.XPATH,"//a[@class='styled__TabItem-bzzga5-8 fUIqCp'][1]").click()
time.sleep(4)
Amarillas=driver.find_element(By.XPATH,"//table[@class='styled__TableStyled-sc-57jgok-1 bgbrFU']").text


Amarilla_lista=list()
Amarilla_lista=Amarillas.split(sep='\n')

puesto=list()
jugador=list()
equipo_jugador=list()
n_tarjetas=list()
g=3#Empiezo en 3 ya que lo primero es header
while g<len(Amarilla_lista):
    if g%4==3:
        puesto.append(Amarilla_lista[g])
    elif g%4==0:
        jugador.append(Amarilla_lista[g])
    elif g%4==1:
        equipo_jugador.append(Amarilla_lista[g])
    elif g%4==2:
        n_tarjetas.append(Amarilla_lista[g])
    g=g+1

df_amarilla=pd.DataFrame({"puesto":puesto,"jugador":jugador,"equipo":equipo_jugador,"n_tarjetas":n_tarjetas})
print(df_amarilla)

#función para eliminar datos de un csv
file = open("amarillas.xlsx", "w")
file.close()
#función para meter datos a un csv
df_clasi_fuera.to_excel('amarillas.xlsx')


##ROJAS
driver.find_element(By.XPATH,"//a[@class='styled__TabItem-bzzga5-8 fUIqCp'][2]").click()
time.sleep(4)
Rojas=driver.find_element(By.XPATH,"//table[@class='styled__TableStyled-sc-57jgok-1 bgbrFU']").text


rojas_lista=list()
rojas_lista=Rojas.split(sep='\n')

puesto=list()
jugador=list()
equipo_jugador=list()
n_tarjetas=list()
g=3#Empiezo en 3 ya que lo primero es header
while g<len(Amarilla_lista):
    if g%4==3:
        puesto.append(rojas_lista[g])
    elif g%4==0:
        jugador.append(rojas_lista[g])
    elif g%4==1:
        equipo_jugador.append(rojas_lista[g])
    elif g%4==2:
        n_tarjetas.append(rojas_lista[g])
    g=g+1

df_rojas=pd.DataFrame({"puesto":puesto,"jugador":jugador,"equipo":equipo_jugador,"n_tarjetas":n_tarjetas})
print(df_rojas)

#función para eliminar datos de un csv
file = open("rojas.xlsx", "w")
file.close()
#función para meter datos a un csv
df_clasi_fuera.to_excel('rojas.xlsx')


##ASISTENCIAS

driver.find_element(By.XPATH,"//a[@class='styled__TabItem-bzzga5-8 fUIqCp'][3]").click()
time.sleep(4)

asistentes=driver.find_element(By.XPATH,"//table[@class='styled__TableStyled-sc-57jgok-1 bgbrFU']").text

#lo transformo a lista
asist_lista=list()
asist_lista=asistentes.split(sep='\n')

#bucle para hacer listas de las caracteristicas de los goleadores
puesto=list()
jugador=list()
equipo_jugador=list()
n_asist=list()
partidos_jugados=list()
porcentaje=list()
g=5 #Empiezo en 5 ya que lo primero es header
while g<len(asist_lista):
    if g%6==5:
        puesto.append(asist_lista[g])
    elif g%6==0:
        jugador.append(asist_lista[g])
    elif g%6==1:
        equipo_jugador.append(asist_lista[g])
    elif g%6==2:
        n_asist.append(asist_lista[g])
    elif g%6==3:
        partidos_jugados.append(asist_lista[g])
    elif g%6==4:
        porcentaje.append(asist_lista[g])
    g=g+1

df_asist=pd.DataFrame({"puesto":puesto,"jugador":jugador,"equipo":equipo_jugador,"asistencias":n_asist,"partidos_jugados":partidos_jugados,"porcentaje":porcentaje})
print(df_asist)

#función para eliminar datos de un csv
file = open("asistencias.xlsx", "w")
file.close()
#función para meter datos a un csv
df_clasi_fuera.to_excel('asistencias.xlsx')


## PASES ##
driver.find_element(By.XPATH,"//a[@class='styled__TabItem-bzzga5-8 fUIqCp'][4]").click()
time.sleep(4)

pases=driver.find_element(By.XPATH,"//table[@class='styled__TableStyled-sc-57jgok-1 bgbrFU']").text

#lo transformo a lista
pases_lista=list()
pases_lista=pases.split(sep='\n')

#bucle para hacer listas de las caracteristicas de los goleadores
puesto=list()
jugador=list()
equipo_jugador=list()
pases_buenos=list()
pases_totales=list()
g=4 #Empiezo en 5 ya que lo primero es header
while g<len(pases_lista):
    if g%5==4:
        puesto.append(pases_lista[g])
    elif g%5==0:
        jugador.append(pases_lista[g])
    elif g%5==1:
        equipo_jugador.append(pases_lista[g])
    elif g%5==2:
        pases_buenos.append(pases_lista[g])
    elif g%5==3:
        pases_totales.append(pases_lista[g])
    g=g+1



df_pases=pd.DataFrame({"puesto":puesto,"jugador":jugador,"equipo":equipo_jugador,"pases_buenos":pases_buenos,"pases_totales":pases_totales})
print(df_pases)

#función para eliminar datos de un csv
file = open("pases.xlsx", "w")
file.close()
#función para meter datos a un csv
df_clasi_fuera.to_excel('pases.xlsx')


##PARADAS
driver.find_element(By.XPATH,"//a[@class='styled__TabItem-bzzga5-8 fUIqCp'][5]").click()
time.sleep(4)
paradas=driver.find_element(By.XPATH,"//table[@class='styled__TableStyled-sc-57jgok-1 bgbrFU']").text

paradas_lista=list()
paradas_lista=paradas.split(sep='\n')

puesto=list()
jugador=list()
equipo_jugador=list()
n_paradas=list()
partidos_jugados=list()
porcentaje=list()
g=5 #Empiezo en 5 ya que lo primero es header
while g<len(paradas_lista):
    if g%6==5:
        puesto.append(paradas_lista[g])
    elif g%6==0:
        jugador.append(paradas_lista[g])
    elif g%6==1:
        equipo_jugador.append(paradas_lista[g])
    elif g%6==2:
        n_paradas.append(paradas_lista[g])
    elif g%6==3:
        partidos_jugados.append(paradas_lista[g])
    elif g%6==4:
        porcentaje.append(paradas_lista[g])
    g=g+1

df_paradas=pd.DataFrame({"puesto":puesto,"jugador":jugador,"equipo":equipo_jugador,"paradas":n_paradas,"partidos_jugados":partidos_jugados,"porcentaje":porcentaje})
print(df_paradas)

#función para eliminar datos de un csv
file = open("paradas.xlsx", "w")
file.close()
#función para meter datos a un csv
df_clasi_fuera.to_excel('paradas.xlsx')


## EQUIPOS ##
driver.find_element(By.XPATH,"//a[@class='styled__TabItem-bzzga5-8 fUIqCp'][6]").click()
time.sleep(5)
equipos=driver.find_element(By.XPATH,"//table[@class='styled__TableStyled-sc-57jgok-1 bgbrFU']").text

equipos_lista=list()
equipos_lista=equipos.split(sep='\n')

puesto=list()
equipo=list()
GF=list()
GC=list()
Disparos_puerta=list()
faltas=list()
amarillas_total=list()
rojas_total=list()
g=7 #Empiezo en 7 ya que lo primero es header
while g<len(equipos_lista):
    if g%8==7:
        puesto.append(equipos_lista[g])
    elif g%8==0:
        equipo.append(equipos_lista[g])
    elif g%8==1:
        GF.append(equipos_lista[g])
    elif g%8==2:
        GC.append(equipos_lista[g])
    elif g%8==3:
        Disparos_puerta.append(equipos_lista[g])
    elif g%8==4:
        faltas.append(equipos_lista[g])
    elif g%8==5:
        amarillas_total.append(equipos_lista[g])
    elif g%8==6:
        rojas_total.append(equipos_lista[g])
    g=g+1


df_equipos=pd.DataFrame({"puesto":puesto,"equipo":equipo,"GF":GF,"GC":GC,"Disparos":Disparos_puerta,"faltas":faltas,"amarillas":amarillas_total,"rojas":rojas_total})
print(df_equipos)

#función para eliminar datos de un csv
file = open("equipos.xlsx", "w")
file.close()
#función para meter datos a un csv
df_clasi_fuera.to_excel('equipos.xlsx')


##HE EMPEZADO EN OTRO SCRIPT##
"""


"""
#SIGUIENTE PASO, AMPLIAR DF. COGER MAS INFO DE LA PAGINA DE LA LIGA

#clicko en un elemento para que carga mas info (amarillas y demas)
driver.find_element(By.XPATH,"//i[@class='styled__IconRegularContainer-sc-1lapsw7-0 eVvDDH font-laliga icon-Flecha-abajo undefined']").click()
time.sleep(2)

#tabla con amarillas y demas
mas_inf=driver.find_element(By.XPATH,"//div[@class='styled__ContainerEvents-ux8vhl-0 kEqdGq']")
print(mas_inf.text)

#Tengo el problema de que solo selecciona el minuto y jugador de la accion; no si es una amarilla o gol...
    #¿Merece la pena solucionar? ---> no viene demasiada info aqui, alomejor coger otras estadisticas
"""