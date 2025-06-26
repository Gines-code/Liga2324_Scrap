import sys
print(sys.executable)



# ### Imports
import pandas as pd
import pandasql as ps
import os
notebook_path = os.getcwd()
print(notebook_path)

def modif_jornada_mas1(df):
    """
    Modifica la variable jornada_datos sumando 1.
    """
    df['jornada'] = df['jornada'] + 1
    return df

try:
    jornada_datos = os.getenv("jornada_datos", 2)
except:
    jornada_datos = '18'

# ## 1- Lectura del fichero

#jornada_datos = '16'
ruta = f'C:/Users/Gines/Desktop/webscrap_liga/datos24-25/jornada_{jornada_datos}/'


# Lectura del fichero de Resultados
ruta_excel_resultados = ruta + "resultados.xlsx"
df_pd_resultados = pd.read_excel(ruta_excel_resultados)


# Lectura del fichero de Clasificacion
ruta_excel_clasificacion = ruta + "clasificacion.xlsx"
df_pd_clasificacion = pd.read_excel(ruta_excel_clasificacion)
df_clasificacion_1 = df_pd_clasificacion
df_clasificacion_1 = modif_jornada_mas1(df_clasificacion_1)



# Lectura del fichero Clasi_casa
ruta_excel_clasi_casa = ruta + "clasi_casa.xlsx"
df_pd_clasiCasa = pd.read_excel(ruta_excel_clasi_casa)
df_pd_clasiCasa = modif_jornada_mas1(df_pd_clasiCasa)


# Lectura del fichero Clasi_fuera
ruta_excel_clasi_fuera = ruta + "clasi_fuera.xlsx"
df_pd_clasiFuera = pd.read_excel(ruta_excel_clasi_fuera)
df_pd_clasiFuera = modif_jornada_mas1(df_pd_clasiFuera)



# # 2- Union de los dataframes
result = df_pd_resultados
clasi = df_pd_clasificacion
clasi_1 = df_clasificacion_1
clasi_casa = df_pd_clasiCasa
clasi_casa1 = df_pd_clasiCasa
clasi_fuera = df_pd_clasiFuera
clasi_fuera1 = df_pd_clasiFuera


query = """
    SELECT R.fecha, R.hora, R.local, R.visitante, R.gol_local, R.gol_visitante, R.arbitro, R.jornada, C.posicion as pos_local, C.puntos as pts_local, C.PJ as PJ_local, C.PG as PG_local, C.PE as PE_local, C.PP as PP_local, C.GF as GF_local, C.GC as GC_local, C.DG as DG_local, C1.posicion as pos_visi, C1.puntos as pts_visi, C1.PJ as PJ_visi, C1.PG as PG_visi, C1.PE as PE_visi, C1.PP as PP_visi, C1.GF as GF_visi, C1.GC as GC_visi, C1.DG as DG_visi, casa.posicion as pos_loc_C, casa.puntos as pts_loc_C, casa.PJ as PJ_loc_C, casa.PG as PG_loc_C, casa.PE as PE_loc_C, casa.PP as PP_loc_C, casa.GF as GF_loc_C, casa.GC as GC_loc_C, casa.DG as DG_loc_C, fuera.posicion as pos_loc_F, fuera.puntos as pts_loc_F, fuera.PJ as PJ_loc_F, fuera.PG as PG_loc_F, fuera.PE as PE_loc_F, fuera.PP as PP_loc_F, fuera.GF as GF_loc_F, fuera.GC as GC_loc_F, fuera.DG as DG_loc_F, casa1.posicion as pos_vis_C, casa1.puntos as pts_vis_C, casa1.PJ as PJ_vis_C, casa1.PG as PG_vis_C, casa1.PE as PE_vis_C, casa1.PP as PP_vis_C, casa1.GF as GF_vis_C, casa1.GC as GC_vis_C, casa1.DG as DG_vis_C, fuera1.posicion as pos_vis_F, fuera1.puntos as pts_vis_F, fuera1.PJ as PJ_vis_F, fuera1.PG as PG_vis_F, fuera1.PE as PE_vis_F, fuera1.PP as PP_vis_F, fuera1.GF as GF_vis_F, fuera1.GC as GC_vis_F, fuera1.DG as DG_vis_F
    FROM result R
    LEFT JOIN clasi C ON R.local = C.equipo AND R.jornada = C.jornada
    LEFT JOIN clasi_1 C1 ON R.visitante = C1.equipo AND R.jornada = C1.jornada
    LEFT JOIN clasi_casa casa ON R.local = casa.equipo AND R.jornada = casa.jornada
    LEFT JOIN clasi_fuera fuera ON R.local = fuera.equipo AND R.jornada = fuera.jornada
    LEFT JOIN clasi_casa1 casa1 ON R.visitante = casa1.equipo AND R.jornada = casa1.jornada
    LEFT JOIN clasi_fuera1 fuera1 ON R.visitante = fuera1.equipo AND R.jornada = fuera1.jornada
"""


df_total = ps.sqldf(query, locals())

df_total = df_total.sort_values(by = 'jornada', ascending=True)


import os
directory = ruta
csv_path = os.path.join(directory, 'df_total.csv')

# Verificar y crear el directorio si no existe
if not os.path.exists(directory):
    os.makedirs(directory)
csv_path = directory + 'df_total.xlsx'
df_total.to_excel(csv_path, index = False)
print('Se ha creado correctamente')

# #función para eliminar datos de un csv
# file = open("df_total.xlsx", "w")
# file.close()
# #función para meter datos a un csv
# df_pd_total.to_excel('df_total.xlsx')





# ## Lectura df cuotas


# ruta_cuotas = 'C:/Users/gines/Desktop/webscrap_liga/SP1.csv'


# df_pd_cuotas = df_pd_resultados = pd.read_csv(ruta_cuotas)


# reemplazos = {'Almeria': 'UD ALMERÍA', 'Sevilla': 'SEVILLA FC','Sociedad':'REAL SOCIEDAD','Las Palmas':'UD LAS PALMAS',
#               'Ath Bilbao':'ATHLETIC CLUB','Celta':'RC CELTA','Villarreal':'VILLARREAL CF','Getafe':'GETAFE CF',
#              'Cadiz':'CÁDIZ CF','Ath Madrid': 'ATLÉTICO DE MADRID','Vallecano':'RAYO VALLECANO','Valencia':'VALENCIA CF',
#              'Girona':'GIRONA FC','Mallorca':'RCD MALLORCA','Real Madrid':'REAL MADRID','Osasuna':'CA OSASUNA','Betis':'REAL BETIS',
#              'Barcelona':'FC BARCELONA','Alaves':'DEPORTIVO ALAVÉS','Granada':'GRANADA CF'}


# df_pd_cuotas['HomeTeam'] = df_pd_cuotas['HomeTeam'].replace(reemplazos)
# df_pd_cuotas['AwayTeam'] = df_pd_cuotas['AwayTeam'].replace(reemplazos)
# df_pd_cuotas








