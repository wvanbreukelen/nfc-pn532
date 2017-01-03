import ConfigParser

def GetGPIOConfig():
    config = ConfigParser.ConfigParser()

    config.read('config.ini')

    gpio = {}

    for option in config.options('GPIO'):
        gpio[option.upper()] = int(config.get('GPIO', option))

    return gpio

def GetTagKey():
    return [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
