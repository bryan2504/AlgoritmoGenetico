## Librerías
import os, sys
import Image
import math
import random

## IMG: "C:\Users\PC\Desktop\steve.jpg"

## Variables Globales
nombre_img = ""
generacion = 1
limites = []
dimensiones = []
imgs_selec = []

def VGE (dir_imagen,tamanno_poblacion,proprobabilidad_cruce,porcentaje_mutacion, porcentaje_menosAptos): ##Faltan muchos parámetros aún
    global nombre_img, dimensiones, imgs_selec
    nombre_img = define_nombre(dir_imagen)
    img_meta = Image.open(dir_imagen)#Variable que guarda la imágen meta
##    print(list(img_meta.getdata())[0])
    dimensiones = img_meta.size #tupla con dimensiones de imagen
    
    lista_imagenes = primera_gen(dimensiones,tamanno_poblacion)   #lista llena de imágenes
    imgs_selec.append(lista_imagenes[0])
    
    nueva_generacion = []

    cont = 0 # Se usará para iterar el ciclo n veces(tamaño de la poblacion).
             # También se usará para saber cuándo tomar un especimen para el colage

    lista_temp =[] #temporal para el cruce de genes
    num = 0
    while (cont<tamanno_poblacion):

        #Cuando es un tamaño de poblacion impar, se duplica un especimen para que no haya nada sin cruzarse.
        if (len(lista_imagenes)%2==1):
            lista_imagenes.append(lista_imagenes[random.randrange(0,len(lista_imagenes))])
        lista_temp =[] #temporal para el cruce de genes
        #Cruce
        while(lista_imagenes!=[]):
            img1=lista_imagenes[random.randrange(0,len(lista_imagenes))]
            lista_imagenes.remove(img1)
            img2=lista_imagenes[random.randrange(0,len(lista_imagenes))]
            lista_imagenes.remove(img2)

            result_cruce = cruce(img1, img2)
            lista_temp = lista_temp + result_cruce

        print("Se ha completado un nuevo cruce "+"("+str(cont)+").")

        lista_imagenes= lista_temp
        lista_temp = []
        
        #Mutación
        lista_temp = generar_mutacion(lista_imagenes,img_meta,dimensiones,porcentaje_mutacion,tamanno_poblacion)
        lista_imagenes= lista_temp
        lista_temp = []
        print("Mutación completada")

        #Cuando no hayan menos de 10 generaciones realizadas
        if(cont>=(float(tamanno_poblacion)/10)*num):
            img_apta = buscar_mas_apto(lista_imagenes,img_meta,dimensiones) 
            imgs_selec.append(img_apta)
            num = num + 1
            print(similitud_porcentual(imgs_selec[-1].load(),img_meta.load(),dimensiones))
            print("Guardado nuevo especimen.")
        
        #Fin de iteracion
        cont=cont+1
    imgs_concatenadas = []
    cont_filas = 1
    xxx =[] 
    while(cont_filas < len(imgs_selec)):
        xxx = xxx + list(imgs_selec[cont_filas].getdata())
        cont_filas = cont_filas + 1
    print(len(imgs_selec))
    img_final = Image.new('RGB',(dimensiones[0],dimensiones[1]*(len(imgs_selec)-1)))
    img_final.putdata(xxx)
    img_final.save(nombre_img+str(generacion)+"FINAL.jpg")

    ##    print(euclideana(img_meta,imgs_selec[-1],dimensiones))
    print("El programa ha concluído con éxito.")

def buscar_mas_apto(lista_imagenes,imagen_meta,dimensiones):
    cont = 1;
    mas_apto = lista_imagenes[0]
    while (cont<len(lista_imagenes)):
        if (similitud_porcentual(mas_apto.load(),imagen_meta.load(),dimensiones) < similitud_porcentual(lista_imagenes[cont].load(),imagen_meta.load(),dimensiones)):
            mas_apto = lista_imagenes[cont]
        cont+=1
    return mas_apto

def define_nombre(dir_imagen):
    result = []
    x=5
    while (x>0):
        if(dir_imagen[-x]!='\\'):
            result.insert(0,dir_imagen[-x])
            x = x+1
        else:
            break
    final = ""
    for e in (result):
        final = final + e
    return (final)

