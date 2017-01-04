import ConfigReader

# NFC Python library voor PN532 microcontroller importeren
# Bron: https://github.com/adafruit/Adafruit_Python_PN532/
try:
    import Adafruit_PN532 as PN532
except Exception:
    print("PN523 library niet gevonden!")
    sys.exit()

# NFC autoriseerfout
class NFCAuthorizeException(Exception):
    pass

# Geen prefix match
class NFCPrefixMismatch(Exception):
    pass

# NFC schrijffout
class NFCWriteError(Exception):
    pass

# Formateerfout
class FormatError(Exception):
    pass

class NFC:
    def __init__(self, ctl, tag_key):
        self.ctl = ctl
        self.key = tag_key

    def begin(self):
        # Maak connectie met de PN532 controller
        self.ctl.begin()

        # Configuratie instellen op PN532
        self.ctl.SAM_configuration()

    def scan(self):
        self.tag_id = self.ctl.read_passive_target()

        return self.tag_id != None

    def read(self, block, prefix):
        if not self.authorizeBlock(block):
            raise NFCAuthorizeException('Cannot authorize with NFC tag.')

        data = self.ctl.mifare_classic_read_block(block)

        if data is None:
            raise NFCPrefixMismatch('No data available for block {0} with prefix {1}'.format(block, prefix))

        # Controleer of dataveld de juiste prefix header heeft
        if data[0:2] != prefix:
            raise NFCPrefixMismatch('Prefix from block {0} does not equals with requested prefix "{1}"'.format(block, prefix))

        try:
            fmtData = int(data[2:8].decode('utf-8'), 16)
        except Exception as e:
            raise FormatError('Format error on block {0} with data {1}'.format(block, str(data)))

        return {prefix: fmtData}

    def write(self, block, prefix, input):
        # Gebruik sleutel om datasector vrij te geven voor schrijven
        if not self.authorizeBlock(block):
            raise NFCAuthorizeException('Cannot authorize with NFC tag.')

        # Maak datapakket
        data = bytearray(16)

        prefixLen = len(prefix)

        # Controleer of header juiste lengte heeft
        if prefixLen > 3:
            raise NFCPrefixMismatch('Prefix {0} is too long.'.format(prefix))

        # Header toevoegen aan eerste twee bytes. Op deze manier weten we dat deze rij het ID van de tag bevat
        data[0:prefixLen] = str.encode(prefix)

        # Zet integer om naar hexidecimaal
        tag_id = format(input, 'x')

        # Voeg nullen toe zodat de totale lengte op zes bytes komt
        while (len(tag_id) < 6):
            tag_id = '0' + tag_id

        data[2:8] = tag_id

        # Schrijf data naar tag op block 1
        if not self.ctl.mifare_classic_write_block(block, data):
            raise NFCWriteError('Cannot write to NFC tag.')

    def clean(self, block, prefix):
        # Gebruik sleutel om datasector vrij te geven voor schrijven
        if not self.authorizeBlock(block):
            raise NFCAuthorizeException('Cannot authorize with NFC tag.')

        # Haal actuele data van het blok op
        data = self.ctl.mifare_classic_read_block(block)

        # Bepaal de (waarschijnlijke) prefix van het datablock
        dataPrefix = data[0:len(prefix)]

        # Vergelijk de prefix van het actuele datablock met de gevraagde prefix.
        # Komt deze niet overeen, sla het block over. We hebben hier niet te maken met het te verwijderen dataveld.
        # Ook wordt verkomen dat er een lege sleutel kan worden aangemaakt. Het gevolg zou een gedeeltelijk corrupt geheugen
        # van de NFC tag.
        if dataPrefix == prefix:
            # Schrijf block vol met lege bytearray
            self.ctl.mifare_classic_write_block(block, bytearray(16));

    # Gebruik sleutel om datasector vrij te geven voor schrijven
    def authorizeBlock(self, block):
        return self.ctl.mifare_classic_authenticate_block(self.tag_id, block, PN532.MIFARE_CMD_AUTH_B, self.key)
