# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 18:53:45 2021

@author: titit
"""
from PIL import Image
import os
import decimal
from Rain_maker_blur import *
from matplotlib import pyplot as plt


"""Dimension que se usara para redimensionar imagenes y tener una mejor 
area de trabajo"""
dim = (1024, 1024)

# Se importara la imagen en negro que servira para crear la mascara de lluvia
base = cv2.imread("blank.png",0)
base = cv2.resize(base, dim, interpolation = cv2.INTER_AREA)

#Se añadira el directorio de las imagenes a usar
Path = "./ground_truth"
"""Se seleccionara una imagen del directorio en este caso se tienen
# imagenes con nombres desde 1 hasta 1000 modificable a gusto"""

# Se crea el kernel para crear el difuminado de las rayas de lluvia
kernel = np.ones((5,5),np.float32)/20

for i in range(1,3):
    """Seleccion de la imagen a modificar (en este caso se usan imagenes
    enumeradas, por lo cual se usa un ciclo for para modificar varias 
    imagenes a la vez), esta de la misma manera se redimensiona a 1024x1024 
    pixeles para tener una mejor area de trabajo"""
    image_to_mod = i 
    ori = cv2.resize(cv2.imread(Path+"/"+str(image_to_mod)+".jpg"),dim)
    nparray1=np.array(ori)
    cv2.imwrite('./resize/'+str(image_to_mod)+'.jpg', ori )
    
    """Se le dice al codigo cuantas subcapas(layers) tendra la mascara de 
    lluvia completa, esto para causar un mejor efecto"""
    n_mask = 10
    
    # Se selcciona la cantidad de submascaras y el ángulo de lluvia a usar
    random_g = random.randint(1, 100)
    if random_g % 2 == 0:
        random_angle = random.randint(40, 70)
    else:
        random_angle = random.randint(110, 140)
        
    # Se seleccionara el la probabilidad de aplicar ruido 
    # de sal y pimienta y su tamaño
    noise_ramdom = float(decimal.Decimal(random.randrange(15, 30))/10000)
    random_size = random.randint(12,40)
    
    # Se manda a llamar a la funcion creada
    complete_mask = sp_blur(base, noise_ramdom, random_size, random_angle, n_mask)
    
    # Se almacena la mascara de lluvia creada para su uso posterior
    cv2.imwrite("./Mask/"+str(image_to_mod)+".jpg", complete_mask)
    rain_mask_read = cv2.imread("./Mask/"+str(image_to_mod)+".jpg")
    rain_mask_read = cv2.Sobel(rain_mask_read,cv2.CV_8U,1,0,ksize=3)
    
    # Se aplica un filtro en base al kernel declarado para crear el difuminado
    rain_mask_read = cv2.filter2D(rain_mask_read,-1,kernel)
    
    """ Se redimensiona la mascara de lluvia al tamaño de la imagen a modificar
    para aplicarla completamente"""
    rain_mask_read = cv2.resize(rain_mask_read,dim)
    rainy_img = cv2.addWeighted(ori, 0.9,rain_mask_read,2.5,1)
    
    # Se almacena la imagen modificada para su uso como imagen con lluvia sintetica
    cv2.imwrite("./nmethod/"+str(image_to_mod)+".jpg", rainy_img)
    
    """ Se hace un reset a la mascara de lluvia para crear una nueva en caso de 
    realizar varias a la vez"""
    complete_mask= base

    
    
    
    
    
    
    
    
    
    
    
    
    
    