def convertir_pix_imagen(pix,dimensiones):
    largo = 0
    listaPix = []
    img_creada = Image.new('RGB',(dimensiones[0],dimensiones[1]))
    while (largo<(dimensiones[1])):
        ancho = 0
        while (ancho<dimensiones[0]):
            r = pix[ancho,largo][0]
            g = pix[ancho,largo][1]
            b = pix[ancho,largo][2]
            listaPix.append((r,g,b))
            ancho = ancho + 1
        largo = largo + 1
    img_creada.putdata(listaPix)
    return img_creada

def primera_gen(dimensiones,tamanno): #Función que genera una imágen random como primera generación
    global limites
    """Recibe: Tupla con dimensiones de la imágen meta."""
    cont = 0
    lista_final = []
    lista_imagenes = []
    contador = 0
    while(contador<tamanno):
        while (cont<dimensiones[0]):
            cont2 = 0
            while (cont2<dimensiones[1]):
                r,g,b = random.randrange(0,256), random.randrange(0,256),random.randrange(0,256)
                lista_final.append((r,g,b))
                cont2 = cont2 + 1
            cont = cont + 1
        primera_gen = Image.new('RGB',dimensiones)
        primera_gen.putdata(lista_final)
        lista_imagenes.append(primera_gen)
        contador+= 1
    print("El programa creó "+str(len(lista_imagenes))+" individuos iniciales.")
    cont1=0
    limites=[]
    while(cont1!=dimensiones[0]):
        cont2=0
        listatemp = []
        while(cont2!=dimensiones[1]):
            listatemp.append([[0, 256],[0, 256],[0, 256]])
            cont2 = cont2 + 1
        limites.append(listatemp)
        cont1 = cont1 + 1
    return lista_imagenes
    
def euclideana(pix1, pix2,dimensiones):
    """Recibe:  1. Dir. de imágen a evaluar.
                2. Dir. de imágen meta.
                3. Dimensiones imágen meta."""
    result_final = 0
    alt=0
    while (alt<dimensiones[0]):
        anch=0
        while(anch<dimensiones[1]):
            diferencia = (pix1[alt,anch][0]+pix1[alt,anch][1]+pix1[alt,anch][2])-(pix2[alt,anch][0]+pix2[alt,anch][1]+pix2[alt,anch][2])
            result_final = result_final + abs(diferencia)
            anch = anch + 1
        alt = alt +1
    result_final = math.sqrt(result_final)
    return(result_final)

def chebyshev(pix1,pix2,dimensiones):
    alt=0
    mayor_diferencia = 0
    while (alt<dimensiones[0]):
        anch=0
        while(anch<dimensiones[1]):
            diferencia = (pix1[alt,anch][0]+pix1[alt,anch][1]+pix1[alt,anch][2])-(pix2[alt,anch][0]+pix2[alt,anch][1]+pix2[alt,anch][2])
            if (abs(diferencia) > mayor_diferencia):
                mayor_diferencia = abs(diferencia)
                anch+=1
            else:
                anch+=1
        alt = alt +1
    return mayor_diferencia

def similitud_porcentual(pix1,pix2,dimesiones):
    porcentaje_total = 0
    cantidad_pixeles = dimensiones[0]*dimensiones[1]
    valor_porcentual_pixel = float(100)/cantidad_pixeles
    valor_porcentual_rgb = valor_porcentual_pixel/3
    alt = 0
    while (alt<dimensiones[0]):
        anch=0
        while(anch<dimensiones[1]):
            if (pix1[alt,anch][0] == pix2[alt,anch][0]):
                porcentaje_total += valor_porcentual_rgb
            if (pix1[alt,anch][1] == pix2[alt,anch][1]):
                porcentaje_total += valor_porcentual_rgb
            if (pix1[alt,anch][2] == pix2[alt,anch][2]):
                porcentaje_total += valor_porcentual_rgb
            anch+=1
        alt+=1
    return porcentaje_total
    


