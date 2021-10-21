# Cargar la libreria numpy como np
import numpy as np
# Importar cv2 (la libreria del opencv)
import random
import cv2

dim = (1024, 1024)

# Se define la funcion para la creacion de la mascara de ruido en base al tamaño 
# de la imagen base
def sp_blur(image, prob, size, angle, masks):
    complete_mask = image
    for n in range(masks):
        noise = np.zeros(image.shape, np.uint8)
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                rdn = random.random()
                if rdn <= prob:
                    noise[i][j] = 255
                else:
                    noise[i][j] = image[i][j]
        cv2.imwrite("./Mask/noise.jpg", noise)
        # En esta parte se aplicara el blur y angulo a la imagen de ruido
        # y crear la mascara de lluvia
        k = np.zeros((size, size), dtype=np.float32)
        k[ (size-1)// 2 , :] = np.ones(size, dtype=np.float32)
        M = cv2.getRotationMatrix2D ((size / 2 , size / 2 ), angle, 1.0)
        MB = cv2.warpAffine(k, M, (size, size) ) 
        MB = MB * ( 1.0 / np.sum(MB) )
        rain = cv2.filter2D(noise, -1, MB)
        cv2.imwrite("./Mask/rain1.jpg", rain)
        maskv1 = cv2.filter2D(noise, -1, MB)
        maskv1 = maskv1[0:960,0:960]
        rainmask = cv2.GaussianBlur(maskv1,(3,3),1)
        rainmask = cv2.medianBlur(rainmask,3)
        rainmask = cv2.resize(rainmask, dim)
        complete_mask = cv2.addWeighted(complete_mask, 1,rainmask,0.9,0)
    return complete_mask


