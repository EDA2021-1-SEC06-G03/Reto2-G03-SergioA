"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as shell
from DISClib.Algorithms.Sorting import selectionsort as selection
from DISClib.Algorithms.Sorting import insertionsort as insertion
from DISClib.Algorithms.Sorting import quicksort as quick
from DISClib.Algorithms.Sorting import mergesort as merge

assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog(estructura):
    """
    Inicializa el catálogo de libros. Crea una lista vacia para guardar
    todos los libros, adicionalmente, crea una lista vacia para los autores,
    una lista vacia para los generos y una lista vacia para la asociación
    generos y libros. Retorna el catalogo inicializado.
    """
    catalog = {'videos': None, 'VideosPorId':None,
               'VideosPorCategoriasId': None,
               'paises': None}
    catalog['videos'] = lt.newList(estructura)
    #lista de videos donde un video es una linea del csv
    catalog['VideosPorCategoriasId'] = mp.newMap(numelements=37, maptype='CHAINING', loadfactor=4.0,
     comparefunction=MAPcompareCategoriesById)
    #map : hash table, donde las llaves son dadas por las categorias y los valores de cada llave son videos,
    #  donde un video es una linea del csv (los mismos elementos de catalog['videos'])

    catalog['VideosPorId'] = mp.newMap(numelements=380000, maptype='PROBING', loadfactor=0.5,
     comparefunction=MAPcompareVideosById)
#map : hash table, donde las llaves son dadas por las video_id y los valores de cada llave son videos,
#  donde un video es una linea del csv (los mismos elementos de catalog['videos'])
#en otras palabras estos son los videos unicos

#antiguo:
    catalog['paises'] = lt.newList(datastructure = 'ARRAY_LIST')

    return catalog

# Funciones para agregar informacion al catalogo

def addVideo(catalog, video):
    # Se adiciona el video a la lista de videos
    lt.addLast(catalog['videos'], video)
    mp.put(catalog['VideosPorId'], video['video_id'], video)
    addVideo_a_Categoria(catalog, video)

def addVideo_a_Categoria(catalog, video):
    """
    Esta funcion adiciona un video a la lista de libros que
    son de la misma categoria especifica.
    Las categorias se guardan en un Map, donde la llave es la categoria
    y el valor es la lista de videos de esa categoria.
    """
    
    categorias = catalog['VideosPorCategoriasId']
#el video solo trae el id de la categoria, toca recorrer la lista de categorias para coger el nombre también
    categoria_id = video['category_id']
    
    entry = mp.get(categorias, categoria_id)
    videos_de_categoria = me.getValue(entry)
    
    lt.addLast(videos_de_categoria['videos'], video)

def addCategoria(catalog, categoria):
#esta categoria de entrada es un dicci
#    categoria_id = categoria['id']
#    nombre_categoria = categoria['name']
    categorias = catalog['VideosPorCategoriasId']
    categoria_id = categoria['id']
    existCate = mp.contains(categorias, categoria_id)
    if not existCate:
        videos_de_categoria = nuevaCategoria(categoria)
        mp.put(categorias, categoria_id, videos_de_categoria)

def nuevaCategoria(categoria):
#esta categoria de entrada es un dicci
#    categoria_id = categoria['id']
#    nombre_categoria = categoria['name']
    """
    Esta funcion crea la estructura de videos asociados
    a una categoria.
    """
    
    entry = {'categoria_id': "", "nombre_categoria": "", "videos": None}
    entry['categoria_id'] = categoria['id']
    entry['nombre_categoria'] = categoria['name']
    entry['videos'] = lt.newList('SINGLE_LINKED', compareCategories)
    return entry

#antiguo:
def addPais(catalog, pais):
    # Se adiciona el pais a la lista de paises
    lt.addLast(catalog['paises'], pais)




# Funciones para creacion de datos

#antiguo
def loadPaises(catalog):
    for video in lt.iterator(catalog['videos']):
        pais = str(video['country']).lower()
        if not (pais_presente(catalog, pais)):
            addPais(catalog, pais)

# Funciones de consulta
#antiguo
def subListVideos(catalog, pos, number):
    """
    Retorna sublista de videos
    """
    videos = catalog["videos"]
    
    return lt.subList(videos, pos, number)

#nuevo
def subListVideos2(lista, pos, number):
    return lt.subList(lista, pos, number)

#antiguo
def primer_video(catalog):
    return lt.firstElement(catalog['videos'])
#antiguo
def pais_presente(catalog, pais:str):
    return lt.isPresent(catalog['paises'], pais)
#nuevo
def categoria_presente(catalog, categoria_nombre:str):
    nombre_presente = False
    categoria_id = ''
    for categoria in lt.iterator(mp.valueSet(catalog['VideosPorCategoriasId'])):
        if categoria['nombre_categoria'] == categoria_nombre:
            nombre_presente = True
            categoria_id = categoria['categoria_id']
            break
    return (nombre_presente, categoria_id)

#antiguo
'''def subListVideos_porCategoria(tad_lista, categoria_id:str):
    sublist = lt.newList(datastructure = tad_lista['type'])
    for video in lt.iterator(tad_lista):
        
        if str(video['category_id']) == categoria_id:
            lt.addLast(sublist, video)
    return sublist'''

