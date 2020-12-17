import paho.mqtt.client as mqtt
import sys
import mysql.connector

#callback kun client vastaanottaa servulta connack
def on_connect(client, userdata, flags, rc):
        print("Connected: "+str(rc))

        client.subscribe("TVTLukko")
#callback kun saadaan publish msg palvelimerlta
def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        #topikki = msg.topic
        sql = "INSERT INTO lukontila(id,tila,msg,aika) VALUES(NULL,%s,%s ,CURRENT_TIMESTAMP);"
        sql = "INSERT INTO logi(id,tila,msg,aika) VALUES(NULL,%s,%s ,CURRENT_TIMESTAMP);"
        val =(msg.topic, str(msg.payload))
#tallennetaan sql
        try:
                cursor.execute(sql, val)
                mydb.commit()
                print("Save to the db ... OK")
        except:
                mydb.rollback()
                print("Save to Database ... Failed")

try:
 mydb = mysql.connector.connect(host='localhost',database='codeigniter',user='codeigniter',password='redhat')
except:
        print("Failed to connect to database")
        sys.exit()
#valmistellaan kursori. Kursori toteuttaa kyselyja sql:ss
cursor = mydb.cursor()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
try:
        client.connect("broker.hivemq.com", 1883, 60)
except:
        print("Couldn't connect to MQTT Broker...")
        print("stop...")
        sys.exit()


try:
        client.loop_forever()
except KeyboardInterrupt:  #ctrl+C
        print("Stop...")
        db.close()
