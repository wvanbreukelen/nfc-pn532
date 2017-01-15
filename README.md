# nfc-pn532

Pythoncode om met NXP PN532 microcontroller te communiceren

## Installatie

- Installeer [Adafruit_Python_PN532](https://github.com/adafruit/Adafruit_Python_PN532):
```bash
sudo apt-get update
sudo apt-get install build-essential python-dev git
git clone https://github.com/adafruit/Adafruit_Python_PN532.git
cd Adafruit_Python_PN532
sudo python setup.py install
```

- Download deze repository (GIT of als ZIP-bestand)

## Gebruik

### Lezen
```bash
sudo python ReadTag.py
```

### Schrijven
```bash
sudo python WriteTag.py
```

### Schoonmaken
```bash
sudo python CleanTag.py
```
