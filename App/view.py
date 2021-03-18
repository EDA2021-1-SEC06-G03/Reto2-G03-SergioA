"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """
import time
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
assert cf





'''
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
'''
def initCatalog(estructura):
    """
    Inicializa el catalogo de libros
    """
    return controller.initCatalog(estructura)

def loadData(catalog, size_videos: int, estructura='ARRAY_LIST'):
    """
    Carga los libros en la estructura de datos
    """
    controller.loadData(catalog, size_videos)



def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Consultar top x videos por vistas, dado el país y la categoría")
    print("3- Consultar el video con mayor cantidad de dias de tendencia de un pais")
    print("4- Videos por categoria")
    print("5- Consultar top x videos por LIKES, dado el país y UN tag")

    print('Reto 2:')
    print('6- Consultar n videos con más likes en una categoria')
    print("0- Salir")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        if catalog == None:
            print("¿Cual estructura de datos deseas usar para guardar los videos?")
            ha_escogido = False
            while not ha_escogido:
                print("1: Arreglo (Recomendado)")
                print("2: Lista Enlazada")
                escogencia = str(input(""))
                if escogencia == "1":
                    ha_escogido = True
                    estructura = 'ARRAY_LIST'
                elif escogencia == "2":
                    ha_escogido = True
                    estructura = 'LINKED_LIST'
                else:
                    print("Por favor escoge una de las dos opciones")
            
            print("Cuantos videos desea cargar maximo: (escribe T para todos)")
            cantidad_datos = input("")

            print("Cargando información de los archivos ....")
            if str(cantidad_datos).lower() == 't':
                cantidad_datos = 375942
            cantidad_datos = int(cantidad_datos)
            if cantidad_datos >= 375942:
                print("Espera mientras se cargan todos los datos, recuerda que el archivo Large tiene {} videos".format(str(375942)))
            time_1 = time.process_time()
            catalog = initCatalog(estructura)
            loadData(catalog, cantidad_datos)
            time_2 = time.process_time()
            print('Videos cargados: ' + str(lt.size(catalog['videos'])))
            print('Milisegundos de carga :{}'.format(str((time_2-time_1)*1000)))
            print('Categorias cargadas: ' + str(mp.size(catalog['VideosPorCategoriasId'])))
            print('Las categorias cargadas son :')
            posicion_imprimir = 1
            for cate in lt.iterator(mp.valueSet(catalog['VideosPorCategoriasId'])):
                print(str(posicion_imprimir),": " + "ID: " + cate["categoria_id"] + "  ,  Nombre: " + cate['nombre_categoria'])
                posicion_imprimir += 1
            primer_video = controller.primer_video(catalog)
            print('El primer video cargado es:')
            print("Titulo: " + primer_video["title"] + ", Canal: " + primer_video["channel_title"] + ", Fecha de tendencia: " + \
                str(primer_video["trending_date"]) + ", País: " + primer_video["country"] + ", Vistas: " + str(primer_video["views"]) + \
                    ", Likes: " + str(primer_video["likes"]) + ", Dislikes: " + str(primer_video["dislikes"]))
            print('Los paises distintos de los videos son :')
            contador_paises = 1
            for pais in lt.iterator(catalog['paises']):
                print(str(contador_paises),':',pais)
                contador_paises += 1
        else:
            print('Los datos ya han sido cargados, recuerda que el programa solo tiene permitido cargar\
los datos una vez de los archivos. \n Para recargar, reinicia la aplicación.')
        
        
    
    elif int(inputs[0]) == 2:
        n = lt.size(catalog['videos'])
        print("Buscando en el país: ")
        ha_escogido_pais = False
        while not ha_escogido_pais:
            pais = input("")
            if controller.pais_presente(catalog, pais):
                ha_escogido_pais = True
            else:
                print("Por favor ingresa un pais disponible.")
        print("Buscando en la categoria de ID: ")
        ha_escogido_categoria = False
        while not ha_escogido_categoria:
            categoria_id = input("")
            if controller.categoria_id_presente(catalog, categoria_id):
                ha_escogido_categoria = True
            else:
                print("Por favor ingresa el id de una categoria disponible.")
        print("Revisar entre los primeros x videos: (escribe T para todos)")
        ha_escogido_tamaño = False
        while not ha_escogido_tamaño:
            tamaño_muestra = input("")
            if str(tamaño_muestra).lower() == 't':
                ha_escogido_tamaño = True
                tamaño_muestra = n
            tamaño_muestra = int(tamaño_muestra)
            if tamaño_muestra <= n:
                ha_escogido_tamaño = True
            else:
                print("Recuerda que hay " + str(n) + " videos cargados")
        print("¿Cual algoritmo deseas usar para organizar los videos?")
        ha_escogido_metodo = False
        print("1: Shell Sort ")
        print("2: Selection Sort")
        print("3: Insertion Sort")
        print("4: Quick (Recomendado) Sort")
        print("5: Merge (Recomendado) Sort")
        while not ha_escogido_metodo:
            escogencia = str(input(""))
            if escogencia == "1":
                ha_escogido_metodo = True
                metodo = 'shell'
            elif escogencia == "2":
                ha_escogido_metodo = True
                metodo = 'selection'
            elif escogencia == "3":
                ha_escogido_metodo = True
                metodo = 'insertion'
            elif escogencia == "4":
                ha_escogido_metodo = True
                metodo = 'quick'
            elif escogencia == "5":
                ha_escogido_metodo = True
                metodo = 'merge'
            else:
                print("Por favor escoge una de las cinco opciones de algoritmos de ordenamiento")
        ha_escogido_tamaño_a_mostrar = False
        print("Aunque se organizaran " + str(tamaño_muestra) + " videos, puedes escoger cuantos mostrar en pantalla:")
        while not ha_escogido_tamaño_a_mostrar:
            tamaño_a_mostrar = int(input(""))
            if tamaño_a_mostrar <= tamaño_muestra :
                ha_escogido_tamaño_a_mostrar = True
            else:
                print("Recuerda que organizaras " + str(tamaño_muestra) + " videos")
        ha_escogido_metodo = False
        print("Organizando datos con {}sort, por favor espera...".format(str(metodo)))
        time_1 = time.process_time()
        mas_vistos = controller.getMostViewed(catalog, tamaño_muestra, pais, categoria_id, metodo)
        time_2 = time.process_time()
        posicion_imprimir = 1
        for video in lt.iterator(mas_vistos):
            print(str(posicion_imprimir),": " + "Titulo: " + video["title"] + ", Vistas: " + str(video["views"]) + ", Fecha de tendencia: " \
+ str(video["trending_date"]) + ", Canal: " + video["channel_title"] + ", Likes: " + str(video["likes"]) + ", Dislikes: "\
+ str(video["dislikes"]) + ", Fecha publicación: " + video["publish_time"])
            posicion_imprimir += 1
            if posicion_imprimir > tamaño_a_mostrar:
                break
        print('Milisegundos de carga :{}'.format(str((time_2-time_1)*1000)))
        
    
    elif int(inputs[0]) == 3:
        print("Buscando en el país: ")
        ha_escogido_pais = False
        while not ha_escogido_pais:
            pais = input("")
            if controller.pais_presente(catalog, pais):
                ha_escogido_pais = True
            else:
                print("Por favor ingresa un pais disponible.")
        print('Cargando informacion, por favor espera...')
        time_1 = time.process_time()
        mas_trending = controller.getMostTrending(catalog, pais)
        time_2 = time.process_time()
        print("El video con mayor cantidad de dias en tendencia en {} es : ".format(pais))
        print("Titulo: " + mas_trending["title"] + ", Canal: " + mas_trending["channel_title"] + ", Dias en tendencia: "\
 + str(mas_trending["repeticiones"]) + ", Pais: " + mas_trending["country"])
        print('Milisegundos de carga :{}'.format(str((time_2-time_1)*1000)))
