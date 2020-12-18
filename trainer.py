import os
#moduuli joka antaa toimintoja luoda/poistaa hakemistoja/kansioita, hakea sisältöjä tai muuttaa ja tunnistaa hakemiston.
import numpy as np
#kirjasto jossa toimintoja lineaarisen algebran, fourier muunnoksen ja matriisien toiminta-alueella
#kasvojen tunnistuksessa käytetään matriisien toimintoja
from PIL import Image
#kuvan käsittelyominaisuudet, laaja tiedostomuototuki
import cv2
#kirjasto joka tunnistaa esimerkiksi muotoja, värejä ja vertailee kuvia
import pickle
#moduuli joka työstää binääristen protokollien sarjoittamista ja epäsarjoittamista
#prosessissa python objektit muutetaan tavuvirraksi (eli binaaritiedostksi tai tavua muistuttavaksi objektiksi) tai toisinpäin
#Kirjastojen kutsumistsa/sisällytystä

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades +"haarcascade_frontalface_default.xml")
#Ladataan cascade-tiedosto tunnistusta varten
#Cascade määrittelee kuvan osat pala kerrallaan
recognizer = cv2.face.LBPHFaceRecognizer_create()
#käytetään kasvojen tunnistukseen LBPH- pakettia joka on OpenCV kirjastossa

baseDir = os.path.dirname(os.path.abspath(__file__)) #projektin hamkemisto / (__file__) = moduulin tiedostonnimi 
imageDir = os.path.join(baseDir, "kuvat") #määritellään kuvien hakemistot ja siirrytään niihin

currentId = 1 #aloittava id numero nimelle
labelIds = {} #nimen ja id yhdistys
yLabels = [] # taulukko kertoo xTrain taulukon datan tiedot
xTrain = []  #taulukko opetuskuvadataa 

for root, dirs, files in os.walk(imageDir): #siirrytään kuvahakemistoon, jos kuvia on kuvat muutetaan Numpy-taulukoiksi
    print(root, dirs, files) #pääkäyttäjä, hakemisto polussa ja printataan kuvienomat kansiot
    for file in files: 
        print(file) #printataan kuvien oman hakemiston kuvatiedostot
        if file.endswith("png") or file.endswith("jpg"): 
            path = os.path.join(root, file) #tiedoston polun määritteleminen
            label = os.path.basename(root) #saadaan perusnimi määritetylle kuvakirjaston polulle
            print(label)

            if not label in labelIds: #määritellään kasvoille omat id numerot jos kasvoja on useampi
                labelIds[label] = currentId
                print(labelIds)
                currentId += 1

            id_ = labelIds[label] #id määritellään sisällyttämällä label labelid
            pilImage = Image.open(path).convert("L") #muokataan kuvaa ja palauttaa kopion tästä kuvasta
            imageArray = np.array(pilImage, "uint8") #muutetaan NumPy taulukon matriiseiksi
            faces = faceCascade.detectMultiScale(imageArray, scaleFactor=1.1, minNeighbors=5)
            #kasvojen tunnistus tehdään uudelleen ja varmistetaan että kuvat ovat oikeita
            #tämän jälkeen valmistellaan trainingdata koordinaattien ja akselien avulla
            for (x, y, w, h) in faces:  #käydään läpi kasvot koordinaateittain
                roi = imageArray[y:y+h, x:x+w] #määritelläään roi -> xy-akseleittain ja tallennetaan xTrain taulukon jatkoksi ja yLabelsille tallennetaan id-muuttujan arvo joka vastaa kuvaa
                xTrain.append(roi)
                yLabels.append(id_)
with open("labels", "wb") as f: #avataan tiedpsto kirjoitettavasksi binäärimuodossa
    pickle.dump(labelIds, f) #sisällytetään/tallennetaan labelIds labels tiedostoon 
    f.close() #suljetaan tiedosto
#opetetaan tunnistamaan ja tallennetaan data trainer.yml tiedostoon
recognizer.train(xTrain, np.array(yLabels)) #treenataan kasvot ja tallennetaan yml tiedostoksi 
recognizer.save("trainer.yml")
print(labelIds) #printataan id ja nimet jotka kuuluvat yhteen
