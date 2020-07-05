# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 21:02:14 2020

@author: Thamara Montero Montoya
Carne: B64577
"""

import numpy as np 
import matplotlib.pyplot as plt
from scipy import integrate
import pandas as pd
from scipy import signal

datos_bits = pd.read_csv('bits10k.csv', header = None)

bits = np.array(datos_bits)


N=len(bits)


#1. Esquema de modulación BPSK para los bits presentados.

f = 5000 #frecuencia en la portadora

T = 1/f #período

p = 50 #puntos de muestreo

tp = np.linspace(0, T, p) #puntos de muestreo para cada período

sen = np.sin(2*np.pi*f*tp) #onda de la portadora

#grafica onda
plt.plot(tp, sen)
plt.xlabel('Tiempo / s')
plt.ylabel('Amplitud de la onda')
plt.title('Forma de la onda portadora')
plt.show()

fs = p/T #frecuencia de muestreo

t = np.linspace(0, N*T, N*p) #Creación de la línea temporal para toda la señal Tx

senal = np.zeros(t.shape) #Inicializar el vector de la señal modulada Tx

#Señal modulada BPSK
for k, b in enumerate(bits):
    senal[k*p:(k+1)*p] = sen if b else -sen
    
#Visualización de los primeros bits modulados
pb = 15
plt.figure(1)
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud de la señal")
plt.title("Muestra de los primeros " + str(pb) + " periodos de la señal modulada")
plt.plot(senal[0:pb*p])
plt.show()


#2. Potencia promedio

P_inst = senal**2 #Potencia instantánea
P_prom = integrate.trapz(P_inst, t) / (N*T) #Potencia promedio a partir de la potencia instantánea
print ('La potencia promedio corresponde a: ' + str(P_prom))



#3. Simular un canal ruidoso del tipo AWGN (ruido aditivo blanco gaussiano) con una relación señal a ruido (SNR) desde -2 hasta 3 dB.
rang_snr = list(range(-2,4))
BER = []
for SNR in rang_snr:
    Pn = P_prom/ (10**(SNR / 10)) #Potencia del ruido para SNR y potencia de la señal dadas
    sigma = np.sqrt(P_prom) # Desviación estándar del ruido
    ruido = np.random.normal(0, sigma, senal.shape) #Crear ruido (Pn = sigma^2)
    Rx = senal + ruido #Simular "el canal": señal recibida
    
    #Visualización de los primeros bits recibidos
    pb = 15
    plt.figure(2)
    plt.plot(Rx[0:pb*p])
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud de la señal")
    plt.title("Canal ruidoso en el rango de SNR entre -2dB y 3dB.")
    plt.show()


#4. Graficar la densidad espectral de potencia de la señal con el método de Welch (SciPy), antes y después del canal ruidoso.

# Antes del canal ruidoso
    fw, PSD = signal.welch(senal, fs, nperseg=1024)
    plt.figure(3)
    plt.semilogy(fw, PSD)
    plt.xlabel('Frecuencia / Hz')
    plt.ylabel('Densidad espectral de potencia / V**2/Hz')
    plt.title("Densidad espectral de potencia antes del canal ruidoso")
    plt.show()

# Después del canal ruidoso
    fw, PSD = signal.welch(Rx, fs, nperseg=1024)
    plt.figure(4)
    plt.semilogy(fw, PSD)
    plt.xlabel('Frecuencia / Hz')
    plt.ylabel('Densidad espectral de potencia / V**2/Hz')
    plt.title("Densidad espectral de potencia despues del canal ruidoso")
    plt.show()



#5. Demodular y decodificar la señal y hacer un conteo de la tasa de error de bits (BER, bit error rate) para cada nivel SNR.


    Es = np.sum(sen**2)#Pseudo-energía de la onda original
    bitsRx = np.zeros(bits.shape) #Inicialización del vector de bits recibidos

#Decodificación de la señal por detección de energía
    for k, b in enumerate(bits):

        Ep = np.sum(Rx[k*p:(k+1)*p] * sen)
        if Ep > Es/2:
            bitsRx[k] = 1
        else:
            bitsRx[k] = 0
    
    err = np.sum(np.abs(bits - bitsRx))
    ber = err/N

    BER.append(ber)
    
    print('Hay un total de {} errores en {} bits para una tasa de error de {}.'.format(err, N, ber))
    

#6. Graficar BER versus SNR.

plt.figure(5)
plt.scatter(rang_snr, BER)
plt.xlabel("SNR (dB)")
plt.ylabel("BER")
plt.title("BER en función del SNR")