#        print(mas_trending['video_id'])
    
    elif int(inputs[0]) == 4:
        categoria = input("Digite el nombre de la categoría que desea buscar")
        categoryCatalog = controller.getVideosByCategory(catalog, categoria, catalog)
        video = controller.masDiasTrending(catalog)
        print("El vídeo con más días de tendencia en la categoría {0} fue: Nombre: {1} -- Canal: {2} -- ID de la Categoría: {3} -- Días en Trending: {4}".format(categoryName, video['title'], video['channel_title'], video['category_id'], video['dias_t']))
    
    elif int(inputs[0]) == 5:
        n = lt.size(catalog['videos'])
        print("Buscando en el país: ")
        ha_escogido_pais = False
        while not ha_escogido_pais:
            pais = input("")
            if controller.pais_presente(catalog, pais):
                ha_escogido_pais = True
            else:
                print("Por favor ingresa un pais disponible.")
        print("Buscando videos con el tag: ")
        tag = str(input(''))
        print("Revisar entre los primeros x videos: (escribe T para todos)")
        ha_escogido_tamaño = False
        while not ha_escogido_tamaño:
            tamaño_muestra = input("")
            if str(tamaño_muestra).lower() == 't':
                ha_escogido_tamaño = True
                tamaño_muestra = n
            tamaño_muestra = int(tamaño_muestra)
            if tamaño_muestra <= n:
                ha_escogido_tamaño = True
            else:
                print("Recuerda que hay " + str(n) + " videos cargados")
        print("¿Cual algoritmo deseas usar para organizar los videos?")
        ha_escogido_metodo = False
        print("1: Shell Sort ")
        print("2: Selection Sort")
        print("3: Insertion Sort")
        print("4: Quick (Recomendado) Sort")
        print("5: Merge (Recomendado) Sort")
        while not ha_escogido_metodo:
            escogencia = str(input(""))
            if escogencia == "1":
                ha_escogido_metodo = True
                metodo = 'shell'
            elif escogencia == "2":
                ha_escogido_metodo = True
                metodo = 'selection'
            elif escogencia == "3":
                ha_escogido_metodo = True
                metodo = 'insertion'
            elif escogencia == "4":
                ha_escogido_metodo = True
                metodo = 'quick'
            elif escogencia == "5":
                ha_escogido_metodo = True
                metodo = 'merge'
            else:
                print("Por favor escoge una de las cinco opciones de algoritmos de ordenamiento")
        ha_escogido_tamaño_a_mostrar = False
        print("Aunque se organizaran " + str(tamaño_muestra) + " videos, puedes escoger cuantos mostrar en pantalla:")
        while not ha_escogido_tamaño_a_mostrar:
            tamaño_a_mostrar = int(input(""))
            if tamaño_a_mostrar <= tamaño_muestra :
                ha_escogido_tamaño_a_mostrar = True
            else:
                print("Recuerda que organizaras " + str(tamaño_muestra) + " videos")
        
        ha_escogido_metodo = False
        print("Organizando datos con {}sort, por favor espera...".format(str(metodo)))
        time_1 = time.process_time()
        mas_likes = controller.getMostLiked_porPaisyTags(catalog, tamaño_muestra, pais, tag, metodo)
        time_2 = time.process_time()
        posicion_imprimir = 1
        for video in lt.iterator(mas_likes):
            print(str(posicion_imprimir),": " + "Titulo: " + video["title"] + ", Vistas: " + str(video["views"]) +\
", Canal: " + video["channel_title"] + ", Likes: " + str(video["likes"]) + ", Dislikes: " + str(video["dislikes"])\
+ "Fecha publicación: " + video["publish_time"])
            print('Tags del video: ' )
            for tag in lt.iterator(video['tags']):
                print(tag)
            posicion_imprimir += 1
            if posicion_imprimir > tamaño_a_mostrar:
                break
        print('Milisegundos de carga :{}'.format(str((time_2-time_1)*1000)))
        
    elif int(inputs[0]) == 6:
        print("Buscando en la categoria con nombre: \n")
        ha_escogido_categoria = False
        while not ha_escogido_categoria:
            categoria_nombre = input("")
            id_presente = controller.categoria_presente(catalog, categoria_nombre)
            if id_presente[0]:
                ha_escogido_categoria = True
                categoria_id = id_presente[1]
            else:
                print("Por favor ingresa una categoria disponible.")
        n = lt.size(controller.subListVideos_porCategoria(catalog, categoria_id))
        print("Hay {} videos en la categoria".format(str(n)))
        print('Cuatos videos deseas procesar:\n')
        ha_escogido_tamaño = False
        while not ha_escogido_tamaño:
            tamaño = int(input(""))
            if tamaño <= n:
                ha_escogido_tamaño = True
            else:
                print("Recuerda que hay {} videos en la categoria".format(str(n)))
        print('Mostrar en pantalla los primeros:\n')
        ha_escogido_tamaño_mostrar = False
        while not ha_escogido_tamaño_mostrar:
            tamaño_mostrar = int(input(""))
            if tamaño_mostrar <= tamaño:
                ha_escogido_tamaño_mostrar = True
            else:
                print("Recuerda que organizaras {} videos ".format(str(tamaño)))
        time_1 = time.process_time()
        mas_likeados = controller.getMostLiked_porCategoria(catalog, categoria_id, tamaño)
        time_2 = time.process_time()
        contador = 0
        for video in lt.iterator(mas_likeados):
            contador += 1
            print(str(contador)+': '+'Titulo: '+(video['title']) + 'Likes: ' + str(video['likes']))
            if contador >= tamaño_mostrar:
                break
        print('Milisegundos de carga :{}'.format(str((time_2-time_1)*1000)))

        
        
    
    else:
        sys.exit(0)

sys.exit(0)
        
# falta pulir view, dejar bien hechos los nuevos, borrar los viejos si lo requieren
