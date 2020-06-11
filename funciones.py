import Procesos as pros
import logging as log
from time import time
log.basicConfig(filename='Historial.log', filemode='a',level= log.DEBUG,format='%(asctime)s  %(levelname)s  %(message)s')

datafull = []
dataclear = []
datafilter = [] 
dataused = []
ReporteFinanciero = {}
TotalRegistrosReparado = 0
TotalRegistrosfiltrados = 0 



def ReporteTecnico(TotalRgistros,TiempoReparacio,TiempoFiltrado,TiempoRecargaArchivoOri,TiempoGeneracionReportes,TiempoTotalEjecucion):
    try:
        pros.GenerarReporteEjecucion(TotalRgistros,TotalRegistrosReparado,
        TotalRegistrosfiltrados,TiempoReparacio,TiempoFiltrado,TiempoRecargaArchivoOri,
        TiempoGeneracionReportes,TiempoTotalEjecucion)
    except:
        log.error('Errror Al generar Reporte Tecnico.... Estado NoOK\n')

def ReporteEjecutivo():
    try:
        ReporteFinanciero = pros.GenerarMapeo(dataused)
        data = pros.ConversionDataEjecutiva(ReporteFinanciero)
        pros.GenerarReporteEjecutivo(data)
    except:
        log.error('Error al Generar Reporte Ejecutivo.... Estado NoOK\n')
    

def ModOrigin(path):
    try:
        for data in dataused:
            pros.escritura(data, path)
        log.info('Proceso de Modificacion de archivo '+path+'completado......Estado OK\n')
        return('Proceso de Modificacion de archivo '+path+'completado......Estado OK\n')
    except:
        log.error('Proceso de Modificacion de archivo '+path+' incompleto......Estado NoOK\n')
        return('Proceso de Modificacion de archivo '+path+' incompleto......Estado NoOK\n')

def ValidarDocumento(path):
    try:
        respuesta = pros.validaFormat(path)
        log.info('Archivo: '+ path+'Validado Correctamente')
        return(respuesta)
    except:
        log.error('Archivo: '+ path+'Error al intentar Validar documento')

def CargarFiltrado(path):

    try:
        for data in datafilter:
            pros.escritura(data, path)
        log.info('Proceso de Carga de archivo Registros para ser revisados.txt completado......Estado OK\n')
        return('Proceso de Carga de archivo Registros para ser revisados.txt completado......Estado OK\n')
    except:
        log.error('Proceso de Carga de archivo Registros para ser revisados.txt incompleto......Estado NoOK\n')
        return('Proceso de Carga de archivo Registros para ser revisados.txt incompleto......Estado NoOK\n')

def filtrar():

    count = 0
    try:
        for data in dataclear:
            respuesta = pros.validateFilter(data)
            if(respuesta == 1):
                datafilter.append(data)
                count = count +1
            if(respuesta == 2):
                dataused.append(data)
            if(respuesta == 3):
                log.error("Error Filtrando Data......Proceso no Ok\n"+
                "Cantidad de Registros filtrados: "+str(count)+'\n')
                return("Error Filtrando Data......Proceso no Ok\n"+
                "Cantidad de Registros filtrados: "+str(count)+"\n")
        dataclear.clear()
        log.info("Proceso de Filtrado completo.......Proceso OK\n"+
        "Cantidad de Registros Filtrados: "+str(count)+'\n')
        TotalRegistrosfiltrados= count
        return("Proceso de Filtrado completo.......Proceso OK\n"+
        "Cantidad de Registros Filtrados: "+str(count)+'\n')
    except:
        log.error("Error Filtrando Data......Proceso no Ok\n"+
                "Cantidad de Registros filtrados: "+str(count)+'\n')
        return("Error Filtrando Data......Proceso no Ok\n"+
                "Cantidad de Registros filtrados: "+str(count)+'\n')

def Reparar():

    count = 0
    try:
        for data in datafull:
            Result =  pros.searchSpace(data)
            if(Result > 0):
                count = count + Result
                clearLine = pros.buildLine(data)
                dataclear.append(clearLine)
            else:
                dataclear.append(data)
        log.info('Proceso de Reparacion Completado.....Estado OK'+
        'Cantidad de Registros Reparados: '+ str(count)+'\n')
        TotalRegistrosReparado = count
        return('Proceso de Reparacion Completado.....Estado OK'+
        'Cantidad de Registros Reparados: '+ str(count)+'\n')
    except:
        log.error('Proceso de Reparacion No Completados.....Estado NoOK\n'+
        'Verificar Rura o Formato del documento analizado\n')
        return('Proceso de Reparacion No Completados.....Estado NoOK\n'+
        'Verificar Rura o Formato del documento analizado\n')

def lectura(path):
    Tinicio = time()
    data = open(path,'r')
    titulo = data.readline()
    pros.resetFile('Registros para ser revisados.txt')

    for linea in data:
        datafull.append(linea)
   
    TotalRgistros = len(datafull)
    TRini = time()
    Registros_reparados = Reparar()
    Registros_totales ='Total de Registros para analizar: '+ str(len(datafull))+'\n'
    datafull.clear()
    TRfin = time()
    TiempoReparacio = round(TRfin - TRini, 3)
    TFini = time()
    Registros_filtrados = filtrar()
    pros.escritura(titulo,'Registros para ser revisados.txt')
    Respuesta_Carga_Filter=CargarFiltrado('Registros para ser revisados.txt')
    datafilter.clear()
    TFfin = time()
    TiempoFiltrado = round(TFfin-TFini,3)
    TROini = time()
    pros.resetFile(path)
    pros.escritura(titulo, path)
    Respuesta_mod_Origin=ModOrigin(path)
    TROfin = time()
    TiempoRecargaArchivoOri = round(TROfin - TROini, 3)
    TRPini = time()
    ReporteEjecutivo()
    dataused.clear()
    data.close()
    TRPfin = time()
    TiempoGeneracionReportes =round( TRPfin - TRPini,3)
    Tfinal = time()
    Tejecucion = round((Tfinal - Tinicio), 3)
    TiempoTotalEjecucion = Tejecucion
    ReporteTecnico(TotalRgistros,TiempoReparacio,TiempoFiltrado,TiempoRecargaArchivoOri,TiempoGeneracionReportes,TiempoTotalEjecucion)
    Detalle_proceso = Registros_totales+Registros_reparados+Registros_filtrados+Respuesta_Carga_Filter+Respuesta_mod_Origin+'Tiempo total de ejecucion en Segundos: '+str(Tejecucion)+'\n'
    return(Detalle_proceso)
