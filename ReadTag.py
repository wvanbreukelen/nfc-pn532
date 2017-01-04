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

# Te lezen datablocks en hun bijbehorende prefix
readDatablocks = {1: 'ID'}

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

    # Resultaat dict
    result = {}

    if t_id is None:
        continue

    print("NFC tag gevonden! Lezen...")

    for block, prefix in readDatablocks.items():
        if not ctl.mifare_classic_authenticate_block(t_id, block, PN532.MIFARE_CMD_AUTH_B, ConfigReader.GetTagKey()):
            print('Fout! Kan niet authoriseren met NFC tag op block {0}. Probeer het nog eens.'.format(block))
            continue

        data = ctl.mifare_classic_read_block(block)

        if data is None:
            print('Geen data beschrikbaar voor block {0} met prefix {1}'.format(block, prefix))
            continue

        # Controleer of dataveld de juiste prefix header heeft
        if data[0:2] != prefix:
            print('Prefix van block {0} komt niet overeen met gevraagde prefix "{1}"'.format(block, prefix))
            continue

        try:
            fmtData = int(data[2:8].decode('utf-8'), 16)
        except Exception as e:
            raise Exception('Formatteerfout op block {0} met data {1}'.format(block, str(data)))

        print('Data gevonden op block {0}: {1}'.format(block, fmtData))

        result.update({prefix: fmtData})

        print(result)

    time.sleep(1)
