import cv2
#kirjasto joka tunnistaa esimerkiksi muotoja, värejä ja vertailee kuvia
from picamera.array import PiRGBArray              #Kirjastojen kutsumistsa/sisällytystä
#kolmiulotteinen RGB ryhmä jossa rivit sarakkeet ja värit.. Tämä otetaan koodaamattomasta RGB-sieppauksesta
#lukee kehyksiä raspin kamerasta NumPy matriiseina.
from picamera import PiCamera
#kameran kirjasto
import numpy as np
#kirjasto jossa toimintoja lineaarisen algebran, fourier muunnoksen ja matriisien toiminta-alueella
#kasvojen tunnistuksessa käytetään matriisien toimintoja
import os
#moduuli joka antaa toimintoja luoda/poistaa hakemistoja/kansioita, hakea sisältöjä tai muuttaa ja tunnistaa hakemiston.
import sys
#moduuli joka tarjoaa pääsyn "rootin?" käyttämiin ja ylläpitämiin juttuihin
import time
#ajan kirjasto

camera = PiCamera()
#määritellään kamera
camera.resolution = (640, 480) #pikselien määrät
camera.framerate = 30 #kuvannoupeus, montako kuvaa sekunnissa
camera.rotation = 180 #kameran kääntäminen

rawCapture = PiRGBArray(camera, size=(640, 480))  #Kameran object & resolution
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml") #Ladataan cascade-tiedosto
#tunnistusta varten
#Cascade määrittelee kuvan osat pala kerrallaan

nimi = input("Kerro nimi\n")
nHakemisto = "/home/pi/kasvojentunnistus/kuvat/" + nimi
print(nHakemisto)
if not os.path.exists(nHakemisto): #katsotaan onko hakemisto olemassa jos ei luodaan sellainen
        os.makedirs(nHakemisto)
        print("Hakemisto luotu")
else:
        print("Hakemisto on jo olemassa")
        sys.exit()
        
print("Katso kameraan ja odota..")


count = 1
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
#capture.continous funktio alkaa lukemaan freimejä kamerasta. Muutetaan opencv:tä varten formaatti bgr:ksi
#kohdellaan streamia kuten videota
                if count > 30:
                    break
                frame = frame.array  #frame.arrayn avulla päästään NumPyyn käsiksi             
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #asetetaan kuvat harmaansävyihin
                faces = faceCascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 5)
#Faces = kutsutaan luokittelijafunktiota havaitsemaan kasvoja freimissä. Ensin käsitellään harmaansävykuva.
#        scalefactor määrittää kuinka paljon kuvan koko vähenee jokaisella kuvan skaalauksessa.
#        minNeighbors määrittää kuinka monta "naapuria" jokaisen "palaehdokkaan" täytyisi säilyttää
                for(x,y,w,h) in faces: #koordinaatit kasvoille
                    roiGray = gray[y:y+h, x:x+w] #pilkotaan kuvat y/x akseleihin ja määritellään harmaiksi
                    tiedostonNimi = nHakemisto + "/" + nimi + str(count) + ".jpg" #luodaan tiedosto
                    cv2.imwrite(tiedostonNimi, roiGray)#luodaan tiedostn sisäinen kuva
                    cv2.imshow("face", roiGray) #prinntataan tapahtumaa
                    cv2.rectangle(frame,(x,y), (x+w, y+h), (0, 255, 0), 2)
                    count += 1 #lisää kuvia hakemistoon

                cv2.imshow('frame', frame) #Näytetään alkuperäinen freimi outputissa. cv2.waitkey() on näppäimistön
                key = cv2.waitKey(1)       #sidontafunktio. Se odottaa määrätyn ms ajan näppäimistölta toimintaa. Ottaa yhden
                rawCapture.truncate(0)     #argumentin ja tämä on se aika millisekunteina. Jos näppäintä painetaan sillä ajalla
                                            # ohjelma jatkuu. Jos 0, se odottaa äärettömän ajan näppäintä. Sitten nollataan
                                            # streami kutsumalla truncate(0) rajaamisien välissä ja ollaan valmiina seuraavaa steamiin.
        
print("Tunnistettavat kasvot luotu")        
cv2.destroyAllWindows()  
