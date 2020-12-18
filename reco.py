import cv2
#kirjasto joka tunnistaa esimerkiksi muotoja, värejä ja vertailee kuvia
from picamera.array import PiRGBArray
#kolmiulotteinen RGB ryhmä jossa rivit sarakkeet ja värit.. Tämä otetaan koodaamattomasta RGB-sieppauksesta
#lukee kehyksiä raspin kamerasta NumPy matriiseina
from picamera import PiCamera
#kameran kirjasto
import numpy as np
#kirjasto jossa toimintoja lineaarisen algebran, fourier muunnoksen ja matriisien toiminta-alueella
#kasvojen tunnistuksessa käytetään matriisien toimintoja
import pickle
#moduuli joka työstää binääristen protokollien sarjoittamista ja epäsarjoittamista
#prosessissa python objektit muutetaan tavuvirraksi (eli binaaritiedostksi tai tavua muistuttavaksi objektiksi) tai toisinpäin
from time import sleep
#"aikakirjasto"
import paho.mqtt.client as paho
#paho mqtt kirjaston sisälyttäminen mqtt viestejä varten
#Kirjastojen kutsumistsa/sisällytystä

broker="broker.hivemq.com" #borkerin osoite
port=1883 
def on_publish(client,userdata,result):             #callbackille funktio
    pass
client1= paho.Client("control1")                           #yhteydelle nimi
client1.on_publish = on_publish                          #publish funktio
client1.connect(broker,port)                                 #luodaan yhteys


#avataan "sanastot", joka sisältää pickle tiedoston
with open('labels', 'rb') as f:
    dicti = pickle.load(f)
    f.close()
#määritellään kamera (resoluutio, frame, käännetään kuva, raakaotoksen koko)
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
camera.rotation = 180
rawCapture = PiRGBArray(camera, size=(640, 480))


faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")
#ladataan cascade-tiedosto, luokittelija/tunnistin joka tunnistaa kasvot ja training koodilla saadut tiedot
#luetaan kehykset ja muunnetaan kuvattavaa harmaaksi ja etsitään kasvot. Jos kuvassa huomataan kasvot otetaan
#kuva ja verrataan tätä kuvaa tunnistettaviin kasvoihin tunnistimella
#käytetään kasvojen tunnistukseen LBPH- pakettia joka on OpenCV kirjastossa
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True): 
    frame = frame.array
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #kuvanmuokkaus
    faces = faceCascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 5)
# Faces = kutsutaan luokittelijafunktiota havaitsemaan kasvoja freimissä. Ensin käsitellään harmaansävykuva.
#        scalefactor määrittää kuinka paljon kuvan koko vähenee jokaisella kuvan skaalauksessa.
#        minNeighbors määrittää kuinka monta "naapuria" jokaisen "palaehdokkaan" täytyisi säilyttää
    cv2.imshow('tunnistus', frame) #tulostetaan kehys ja nimetään se
    key = cv2.waitKey(1)
    rawCapture.truncate(0) #tyhjennetään streami, jotta voidaan valmistua seuraavaan kehykkseen
    for (x, y, w, h) in faces: #käydään koordinaateittain läpi
        roiGray = gray[y:y+h, x:x+w] #otetaan pikselit Gray kuvamatriisista x/y-akseleiden ja sijoitetaan ne roiGary
        id_, conf = recognizer.predict(roiGray)#tunnistin ennustaa käyttäjän tunnuksen ja ennusteen luottamuksen
#etsitään läpi "sanastosta" idlle ja kuvalle yhtäläisyys, jos kuvan henkilöt tunnistetaan
#printataan "kasvot löydetty" kun täämä on käsitelty ja kasvot on löydetty ja kameran ikkunan voi sulkea
        for nimi, value in dicti.items():
            if value == id_:
                print("kasvot löydetty")
         
        if conf <= 80:
            #tarkistetaan onko kuvien välillä tarpeeksi samanlaisuutta jos cof on alle 80 lähetetään arduinolle viesti
            #oven avautumisesta
            print("pääsy sallittu")
            client1.publish("Tunnistettu","1")
            if client1.publish("Tunnistettu","1"):
                print("viesti lähetetty")
                exit()
    
        else:
            print("pääsy hylätty")
            client1.publish("Tunnistettu","0")
            if client1.publish("Tunnistettu","0"):
                print("viesti lähetetty")
                exit()
            #muussa tapauksessa hylkäys viesti lähetetään
