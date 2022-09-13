import json
import oracledb
import os

un = 'eurocop'
pw = 'copLEGA2022'
cs = '10.1.55.111:1521/eucop'

#Conexion exitosa a la base de datos de EUROCOP
conexion = oracledb.connect(user=un, password=pw, dsn=cs)

#sql = """select sysdate from dual"""

cursor = conexion.cursor()



#for r in res:
#    print(r)

lista = []

def situacion():
    sql = """
            SELECT
                PERSONAL."NUMERO_PROFESIONAL" AS PERSONAL_NUMERO_PROFESIONAL,
                substr(PERSONAL."NUMERO_PROFESIONAL",6,1) AS PERSONAL_NUMERO_PROFESIONAL2,
                
                to_date(to_char(CUADRANTE."FECHA",'DD/MM/YYYY'),'DD/MM/YYYY') AS CUADRANTE_FECHA,
               
                TURNOINCIDENCIAS."SIGLAS" AS TURNOINCIDENCIAS_SIGLAS
     
                FROM
                    "EUROCOP"."PERSONAL" PERSONAL INNER JOIN "EUROCOP"."CUADRANTE" CUADRANTE ON PERSONAL."PERSONAL_ID" = CUADRANTE."PERSONAL_ID"
                    INNER JOIN "EUROCOP"."CUADRANTES_TURNOSERVICIO" CUADRANTES_TURNOSERVICIO ON CUADRANTE."TURNOSERVICIO_ID" = CUADRANTES_TURNOSERVICIO."TURNOSERVICIO_ID"
                    INNER JOIN "EUROCOP"."TURNOINCIDENCIAS" TURNOINCIDENCIAS ON CUADRANTES_TURNOSERVICIO."TURNOINCIDENCIAS_ID" = TURNOINCIDENCIAS."TURNOINCIDENCIAS_ID"
                where 
 
                ROWNUM < 2200
                ORDER BY PERSONAL.NUMERO_PROFESIONAL, CUADRANTE."FECHA"
            """

    res = cursor.execute(sql)

    

    for r in res:
        lista.append(r)


situacion()
print(lista)