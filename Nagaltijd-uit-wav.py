# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 12:17:10 2024

@author: Merlijn, Dirk
"""

import wave, struct
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from math import log10

wavefile = wave.open("J12,2.wav")
#opent de file en leest de data punten, dit zijn 44100 per seconden
length = wavefile.getnframes()
# het vertelt hoeveel frames het bestand heeft
sample_rate, data = wavfile.read('J12,2.wav')
# de sample data (nutteloze data) word gesplitst van de nuttige data
# de nutteloze data link je aan "sample rate"
ydata = []
# is een lijst
td = -1
# zo garandeer je dat je begint bij 0
gemdata = []
# een lijst met de gemiddelde data
tstart = 0
teind = 0
som = 0
# het totaal van de laatste 11025 datapunten

for i in range(0, length):
    #geeft de range van de frames in de file, van 0 tot frames
    wavedata = wavefile.readframes(1)
    #leest
    data = struct.unpack("<h", wavedata)
    # de data word omgezet in leesbare waarde
    y = data[0]
    #lijst
    
    if y == 0:
        ydata.append(-60)
        continue
    # continue betekend dat als y == 0; 
    # alles er onder word genegeerd en dat hij opnieuw begint bij de eerste loop 

    y = 20*log10(abs(y)/2**15) 
    # formule om de waardes (intensiteit) om te zetten naar decibel
    ydata.append(y)
    
    if i >= 11025:
        # een goede balans tussen de lijn goed te kunnen zien
        # en de lijn niet hobbelig word
        som += ydata[i]
        som -= ydata[i-11025]
        gemdata.append(som/11025)
        # elke keer dat hij een kwart seconden toevoegt haalt hij de eerste 
        # kwart seconden weg zodat de som altijd 11025 elementen bevat
        
    else:
        som += ydata[i]
        gemdata.append(som/(i+1))
        # voor elke datapunt word opnieuw het gemiddelde berekend, 
        # elke kwart seconde (11025 datapunten)
    
    te = round(i/44100, 1)
    if te != td:
        print(str(te)+"s verwerkt")
        td = te
    # laat de progress bar zien    
    
for i in range(len(gemdata)):
    if i >= 22050 and tstart == 0:
        dbstart = gemdata[22050]
        if gemdata[i] <= dbstart - 3 and gemdata[i] >= dbstart - 3.1:
            tstart = i
    if i >= 22050 and teind == 0:
        if gemdata[i] <= dbstart - 13 and gemdata[i] >= dbstart - 13.1:
            teind = i
            break
    # berekend wanneer de decibel met 10 db is gedaald
    # en de break zorgt er voor dat de loop is gestopt
    
t = (teind - tstart)/44100
#hij kijkt naar het totaal aantal frames en deelt het door 44100 om seconden te krijgen
print("nagalmtijd is " + str(6*t))
#omdat je een beschil van 10 db neemt moet je hem keer 6 nemen om op de 60 te komen

x = np.linspace(0, len(gemdata)/44100, len(gemdata)) 
# maakt een lijst van je data en zet het om in seconden  
plt.plot(x,gemdata)
# plot een grafiek
plt.show()
# show grafiek

