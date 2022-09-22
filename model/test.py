import json
import oracledb
import os
#import listado as li
#import credenciales as cr

un = 'eurocop'
pw = 'copLEGA2022'
cs = '10.1.55.111:1521/eucop'

#Conexion exitosa a la base de datos de EUROCOP
conexion = oracledb.connect(user=un, password=pw, dsn=cs)

#sql = """select sysdate from dual"""




def situacion(fecha='13/09/2022'):
    lista = []
    sql = '''   SELECT substr(PERSONAL."NUMERO_PROFESIONAL",6,1) AS PERSONAL_NUMERO_PROFESIONAL2,     
                    to_char(CUADRANTE."FECHA",'DD/MM/YYYY') AS CUADRANTE_FECHA,     
                    TURNOINCIDENCIAS."SIGLAS" AS TURNOINCIDENCIAS_SIGLAS     
                FROM
                    "EUROCOP"."PERSONAL" PERSONAL INNER JOIN "EUROCOP"."CUADRANTE" CUADRANTE ON PERSONAL."PERSONAL_ID" = CUADRANTE."PERSONAL_ID"
                    INNER JOIN "EUROCOP"."CUADRANTES_TURNOSERVICIO" CUADRANTES_TURNOSERVICIO ON CUADRANTE."TURNOSERVICIO_ID" = CUADRANTES_TURNOSERVICIO."TURNOSERVICIO_ID"
                    INNER JOIN "EUROCOP"."TURNOINCIDENCIAS" TURNOINCIDENCIAS ON CUADRANTES_TURNOSERVICIO."TURNOINCIDENCIAS_ID" = TURNOINCIDENCIAS."TURNOINCIDENCIAS_ID"
                where 
                    to_char(CUADRANTE."FECHA",'DD/MM/YYYY') = '{fe}'	 

                ORDER BY PERSONAL.NUMERO_PROFESIONAL, CUADRANTE."FECHA"                
            '''.format(fe=fecha)    

    res = cursor.execute(sql) 

    policias = []   
    
    for r in res: 
        lista.append(r)

   
    #lista_situacion = dias_situacion(lista)
    #return dias_situacion(lista)
    return lista



def personal():
    cursor = conexion.cursor()
    lista = []
    sql = """SELECT 
            	CASE  
                    WHEN Personal.numero_profesional LIKE '280741%' THEN 'Policia'
                    WHEN Personal.numero_profesional LIKE '280742%' THEN 'Oficial'
                    WHEN Personal.numero_profesional LIKE '280743%' THEN 'Subinspector'
                    WHEN Personal.numero_profesional LIKE '280744%' THEN 'Inspector'
                    WHEN Personal.numero_profesional LIKE '280745%' THEN 'Intendente'
		        END AS CARGO
                from
                    Personal Personal 
                    left outer join
                        Tipo tipo1_ 
                            on Personal.estado_id=tipo1_.tipo_id 
                    left outer join
                        Texto_Traducible textotradu2_ 
                            on tipo1_.trNombre=textotradu2_.texto_traducible_id 
                    left outer join
                        Traduccion traduccion3_ 
                            on textotradu2_.texto_traducible_id=traduccion3_.texto_traducible_id 
                            and (
                                traduccion3_.idioma_id=1
                            ) 
                    where
                    (
                        (
                            upper(Personal.numero_profesional) like '%280742%' 
                            or upper(Personal.numero_profesional) like '%280743%' 
                            or upper(Personal.numero_profesional) like '%280744%' 
                            or upper(Personal.numero_profesional) like '%280745%' 
                            or upper(Personal.numero_profesional) like '%2807411%' 
                            or upper(Personal.numero_profesional) like '%2807412%' 
                            or upper(Personal.numero_profesional) like '%2807413%'
                        ) 
                        
                    )and Personal.estado_id=28433 
                    group by
                        Personal.numero_profesional ,
                        traduccion3_.texto
            """

    res = cursor.execute(sql)   

    p = 0
    o= 0
    s= 0
    ins= 0
    inten = 0 

    for r in res:
        item = list(r)

        #lista.append(item)

        if(item[0] == 'Policia'):
            p+= 1
        if(item[0] == 'Oficial'):
            o+= 1
        if(item[0] == 'Subinspector'):
            s+= 1
        if(item[0] == 'Inspector'):
            ins+= 1
        if(item[0] == 'Intendente'):
            inten+= 1
    
    lista.append(p)    
    lista.append(o)
    lista.append(s)
    lista.append(ins)
    lista.append(inten)

    return lista