def mutacionOriginal(img_eval, img_meta, dimensiones, prob_mutar):
    global generacion, limites
    y = 0
    pix1 = img_eval.load() #evaluada
    pix2 = img_meta.load() #imagen meta
    lista_result=[]
    while (y<dimensiones[1]):
        x = 0
        while (x<dimensiones[0]):
            """ R """
            if(pix1[x,y][0]<pix2[x,y][0]): #si la evaluada es menor que la meta
                lim = pix1[x,y][0]
                dif = random.randrange(lim,256)
                p = random.randrange(0,101)# random para delimitar si la mutación se hace
                if(lim +(256-dif) < limites[x][y][0][1] and (lim +(256-dif))>=pix2[x,y][0] and p<=prob_mutar):
                    r = lim + (256-dif)
                    limites[x][y][0][1] = r
                else:
                    r = lim
            elif(pix1[x,y][0]>pix2[x,y][0]): #si la evaluada es mayor que la meta
                lim = pix1[x,y][0]
                dif = random.randrange(0,lim)
                p = random.randrange(0,101)# random para delimitar si la mutación se hace
                if(lim - dif > limites[x][y][0][0] and (lim - dif <=pix2[x,y][0]) and p<=prob_mutar):
                    r = lim - dif
                    limites[x][y][0][0] = r
                else:
                    r = lim
            else:
                r = pix1[x,y][0]

            """ G """
            if(pix1[x,y][1]<pix2[x,y][1]): #si la evaluada es menor que la meta
                lim = pix1[x,y][1]
                dif = random.randrange(lim,256)
                p = random.randrange(0,101)# random para delimitar si la mutación se hace
                if (lim +(256-dif)<limites[x][y][1][1] and (lim +(256-dif))>=pix2[x,y][1] and p<=prob_mutar):
                    g = lim + (256-dif)
                    limites[x][y][1][1] = g
                else:
                    g = lim
            elif(pix1[x,y][1]>pix2[x,y][1]): #si la evaluada es mayor que la meta
                lim = pix1[x,y][1]
                dif = random.randrange(0,lim)
                p = random.randrange(0,101)# random para delimitar si la mutación se hace
                if (lim - dif > limites[x][y][1][0] and (lim - dif <=pix2[x,y][1]) and p<=prob_mutar):
                    g = lim - dif
                    limites[x][y][1][0] = g
                else:
                    g = lim
            else:
                g = pix1[x,y][1]

            """ B """
            if(pix1[x,y][2]<pix2[x,y][2]): #si la evaluada es menor que la meta
                lim = pix1[x,y][2]
                dif = random.randrange(lim,256)
                p = random.randrange(0,101)# random para delimitar si la mutación se hace
                if(lim+(256-dif)<limites[x][y][2][1] and (lim +(256-dif))>=pix2[x,y][2] and p<=prob_mutar):
                    b = lim + (256-dif)
                    limites[x][y][2][1] = b
                else:
                    b = lim
            elif(pix1[x,y][2]>pix2[x,y][2]): #si la evaluada es mayor que la meta
                lim = pix1[x,y][2]
                dif = random.randrange(0,lim)
                p = random.randrange(0,101)# random para delimitar si la mutación se hace
                if(lim-dif > limites[x][y][2][0] and (lim - dif <=pix2[x,y][1]) and p<=prob_mutar):
                    b = lim - dif
                    limites[x][y][2][0] = b
                else:
                    b = lim
            else:
                b = pix1[x,y][2]
            x = x + 1
            lista_result.append((r,g,b))
        y = y + 1
    gen_mutada = Image.new('RGB',dimensiones)
    gen_mutada.putdata(lista_result)
    gen_mutada.save(nombre_img+str(generacion)+".jpg")
    generacion = generacion +1

    return(gen_mutada)


def mutacion(img_eval, img_meta, dimensiones, prob_mutar,tamanno_poblacion):
    global generacion, limites
    y = 0
    pix1 = img_eval.load() #evaluada
    pix2 = img_meta.load() #imagen meta
    lista_result=[]
    while (y<dimensiones[1]):
        x = 0
        while (x<dimensiones[0]):
            aleatorio = random.randrange(0,tamanno_poblacion)
           
            r = random.randrange(limites[x][y][0][0],limites[x][y][0][1])
            g = random.randrange(limites[x][y][1][0],limites[x][y][1][1])
            b = random.randrange(limites[x][y][2][0],limites[x][y][2][1])
            if (aleatorio<=prob_mutar):
                """ R """
                r1 = random.randrange(0,tamanno_poblacion)
                if(r1<=100/prob_mutar):
                    if (pix2[x,y][0] in range(limites[x][y][0][0],r)):
                        limites[x][y][0][1] = r
                    elif (pix2[x,y][0] in range(r,limites[x][y][0][1])):
                        limites[x][y][0][0] = r
                """ G """
                r1 = random.randrange(0,tamanno_poblacion)
                if(r1<=100/prob_mutar):                
                    if (pix2[x,y][1] in range(limites[x][y][1][0],g)):
                        limites[x][y][1][1] = g
                    elif (pix2[x,y][1] in range(g,limites[x][y][1][1])):
                        limites[x][y][1][0] = g
                """ B """
                r1 = random.randrange(0,tamanno_poblacion)
                if(r1<=100/prob_mutar):
                    if (pix2[x,y][2] in range(limites[x][y][2][0],b)):
                        limites[x][y][2][1] = b
                    elif (pix2[x,y][2] in range(b,limites[x][y][2][1])):
                        limites[x][y][2][0] = b

            x = x + 1
            lista_result.append((r,g,b))
        y = y + 1
    gen_mutada = Image.new('RGB',dimensiones)
    gen_mutada.putdata(lista_result)
    gen_mutada.save(nombre_img+str(generacion)+".jpg")
    generacion = generacion +1

    return(gen_mutada)

