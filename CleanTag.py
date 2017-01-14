import sys
import ConfigReader
import time
import NFC

# NFC Python library voor PN532 microcontroller importeren
# Bron: https://github.com/adafruit/Adafruit_Python_PN532/
try:
    import Adafruit_PN532 as PN532
except Exception:
    print("PN532 library niet gevonden!")
    sys.exit()

# Te legen datablocks
emptyDatablocks = {1: 'ID', 2: 'BA'}

# Elke NFC tag bestaat uit verschillende sectoren (in ons geval 16) waarin een bepaalde hoeveelheid data in opgeslagen kan worden.
# Om de data te kunnen lezen/schrijven is er een unieke sleutel nodig. Standaard staat deze sleutel op zes FF bytes

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

nfc = NFC.NFC(ctl, key)

# Maak connectie met de PN532 controller
nfc.begin()

print("Plaats NFC tag op lezer...")

# Wacht totdat er een NFC tag gevonden is
while True:
    # Probeer een tag te lezen. Is de lezing succesvol, toon melding
    if nfc.scan():
        print("NFC tag gevonden! Verplaats deze niet...")
        break

# Tijd toevoegen zodat de tag juist geplaatst kan worden.
time.sleep(2)

for block, prefix in emptyDatablocks.items():
    nfc.clean(block, prefix)

print('NFC tag schoongemaakt!')
