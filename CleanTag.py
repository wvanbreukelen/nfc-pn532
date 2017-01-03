import sys
import ConfigReader
import time

# NFC Python library voor PN532 microcontroller importeren
# Bron: https://github.com/adafruit/Adafruit_Python_PN532/
try:
    import Adafruit_PN532 as PN532
except Exception:
    print("PN523 library niet gevonden!")
    sys.exit()

# Te legen datablocks
emptyDatablocks = [1]

# Elke NFC tag bestaat uit verschillende sectoren (in ons geval 16) waarin een bepaalde hoeveelheid data in opgeslagen kan worden.
# Om de data te kunnen lezen/schrijven is er een unieke sleutel nodig. Standaard staat deze sleutel op zes FF bytes

GPIO_CF = ConfigReader.GetGPIOConfig()

# Nieuwe instantie aanmaken van de PN532 klasse
ctl = PN532.PN532(
 cs   = GPIO_CF['CS'],
 sclk = GPIO_CF['SCLK'],
 mosi = GPIO_CF['MOSI'],
 miso = GPIO_CF['MISO']
)

# Maak connectie met de PN532 controller
ctl.begin()

# Configuratie instellen op PN532
ctl.SAM_configuration()

print("Plaats NFC tag op lezer...")

# Wacht totdat er een NFC tag gevonden is
while True:
    # Probeer een tag te lezen. Is de lezing succesvol, toon melding
    t_id = ctl.read_passive_target()

    if t_id != None:
        print("NFC tag gevonden! Verplaats deze niet...")
        break

time.sleep(1)

# Maak leeg datapakket
data = bytearray(16)


for block in emptyDatablocks:
    # Gebruik sleutel om datasector vrij te geven voor schrijven
    if not ctl.mifare_classic_authenticate_block(t_id, block, PN532.MIFARE_CMD_AUTH_B, ConfigReader.GetTagKey()):
        print('Fout! Kan niet authoriseren met NFC tag op block {0}. Probeer het nog eens.'.format(block))
        sys.exit(0)

    # Leeg NFC block
    ctl.mifare_classic_write_block(block, data);

print('NFC tag schoongemaakt!')