def define_turno(turno="L"):
    cursor = conexion.cursor()
    lista_situacion = situacion()
    print(lista_situacion)



#Devuelve el listado de personas AP, V, M, T... 
def dias_situacion(fecha='13/09/2022'):
    cursor = conexion.cursor()
    listado = []
    sql = '''   SELECT substr(PERSONAL."NUMERO_PROFESIONAL",6,1) AS PERSONAL_NUMERO_PROFESIONAL2,     
                    to_char(CUADRANTE."FECHA",'DD/MM/YYYY') AS CUADRANTE_FECHA,     
                    TURNOINCIDENCIAS."SIGLAS" AS TURNOINCIDENCIAS_SIGLAS     
                FROM
                    "EUROCOP"."PERSONAL" PERSONAL INNER JOIN "EUROCOP"."CUADRANTE" CUADRANTE ON PERSONAL."PERSONAL_ID" = CUADRANTE."PERSONAL_ID"
                    INNER JOIN "EUROCOP"."CUADRANTES_TURNOSERVICIO" CUADRANTES_TURNOSERVICIO ON CUADRANTE."TURNOSERVICIO_ID" = CUADRANTES_TURNOSERVICIO."TURNOSERVICIO_ID"
                    INNER JOIN "EUROCOP"."TURNOINCIDENCIAS" TURNOINCIDENCIAS ON CUADRANTES_TURNOSERVICIO."TURNOINCIDENCIAS_ID" = TURNOINCIDENCIAS."TURNOINCIDENCIAS_ID"
                where 
                    to_char(CUADRANTE."FECHA",'DD/MM/YYYY') = '{fe}'	 

                ORDER BY PERSONAL.NUMERO_PROFESIONAL, CUADRANTE."FECHA"                
            '''.format(fe=fecha)    

    res = cursor.execute(sql) 

    policias = []   
    
    for r in res: 
        listado.append(r)
    

    policias=[]
    npolicias= 0
    noficiales= 0
   
    m= 0
    m5=0
    t=0
    n=0
    c=0
    b=0
    l=0
    ap=0
    n=0
    v=0
    om= 0
    on=0
    om5=0
    ot=0
    oc=0
    ob=0
    ol=0
    ofap=0
    on=0
    ov=0
    policias=[] 
    fila_pol={}

    oficiales={}   
    
    plantilla = {'Policias':[]}    
    
    for li in listado:    
        if(li[0]== '1'):
            npolicias +=1
            if(li[2] == 'M'):
                m+=1
               
            if(li[2] == 'N'):
                n+=1
              
            if(li[2] == 'M2'):
                m5+=1
              
            if(li[2] == 'T'):           
                t+=1
              
            if(li[2] == 'CIF' or  li[2] == 'CBO' or  li[2] == 'CPA'):           
                c+=1
                     
            if(li[2] == 'L'):           
                l+=1
             
            if(li[2] == 'AP' or li[2] == 'AP-'):           
                ap+=1
              
            if(li[2] == 'V'):           
                v+=1
               
            if(li[2] == 'B'):           
                b+=1

        if(li[0]== '2'):
            noficiales +=1
            if(li[2] == 'M'):
                om+=1
                
            if(li[2] == 'T'):           
                ot+=1
                
            if(li[2] == 'N'):           
                on+=1
                
            if(li[2] == 'M2'):
                om5+=1
                
            if(li[2] == 'CIF' or  li[2] == 'CBO' or  li[2] == 'CPA'):           
                oc+=1
                   
            if(li[2] == 'L'):           
                ol+=1
                
            if(li[2] == 'AP' or li[2] == 'AP-'):           
                ofap+=1
                
            if(li[2] == 'V'):           
                ov+=1
                
            if(li[2] == 'B'):           
                ob+=1

    fila_pol['Manana'] = m
    fila_pol['Noche'] = n
    fila_pol['Tarde'] = t
    fila_pol['Manana5-2'] = m5
    fila_pol['Convenio'] = c 
    fila_pol['Libre'] = l
    fila_pol['Asuntos propios'] = ap
    fila_pol['Vacaciones'] = v
    fila_pol['Baja'] = b

    plantilla['Policias'] = fila_pol

    oficiales['Manana'] = om
    oficiales['Noche'] = on
    oficiales['Tarde'] = ot
    oficiales['Manana5-2'] = om5
    oficiales['Convenio'] = oc     
    oficiales['Libre'] = ol
    oficiales['Asuntos propios'] = ofap
    oficiales['Vacaciones'] = ov
    oficiales['Baja'] = ob

    plantilla['Oficial'] = oficiales
    
    return plantilla
    

