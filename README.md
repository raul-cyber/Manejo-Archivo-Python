Desafío Practico Entel.
=============================

Sistema de Manipulacion de Archivos.
------------------------------------

*Autor: Raúl García Vallejos
*Version: 1.0
*Desarrollado con python 3

Requisitos Solicitados Para la solucion solicitada:

1. Sistema Capaz de analizar un archivo de texto plano, con un formato definido.
2. Permitir Generar Reportes con informacion de ejecucion del Sistema Propiamentetal y un Reporte Financiero
3. Permitir Mantener un Registro Log, que describa los procesos Internos Realizados
4. Tratar la Data recibida en el archivo Base, con la finalidad de eliminar posibles espacios en blanco presentes en las columnas diferentes a la columna TipoDescuento
5. En Caso que existieran Registros en la Data base con un menor o mayor numeros de columnas ( Para este caso se considera que sea menor o mayor a 23, basado en el ejemplo de formato de la data base, entregado), este registro debe ser obviado del proceso de generacion de reportes y almacenado en un archivo diferente.

Solucion Propuesta:

*Se Propone una solucion realizada en base al lenguaje de programacion de Python en su version 3
*El sistema esta conformado por 3 archivos con la extension .py, estos son: Manejo de archivos.py , funciones.py y Procesos.py
*Manejo de archivos.py, sera el encargado de generar una pequeña interfaz de usuario, de tal forma que el usuario pueda buscar un archivo, independiente de la ubicacion que se encuentre en la maquina que se ejecute el sistema.
*funciones.py y Procesos.py contienen todos los metodos y librerias necesarias, tanto para la generacion de reportes, como para la generacion en tiempo real de un archivo de registros .log, en el siguiente apartado se detallara los metodos existentes por cada uno de estos archivos y cuales son sus funcionalidades dentro del procesamiento generado por el sistema.


funciones.py:

Este archivo, se encarga de realizar toda la carga en memoria de la data contenida en el archivo. De tal manera de realizar la lectura de este una sola vez y no perder tiempo de procesamiento en abrir y cerrar el archivo base por cada actividad que se realice. La funciones que se definieron son:

*lectura: Esta funcion recibe como parametro la ruta y nombre del archivo base, para posteriormete almacenar su data en memoria, y de esta forma poder generar los procesamientos de los registros capturados.
*Reparar: Esta funcion analiza los datos guardados en memoria, para ver si es necesario tener que reparar un registro que contenga espacios en su interior, siempre y cuando la columna analizada fuera distinta a la columna de detalle descuento, ya que es la unica que puede contener espacios en su interior. Al detectar un registro que tubiera espacios procede a quitarlos y regenerar el registro.
*filtrar: Esta funcion se encarga de analizar la data cargada en memoria, para ver si existe algun registro con un numero mayor o menor a 23 columnas de informacion. para posteriormente aislarla y registrarlas en un archivo diferente. Este archivo que contendra todos estos registros aisldos tiene como nombre Registros para ser revisados.txt
*CargarFiltrado: funcion encargada de generar el documento Registros para ser revisados.txt y agregar su contenido
*ValidarDocumento: Funcion que se encarga de validar que el documento seleccionado por el usuario contenga el formato correcto de columnas separadas por ;
* ModOrigin: funcion que se encarga de aplicar una recarga de la informacion perteneciente al archivo base, luego de haber sido repardos y filtrado, los registros correspondites.
*ReporteEjecutivo: Funcion que se encarga de preparar la data para ser insertada en un reporte con el formato pdf


