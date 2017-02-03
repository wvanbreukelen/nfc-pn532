import sys
import time
import ConfigReader
import NFC

# NFC Python library voor PN532 microcontroller importeren
# Bron: https://github.com/adafruit/Adafruit_Python_PN532/
try:
    import Adafruit_PN532 as PN532
except Exception:
    print("PN523 library niet gevonden!")
    sys.exit()

# Te schrijven datablocks en hun bijbehorende prefix
writeDatablocks = {1: 'ID'}

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

nfc = NFC.NFC(ctl, key)

# Maak connectie met de PN532 controller
nfc.begin()

while True:
    print("Plaats NFC tag op lezer...")

    # Wacht totdat er een NFC tag gevonden is
    while True:
        # Probeer een tag te lezen. Is de lezing succesvol, toon melding
        if nfc.scan():
            print("NFC tag gevonden! Verplaats deze niet...")
            break

    choice = None

    for block, prefix in writeDatablocks.items():

        while choice is None:
            # Check voor integer
            try:
                choice = int(raw_input("Voer {0} in: ".format(prefix.upper())))
            except ValueError, NameError:
                print("Geen nummer, probeer opnieuw!")
                continue

        nfc.write(block, prefix, choice)

        choice = None

    print('Tag geschreven!')


    time.sleep(2)