#Muestra los agentes de baja con su fecha de baja
def bajas():
    cursor = conexion.cursor()
    lista = []
    sql="""
            SELECT  p.NUMERO_PROFESIONAL, to_char(cp.fechadesde,'DD/MM/YYYY') AS fechadesde, to_char(cp.FECHAHASTA,'DD/MM/YYYY') AS FECHAHASTA, cp.NUMERODIAS FROM BAJAPERSONAL cp
            LEFT OUTER JOIN PERSONAL p ON p.PERSONAL_ID = cp.PERSONAL_ID
            WHERE cp.FECHAHASTA IS NULL ORDER BY  p.NUMERO_PROFESIONAL  
        """
    res = cursor.execute(sql)       
    
    for r in res:         
        lista.append(r)
    return lista

#DENUNCIAS AYTO
def denuncias_ayto(fecha = '01/01/2022'):
    cursor = conexion.cursor()
    lista = []
    sql="""select
                to_char(Denuncia.fechaGrabacion,
                'DD/MM/YYYY') as fechaGrabacion,
                count(*) as fechaDenuncia 
            from
                Denuncia Denuncia 
            where
            (
                Denuncia.fechaGrabacion between to_date('{} 00:00:00', 'DD/MM/YYYY HH24:MI:SS') 
                and to_date('{} 23:59:59', 'DD/MM/YYYY HH24:MI:SS') 
            )
            group by
                to_char(Denuncia.fechaGrabacion,'DD/MM/YYYY')
        """.format(fecha,fecha)
    res = cursor.execute(sql)     
    
    for r in res:        
        lista.append(r)
    if(len(lista)==0):
        f = fecha,0
        lista.append(f)        
        return lista
    return lista  

#DENUNCIAS JPT
def denuncias_JPT(fecha='01/01/2022'):
    cursor = conexion.cursor()
    lista = []
    sql="""
            select
                    to_char(Denuncia_DGT.fechaGrabacion,
                    'DD/MM/YYYY') as fechaGrabacion,
                    count(*) as fechaGrabacion_1 
                from
                    Denuncia_DGT Denuncia_DGT 
                where
                (
                    Denuncia_DGT.fechaGrabacion between to_date('{} 00:00:00', 'DD/MM/YYYY HH24:MI:SS') and to_date('{} 23:59:59', 'DD/MM/YYYY HH24:MI:SS') 
                )
                group by
                    to_char(Denuncia_DGT.fechaGrabacion,
                    'DD/MM/YYYY')
        """.format(fecha,fecha)
    res = cursor.execute(sql)  

    
    for r in res:
        lista.append(r)
    if(len(lista)==0):
        f = fecha,0
        lista.append(f)        
        return lista
    return lista  
   
    
#DENUNCIAS CAM
def denuncias_CAM(fecha='01/01/2022'):
    cursor = conexion.cursor()
    lista = []
    sql="""
            select
                    to_char(Denuncia_DGT.fechaGrabacion,
                    'DD/MM/YYYY') as fechaGrabacion,
                    count(*) as fechaGrabacion_1 
                from
                    Denuncia_DGT Denuncia_DGT 
                where
                (
                    Denuncia_DGT.fechaGrabacion between to_date('{} 00:00:00', 'DD/MM/YYYY HH24:MI:SS') and to_date('{} 23:59:59', 'DD/MM/YYYY HH24:MI:SS') 
                    AND length(Denuncia_DGT.SERIEBOLETIN) > 2
                )
                group by
                    to_char(Denuncia_DGT.fechaGrabacion,
                    'DD/MM/YYYY')
        """.format(fecha,fecha)

    res = cursor.execute(sql)
    for r in res:                
        lista.append(r)
    if(len(lista)==0):
        f = fecha,0
        lista.append(f)        
        return lista
    return lista     
    