#nuevo:
def subListVideos_porCategoria(catalog, categoria_id:str):
    categorias = catalog['VideosPorCategoriasId']
    entry = mp.get(categorias, categoria_id)
    videos = me.getValue(entry)['videos']
    return videos

#antiguo
def subListVideos_porPais(tad_lista, pais:str):
    sublist = lt.newList(datastructure = tad_lista['type'])
    for video in lt.iterator(tad_lista):
        if video['country'] == pais:
            lt.addLast(sublist, video)
    return sublist

#antiguo
def ObtenerVideosDistintos(tad_lista):
    videos_distintos = lt.newList(datastructure = 'ARRAY_LIST')
    primero = lt.firstElement(tad_lista)
    primero['repeticiones'] = 1
    lt.addLast(videos_distintos, primero)
    leidos = 1
    for video in lt.iterator(tad_lista):
        if leidos > 1:
            video_agregar = {}
            info_deseada = ['title','video_id', 'category_id', 'views', 'channel_title', \
    'country', 'likes', 'dislikes', 'publish_time', 'trending_date', 'tags']
            
            for info in info_deseada:
                video_agregar[info] = video[info]
            if   lt.lastElement(videos_distintos)['video_id'] == video_agregar['video_id']:
                    lt.lastElement(videos_distintos)['repeticiones'] = lt.lastElement(videos_distintos)['repeticiones'] + 1
                    lt.lastElement(videos_distintos)['likes'] = max(int(video_agregar['likes']), int(lt.lastElement(videos_distintos)['likes']))
                    lt.lastElement(videos_distintos)['views'] = max(int(video_agregar['views']), int(lt.lastElement(videos_distintos)['views']))
            else :
                video_agregar['repeticiones'] = 1
                lt.addLast(videos_distintos, video_agregar)
        leidos += 1
    return videos_distintos




#antiguo
def getMaxReps(sublista):
    if not lt.isEmpty(sublista):
        maximo_valor = 0
        maximo_apuntador = lt.firstElement(sublista)
        for video in lt.iterator(sublista):
            if video['repeticiones'] >= maximo_valor:
                maximo_valor = video['repeticiones']
                maximo_apuntador = video
        return maximo_apuntador
    else:
        return None
#antiguo
def video_tiene_tag(video, tag:str):
    encontrado = False
    for t in lt.iterator(video['tags']):
        if tag in t:
            encontrado = True
            break

    return encontrado

#antiguo
def subListVideos_porTag(tad_lista, tag:str):
    sublist = lt.newList(datastructure = tad_lista['type'])
    for video in lt.iterator(tad_lista):
        if video_tiene_tag(video, tag):
            lt.addLast(sublist, video)
    return sublist





# Funciones utilizadas para comparar elementos dentro de una lista

#antiguo
def cmpVideosByViews(video1, video2):
    return (int(video1['views']) > int(video2['views']))
#antiguo
def cmpVideosByVideoID(video1, video2):
    return (str(video1['video_id']) > str(video2['video_id']))
#antiguo
def cmpVideosByLikes(video1, video2):
    return (int(video1['likes']) > int(video2['likes']))


def MAPcompareVideosById(id, entry):
    """
    Compara dos ids de videos, id es un identificador
    y entry una pareja llave-valor
    """
    identry = me.getKey(entry)
    if (id == identry):
        return 0
    elif (id > identry):
        return 1
    else:
        return -1

def MAPcompareCategoriesById(keyname, category):
    """
    Compara dos nombres de autor. El primero es una cadena
    y el segundo un entry de un map
    """
    cat_entry = me.getKey(category)
    if (keyname == cat_entry):
        return 0
    elif (keyname > cat_entry):
        return 1
    else:
        return -1

def compareCategories(cate1, cate2):
    if (cate1 == cate2):
        return 0
    elif (cate1 > cate2):
        return 1
    else:
        return -1

#def cmpVideosBy_criterio(video1, video2):
#    return (float(video1['criterio']) > float(video2['criterio']))

# Funciones de ordenamiento
#antiguo, pero creo que no se tendra que editar
def sortList(tad_lista, metodo, orden='vistas'):
    if orden == "vistas":
        funcion_comp = cmpVideosByViews
    if orden == "video_id":
        funcion_comp = cmpVideosByVideoID
    if orden == "likes":
        funcion_comp = cmpVideosByLikes
    '''
    if orden == "criterio"
        funcion_comp = cmpVideosBy_criterio
    '''
    #se puede hacer mas elegante haciendo un diccionario de funciones como valores y los nombres como llaves
    #tanto lo del criterio como lo de los metodos
    if metodo == "shell":
        shell.sort(tad_lista, funcion_comp)
    if metodo == "selection":
        selection.sort(tad_lista, funcion_comp)
    if metodo == "insertion":
        insertion.sort(tad_lista, funcion_comp)
    if metodo == "quick":
        quick.sort(tad_lista, funcion_comp)
    if metodo == "merge":
        merge.sort(tad_lista, funcion_comp)
