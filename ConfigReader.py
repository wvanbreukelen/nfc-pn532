import ConfigParser

# Haal configuratie uit config.ini op
def GetGPIOConfig():
    config = ConfigParser.ConfigParser()

    config.read('config.ini')

    gpio = {}

    for option in config.options('GPIO'):
        gpio[option.upper()] = int(config.get('GPIO', option))

    return gpio

# Elke NFC tag bestaat uit verschillende sectoren (in ons geval 16) waarin een bepaalde hoeveelheid data in opgeslagen kan worden.
# Om de data te kunnen lezen/schrijven is er een unieke sleutel nodig. Standaard staat deze sleutel op zes FF bytes
def GetTagKey():
    return [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