def generar_mutacion(lista_img,img_meta,dimensiones,prob_mutar,tamanno_poblacion):
    pix1 = mutacion(lista_img[0],img_meta,dimensiones,prob_mutar,tamanno_poblacion) #evaluada
    lista_result=[]
    cont = 1
    lista_mutada = []
    lista_mutada.append(pix1)
    while(cont<len(lista_img)):
        rand = random.randrange(0,101)
        if(rand <= prob_mutar):
            img = lista_img[cont]
            img = pix1
            lista_mutada.append(img)
            cont+=1
        else:
            cont+=1
    return lista_mutada

def cruce_genes(img_1, img_2, dimensiones):
    cruce_1 = [] ## Primera matriz cruzada
    cruce_2 = [] ## Segunda matriz cruzada

    pix1 = img_1.load()
    pix2 = img_2.load()

    band = 0 #ahora y, bandera que está en 0 cuando tiene fila par, y en 1 cuando es impar
    
    y = 0
    while (y<dimensiones[1]):
        x = 0
        while(x<dimensiones[0]):
            if (y%2==0): #si la fila es par
                if (x%2==0): #si la columna es par
                    cruce_2.append(pix1[x,y])
                    cruce_1.append(pix2[x,y])
                else: #la columna es impar
                    cruce_1.append(pix1[x,y])
                    cruce_2.append(pix2[x,y])
            else: # la fila es impar
                if (x%2==0): #si la columna es par
                    cruce_1.append(pix1[x,y])
                    cruce_2.append(pix2[x,y])
                else: #la columna es impar
                    cruce_2.append(pix1[x,y])
                    cruce_1.append(pix2[x,y])
            x = x + 1
        y = y + 1
        #evalúo si la fila que viene es par, si lo es, inicio del 0, sino del 1
            
    result_1 = Image.new('RGB',dimensiones)
    result_1.putdata(cruce_1)
    result_2 = Image.new('RGB',dimensiones)
    result_2.putdata(cruce_2)
    return [result_1,result_2]

def cruce(img1, img2):
    dimensiones = img1.size
    pix1 = img1.load()
    pix2 = img2.load()
    img_creada1 = Image.new('RGB',dimensiones)
    img_creada2 = Image.new('RGB',dimensiones)
    largo = 0
    listaPix = []
    while (largo<(dimensiones[1])):
        ancho = 0
        while (ancho<dimensiones[0]):
            r = pix1[ancho,largo][0]
            g = pix1[ancho,largo][1]
            b = pix1[ancho,largo][2]
            listaPix.append((r,g,b))
            ancho = ancho + 1
        ancho = (dimensiones[0]/2)
        while (ancho<(dimensiones[0]/2)):
            r = pix2[ancho,largo][0]
            g = pix2[ancho,largo][1]
            b = pix2[ancho,largo][2]
            listaPix.append((r,g,b))
            ancho = ancho + 1
        largo = largo + 1
    img_creada1.putdata(listaPix)
    largo = 0
    listaPix = []
    while (largo<(dimensiones[1])):
        ancho = 0
        while (ancho<dimensiones[0]):
            r = pix2[ancho,largo][0]
            g = pix2[ancho,largo][1]
            b = pix2[ancho,largo][2]
            listaPix.append((r,g,b))
            ancho = ancho + 1
        ancho = (dimensiones[0]/2)
        while (ancho<(dimensiones[0]/2)):
            r = pix1[ancho,largo][0]
            g = pix1[ancho,largo][1]
            b = pix1[ancho,largo][2]
            listaPix.append((r,g,b))
            ancho = ancho + 1
        largo = largo + 1
    img_creada2.putdata(listaPix)
    return [img_creada1,img_creada2]





























