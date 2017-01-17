import sys
import ConfigReader
import time
from NFC import NFC

# NFC Python library voor PN532 microcontroller importeren
# Bron: https://github.com/adafruit/Adafruit_Python_PN532/
try:
    import Adafruit_PN532 as PN532
except Exception:
    print("PN523 library niet gevonden!")
    sys.exit()

# Te lezen datablocks en hun bijbehorende prefix
readDatablocks = {1: 'ID', 2: 'BA'}

# GPIO configuratie ophalen
GPIO_CF = ConfigReader.GetGPIOConfig()

# Sleutel ophalen
key = ConfigReader.GetTagKey()

# Nieuwe instantie aanmaken van de PN532 klasse
ctl = PN532.PN532(
 cs   = GPIO_CF['CS'],
 sclk = GPIO_CF['SCLK'],
 mosi = GPIO_CF['MOSI'],
 miso = GPIO_CF['MISO']
)

# NFC instantie aanmaken
nfc = NFC(ctl, key)

nfc.begin()

print("Plaats NFC tag op lezer...")

# Wacht totdat er een NFC tag gevonden is
while True:
    # Resultaat dict
    result = {}

    # Probeer een tag te lezen. Is de lezing succesvol, toon melding
    if not nfc.scan():
        continue

    print("NFC tag gevonden! Lezen...")

    for block, prefix in readDatablocks.items():

        try:
            print(nfc.read(block, prefix, False))
        except Exception as e:
            print('Er is een fout opgetreden: ' + str(e))

        #result.update({prefix: fmtData})

        #print(result)

    time.sleep(1)
