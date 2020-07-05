# Tarea4
Modelos Probabilísticos de señales y sistemas.

Thamara Montero Montoya. B64577.

Asignaciones de la tarea 4.


# Esquema de modulación BPSK para los bits presentados. 
Para realizar el esquema de modulación BPSK se cuenta con un archivo de tipo *.csv* del cual se leen los datos, en este caso, correspondientes a los bits a utilizar para el resto de código.

Según el enunciado se debe hacer uso de una frecuencia de 5000Hz por lo que se establece así y se toman 50 puntos de muestreo. Además se sabe que se debe implementar una onda portadora senoidal unitaria por lo que se define la onda portadora de la siguiente forma:

`sen = np.sin(2*np.pi*f*tp)` 

Y se obtiene la siguiente figura:


![](Onda_portadora.png)

Ahora, para la modulación BPSK se define primero el vector de la señal modulada *senal*, y se define la señal modulada BPSK de la siguiente forma:

```
for k, b in enumerate(bits):
  senal[k*p:(k+1)*p] = sen if b else -sen
```

Se define visualizar los primeros 15 periodos y se obtiene la siguiente figura:

![](Primeros_periodos.png)


# Potencia promedio de la señal modulada generada.
```
P_inst = senal**2 #Potencia instantánea
P_prom = integrate.trapz(P_inst, t) / (N*T) #Potencia promedio a partir de la potencia instantánea
print ('La potencia promedio corresponde a: ' + str(P_prom))
```
Donde la potencia promedio, corresponde a 0.4900009800019598.


# Canal ruidoso del tipo AWGN (ruido aditivo blanco gaussiano) con una relación señal a ruido (SNR) desde -2 hasta 3 dB.

## SNR = -2

## SNR = -1

## SNR = 0

## SNR = 1

## SNR = 2

## SNR = 3

# Grafica de la densidad espectral de potencia de la señal con el método de Welch, antes y después del canal ruidoso.


# Demodulación y decodificación de la señal y  conteo de la tasa de error de bits (BER, bit error rate) para cada nivel SNR.


# Grafica de BER versus SNR.
