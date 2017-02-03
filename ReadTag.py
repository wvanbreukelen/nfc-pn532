import sys
import ConfigReader
import time
import random
import datetime
import RPi.GPIO as GPIO
from Buttons import Activity
from NFC import NFC
from DB import DB


# NFC Python library voor PN532 microcontroller importeren
# Bron: https://github.com/adafruit/Adafruit_Python_PN532/
try:
    import Adafruit_PN532 as PN532
except Exception:
    print("PN523 library niet gevonden!")
    sys.exit()

# Te lezen datablocks en hun bijbehorende prefix
readDatablocks = {1: 'ID'}

# Logged in buffer
loggedInBuffer = []

# GPIO button toewijzing
buttonAssignment = [
	[4, '1'],
	[17, '2'],
	[27, '3'],
	[22, '4']
]

# GPIO configuratie ophalen
GPIO_CF = ConfigReader.GetGPIOConfig()

# Knoppen configureren
btnAct = Activity()

# Servomotor configureren
GPIO.setmode(GPIO.BCM)
GPIO.setup(8, GPIO.OUT)
servo = GPIO.PWM(8, 50)

# Alle knoppen registreren
for listing in buttonAssignment:
	btnAct.bindButton(listing[0], listing[1])

# Sleutel ophalen
key = ConfigReader.GetTagKey()

# Nieuwe instantie aanmaken van de PN532 klasse
ctl = PN532.PN532(
 cs   = GPIO_CF['CS'],
 sclk = GPIO_CF['SCLK'],
 mosi = GPIO_CF['MOSI'],
 miso = GPIO_CF['MISO']
)

# Database initialiseren
db = DB('192.168.42.1', 'nfc', 'P@ssw0rd', 'sportschool')
#db = DB('172.27.224.14', 'nfc', 'P@ssw0rd', 'sportschool')
# NFC instantie aanmaken
nfc = NFC(ctl, key)

nfc.begin()

print("Plaats NFC tag op lezer...")

# Wacht totdat er een NFC tag gevonden is
while True:
    # Resultaat dict
    tag = {}

    # Geldigheid tag
    valid = True

    # Probeer een tag te lezen. Is de lezing succesvol, toon melding
    if not nfc.scan():
        continue

    print("NFC tag gevonden! Lezen...")

    for block, prefix in readDatablocks.items():

        try:
            tag.update(nfc.read(block, prefix))
        except Exception as e:
            print('Er is een fout opgetreden: ' + str(e))
            valid = False
	    continue

    print(tag)

    if valid:
        pass
        # Database record invoegen

	# Random locatie nummer!
	locationNr = random.randint(1, 6)

    activityNr = btnAct.waitForPress()

    print("Activiteit: {0}".format(activityNr))

	# Activiteitnummer random, moet later van knoppen komen
    # activityNr = random.randint(1, 6)
	
    curTime = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    item = [tag['ID'], activityNr]

    if item in loggedInBuffer:
	print("Uitloggen...")
	servo.start(6.0)
	time.sleep(1)
	servo.stop()

	db.runQuery('UPDATE machine_activiteit SET endTimestamp = "{}" WHERE klantnummer = {} AND activiteitnummer = {} ORDER BY startTimestamp LIMIT 1'.format(curTime, tag['ID'], activityNr))
	loggedInBuffer.remove([tag['ID'], activityNr]) 
    else:
	print("Inloggen...")
	servo.start(6.0)
	time.sleep(1)
	servo.stop()

    	db.runQuery('INSERT INTO machine_activiteit (klantnummer, locatienummer, activiteitnummer) VALUES ({}, {}, {})'.format(tag['ID'], locationNr, activityNr))
	loggedInBuffer.append([tag['ID'], activityNr])

    db.save()

    # Aan logged in buffer toevoegen
    #loggedInBuffer[] = tag['ID']

    print(loggedInBuffer)

    time.sleep(1)
