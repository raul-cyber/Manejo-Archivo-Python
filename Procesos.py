import logging as log
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table,Image, Spacer,Paragraph
from reportlab.platypus.tables import TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import cm
log.basicConfig(filename='Historial.log', filemode='a',level= log.DEBUG,format='%(asctime)s  %(levelname)s  %(message)s')



def GenerarMapeo(data):

    diccionarioAux = {}
    try:
        for values in data:
            contenido_diccionario = values.split(';')
            if(contenido_diccionario[3]!= '' and contenido_diccionario[2]!= '' ):
                revision= diccionarioAux.get(contenido_diccionario[3],False)
                if(revision == False):
                    diccionarioAux[contenido_diccionario[3]] = [round(float(contenido_diccionario[2]),3),1]
                else:
                    valordescuento = revision[0]
                    cantidadTdescuento = revision[1]
                    valordescuento = valordescuento + float(contenido_diccionario[2])
                    cantidadTdescuento = cantidadTdescuento + 1
                    diccionarioAux[contenido_diccionario[3]] = [round(valordescuento,3),cantidadTdescuento]


            else:
                log.error('Un Registro no cuenta con datos de valor de descuento o el detalle del descuento')
                diccionarioAux.clear()
                return(diccionarioAux)

        return(diccionarioAux)
                
    except:
        log.error('Un Registro no cuenta con datos de valor de descuento o el detalle del descuento')
        diccionarioAux.clear()
        return(diccionarioAux)


def searchSpace(data):

    lista = data.split(';')

    count = 0

    for i in range(len(lista)-1):

        if(i != 3):
            busqueda = lista[i].find(' ')
            if(busqueda >= 0):
                count = 1
    
    return(count)


def buildLine(data):

    lista = data.split(';')
    
    lineaReparada =''

    try:

        for i in range(len(lista)-1):

            if(i != 3 ):
                busqueda = lista[i].find(' ')
                if(busqueda >= 0):
                    auxExtrem = lista[i].strip()
                    auxinternal = auxExtrem.replace(' ', '')
                    if(len(lineaReparada) == 0):
                         lineaReparada = auxinternal
                    else:
                        lineaReparada = lineaReparada + ';'+ auxinternal
                else:
                    if(len(lineaReparada) == 0):
                        lineaReparada = lista[i]
                    else:
                        lineaReparada = lineaReparada + ';'+ lista[i]

            else:
                lineaReparada = lineaReparada + ';'+ lista[i]
        
        lineaReparada = lineaReparada+'\n'
        return(lineaReparada)
    except:
        log.error('Error al Reparar Registro: '+ data)


def validateFilter(data):

    try:
        metadata = data.split(';')
        cantidadMetadata = len(metadata)
        if (cantidadMetadata < 23 or cantidadMetadata > 23):
            return(1)
        if(cantidadMetadata == 23):
            return(2)
    except:
        log.error('Ocurrio un error al analizar la data: '+ data)
        return(3)


def escritura(linea , path):

    try:
        file = open(path,"a")
        file.write(linea)
        file.close()

    except:
        log.error('Error al escribir: '+ linea+' En el archivo: '+ path)



def resetFile(path):
    try:
        archivo = open(path, "w")
        archivo.close()
    except:
        log.error('Problema al Trabajar con el Documento: '+path+'Reset......NoOk')



def validaFormat(path):
    
    try:
        documento = open(path,'r')
        for linea in documento:
            metadata = linea.split(';')
        documento.close()
        return(1)
    
    except:
        log.error('Revision Incompleta Estado del Documento: '+ path+' NoOK, no cumple con el formato interno esperado')
        return(0)


def GenerarReporteEjecucion(datatotal, datareparada,datafiltrada,tiempoR,tiempoF,tiempoRSO,tiempoRPF,tiempoT):

    data_table =[
        ['Proceso', 'Resultado'],
        ['Total Data Analizada',str(datatotal)],
        ['Total Data Reperada',str(datareparada)],
        ['Total Data Filtrada',str(datafiltrada)],
        ['Tiempo de Reparacion',str(tiempoR)+' (s)'],
        ['Tiempo de Filtracion',str(tiempoF)+' (s)'],
        ['Tiempo Reset Documento Original',str(tiempoRSO)+' (s)'],
        ['Tiempo Generacion Reporte Financiero',str(tiempoRPF)+' (s)'],
        ['Tiempo Total Ejecucion Sistema',str(tiempoT)+' (s)']
    ]

    pdf = 'Reporte Tecnico.pdf'
    doc = SimpleDocTemplate(pdf, pagesize= letter, rightMargin=72, leftMargin=72,
                        topMargin=72, bottomMargin=18)
    contenido = []
    logo = './img/Entel.jpg'
    imagen = Image(logo , width= 180  , height= 180  ,hAlign='CENTER')
    contenido.append(imagen)
    Titulo = 'Reporte Ejecucion:'
    Estilos = getSampleStyleSheet()
    Estilos.add(ParagraphStyle(name ='Center', alignment= TA_CENTER))
    contenido.append(Paragraph(Titulo, Estilos["Normal"]))
    contenido.append(Spacer(width=1, height=30))
    tabla = Table(data_table)
    estilohead = TableStyle([
        ('BACKGROUND', (0,0), (2,0), colors.orangered),
        ('TEXTCOLOR',(0,0),(-1,0), colors.blue),
        ('ALIGN',(0,0),(-1,-1), 'CENTER'),
        ('BACKGROUND',(0,1),(-1,-1), colors.beige),
        ('GRID',(0,1),(-1,-1),2,colors.blue),
        ('BOX',(0,0),(-1,-1),2,colors.blue)
    ])
    tabla.setStyle(estilohead)
    contenido.append(tabla)
    doc.build(contenido)


def ConversionDataEjecutiva(diccionario):
    listadelista = [['Monto','CantidadDescuento','TipoDescuento']] 
    llavesdiccionario = diccionario.keys()
    for llave in llavesdiccionario:
        datos = diccionario.get(llave)
        fila = [datos[0],datos[1],llave]
        listadelista.append(fila)
    return(listadelista)


def GenerarReporteEjecutivo(diccionario):

    data_table = diccionario
    pdf = 'Reporte Financiero.pdf'
    doc = SimpleDocTemplate(pdf, pagesize= letter, rightMargin=72, leftMargin=72,
                        topMargin=72, bottomMargin=18)
    contenido = []
    logo = './img/Entel.jpg'
    imagen = Image(logo , width= 180  , height= 180  ,hAlign='CENTER')
    contenido.append(imagen)
    Titulo = 'Reporte Ejecutivo:'
    Estilos = getSampleStyleSheet()
    Estilos.add(ParagraphStyle(name ='Center', alignment= TA_CENTER))
    contenido.append(Paragraph(Titulo, Estilos["Normal"]))
    contenido.append(Spacer(width=1, height=30))
    tabla = Table(data_table)
    estilohead = TableStyle([
        ('BACKGROUND', (0,0), (3,0), colors.orangered),
        ('TEXTCOLOR',(0,0),(-1,0), colors.blue),
        ('ALIGN',(0,0),(-1,-1), 'CENTER'),
        ('BACKGROUND',(0,1),(-1,-1), colors.beige),
        ('GRID',(0,1),(-1,-1),2,colors.blue),
        ('BOX',(0,0),(-1,-1),2,colors.blue)
    ])
    tabla.setStyle(estilohead)
    contenido.append(tabla)
    doc.build(contenido)




