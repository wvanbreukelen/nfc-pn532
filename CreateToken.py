import sys, time
import ConfigReader

# NFC Python library voor PN532 microcontroller importeren
# Bron: https://github.com/adafruit/Adafruit_Python_PN532/
try:
    import Adafruit_PN532 as PN532
except Exception:
    print("PN523 library niet gevonden!")
    sys.exit()

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

while True:
    print("Plaats NFC tag op lezer...")

    # Wacht totdat er een NFC tag gevonden is
    while True:
        # Probeer een tag te lezen. Is de lezing succesvol, toon melding
        t_id = ctl.read_passive_target()

        if t_id != None:
            print("NFC tag gevonden! Verplaats deze niet...")
            break

    choice = None

    while choice is None:
        # Check voor integer
        try:
            choice = int(raw_input("Voer uniek ID in: "))
        except ValueError, NameError:
            print("Geen nummer, probeer opnieuw!")
            continue


    # Gebruik sleutel om datasector vrij te geven voor schrijven
    if not ctl.mifare_classic_authenticate_block(t_id, 1, PN532.MIFARE_CMD_AUTH_B, ConfigReader.GetTagKey()):
        print('Fout! Kan niet authoriseren met NFC tag. Probeer het nog eens.')
        continue

    # Maak datapakket
    data = bytearray(16)

    # Header toevoegen aan eerste twee bytes. Op deze manier weten we dat deze rij het ID van de tag bevat
    data[0:2] = b'ID'

    # Zet integer om naar hexidecimaal
    tag_id = format(choice, 'x')

    # Voeg nullen toe zodat de totale lengte op zes bytes komt
    while (len(tag_id) < 6):
        tag_id = '0' + tag_id

    data[2:8] = tag_id

    print(data)

    # Schrijf data naar tag op block 1
    if not ctl.mifare_classic_write_block(1, data):
        print('Fout! Kan niet naar tag schrijven. Probeer het nog eens.')
        continue

    print('Tag succesvol geschreven!')

    time.sleep(2)