#DENUNCIAS RADAR
def radar(fecha='01/01/2022'):
    cursor = conexion.cursor()
    lista = []
    sql="""
            select
                to_char(Denuncia.fechaGrabacion,
                'DD/MM/YYYY') as fechaGrabacion,       
                count(*) as fechaGrabacion_1 
            from
                Denuncia Denuncia 
            where
            (
                Denuncia.fechaGrabacion between to_date('{} 00:00:00', 'DD/MM/YYYY HH24:MI:SS') and to_date('{} 23:59:59', 'DD/MM/YYYY HH24:MI:SS')
                AND Denuncia.NUMEROBOLETIN LIKE '301%'
            )
            group by
                to_char(Denuncia.fechaGrabacion,
                'DD/MM/YYYY')
        """.format(fecha,fecha)

    res = cursor.execute(sql)
    for r in res:                
        lista.append(r)
    if(len(lista)==0):
        f = fecha,0
        lista.append(f)        
        return lista
    return lista 
        
#ENTRADAS DEPOSITO
def deposito(fecha='01/01/2022'):    
    cursor = conexion.cursor()
    lista = []
    sql="""
            select
                to_char(VehiculoDeposito.fechaEntrada,
                'DD/MM/YYYY') as fechaEntrada,
                count(*) as fechaEntrada_1 
            from
                VehiculoDeposito VehiculoDeposito 
            where
            (
                VehiculoDeposito.fechaEntrada between to_date('21/09/2022 00:00:00', 'DD/MM/YYYY HH24:MI:SS') and to_date('21/09/2022 23:59:59', 'DD/MM/YYYY HH24:MI:SS') 
            )
            group by
                to_char(VehiculoDeposito.fechaEntrada,
                'DD/MM/YYYY')
        """.format(fecha,fecha)

    res = cursor.execute(sql)
    for r in res:                
        lista.append(r)
    if(len(lista)==0):
        f = fecha,0
        lista.append(f)        
        return lista
    return lista 

#ENTRADAS DEPOSITO TIPO VEHICULO
def tipo_vehiculo_deposito(fecha='01/01/2022'):    
    cursor = conexion.cursor()
    lista = []
    sql="""
            select
                    to_char(VehiculoDeposito.fechaEntrada,
                    'DD/MM/YYYY') as fechaEntrada,
                    count(*) as fechaEntrada_1,
                    vehiculovi2_.tipoVehiculo as tipoVehiculo 
                from
                    VehiculoDeposito VehiculoDeposito 
                left outer join
                    Vehiculo vehiculo1_ 
                        on VehiculoDeposito.vehiculo_id=vehiculo1_.vehiculo_id 
                left outer join
                    VehiculoView vehiculovi2_ 
                        on vehiculo1_.vehiculo_id=vehiculovi2_.vehiculo_id 
            where
            (
                VehiculoDeposito.fechaEntrada between to_date('{} 00:00:00', 'DD/MM/YYYY HH24:MI:SS') and to_date('{} 23:59:59', 'DD/MM/YYYY HH24:MI:SS') 
            )
            group by
                to_char(VehiculoDeposito.fechaEntrada,
                'DD/MM/YYYY'),vehiculovi2_.tipoVehiculo
        """.format(fecha,fecha)

    res = cursor.execute(sql)
    for r in res:                
        lista.append(r)
    if(len(lista)==0):
        f = fecha,0,""
        lista.append(f)        
        return lista
    return lista 

#DATOS REGISTRO DE ENTRADA
def registro_entrada(fecha='01/01/2022'):    
    cursor = conexion.cursor()
    lista = []
    sql="""
            select
                    to_char(RegistroEntrada.fecharegistro,
                    'DD/MM/YYYY') as fecharegistro,
                    substr( hechoview2_.descripcion,4) as descripcion,
                    count(*) as descripcion_1 
                from
                    RegistroEntrada RegistroEntrada 
                left outer join
                    Hecho hecho1_ 
                        on RegistroEntrada.hecho_id=hecho1_.id 
                left outer join
                    HechoView hechoview2_ 
                        on hecho1_.id=hechoview2_.id 
                where
                (
                    RegistroEntrada.fecharegistro between to_date('{} 00:00:00', 'DD/MM/YYYY HH24:MI:SS') and to_date('{} 23:59:59', 'DD/MM/YYYY HH24:MI:SS') 
                )
                group by
                    to_char(RegistroEntrada.fecharegistro,
                    'DD/MM/YYYY') ,
                    hechoview2_.descripcion ORDER BY count(*)
        """.format(fecha,fecha)

    res = cursor.execute(sql)
    for r in res:                     
        lista.append(r)
    if(len(lista)==0):
        f = fecha,"",0
        lista.append(f)        
        return lista
    return lista 