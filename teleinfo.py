#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Sébastien Reuiller && Pierre-Yves Merle"
# __licence__ = "Apache License 2.0"

# Python 3, prerequis : pip install pySerial influxdb
#
# Exemple de trame:
# {
#  'OPTARIF': 'HC..',        # option tarifaire
#  'IMAX': '007',            # intensité max
#  'HCHC': '040177099',      # index heure creuse en Wh
#  'IINST': '005',           # Intensité instantanée en A
#  'PAPP': '01289',          # puissance Apparente, en VA
#  'MOTDETAT': '000000',     # Mot d'état du compteur
#  'HHPHC': 'A',             # Horaire Heures Pleines Heures Creuses
#  'ISOUSC': '45',           # Intensité souscrite en A
#  'ADCO': '000000000000',   # Adresse du compteur
#  'HCHP': '035972694',      # index heure pleine en Wh
#  'PTEC': 'HP..'            # Période tarifaire en cours
# }


import serial
import logging
import time
import requests
from datetime import datetime
from influxdb import InfluxDBClient

# clés téléinfo communes 
int_measure_keys = ['PAPP', 'ISOUSC', 'ADCO', 'PMAX']

# clés téléinfo pour compteur tri"
int_measure_keys += ['IMAX1', 'IMAX2', 'IMAX3', 'IINST1', 'IINST2', 'IINST3', 'ADIR1', 'ADIR2', 'ADIR3']

# clés téléinfo pour compteur mono"
#int_measure_keys = ['IMAX', 'IINST', 'ADIR']

# clés téléinfo pour abonnement tempo
int_measure_keys += ['BBRHCJB', 'BBRHPJB', 'BBRHCJW', 'BBRHPJW', 'BBRHCJR', 'BBRHPJR']

# clés téléinfo pour abonnement HCHP
#int_measure_keys += ['HCHC', 'HCHP']

# clés téléinfo pour abonnement base
#int_measure_keys += ['BASE']

# clés téléinfo pour abonnement EJP
#int_measure_keys += ['EJPHN', 'EJPHPM']

# création du logguer
logging.basicConfig(filename='/var/log/teleinfo/releve.log', level=logging.INFO, format='%(asctime)s %(message)s')
logging.info("Teleinfo starting..")

# connexion a la base de données InfluxDB
client = InfluxDBClient('localhost', 8086)
db = "teleinfo"
connected = False
while not connected:
    try:
        logging.info("Database %s exists?" % db)
        if not {'name': db} in client.get_list_database():
            logging.info("Database %s creation.." % db)
            client.create_database(db)
            logging.info("Database %s created!" % db)
        client.switch_database(db)
        logging.info("Connected to %s!" % db)
    except requests.exceptions.ConnectionError:
        logging.info('InfluxDB is not reachable. Waiting 5 seconds to retry.')
        time.sleep(5)
    else:
        connected = True


def add_measures(measures, time_measure):
    points = []
    for measure, value in measures.items():
        point = {
                    "measurement": measure,
                    "tags": {
                        "host": "raspberry",
                        "region": "linky"
                    },
                    "time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "fields": {
                        "value": value
                    }
                }
        points.append(point)

    client.write_points(points)


def main():
        # parité modifiée
    with serial.Serial(port='/dev/ttyS0',  baudrate=1200, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE,
                       bytesize=serial.SEVENBITS, timeout=1, rtscts=1) as ser:

        logging.info("Teleinfo is reading on /dev/ttyS0..")

        trame = dict()

        # boucle pour partir sur un début de trame
        line = ser.readline()
        while b'\x02' not in line:  # recherche du caractère de début de trame
            line = ser.readline()

        # lecture de la première ligne de la première trame
        line = ser.readline()

        while True:
            line_str = line.decode("utf-8")
           # logging.info("LINE : %s" % line)
            ar = line_str.split(" ")
            try:
                key = ar[0]
                if key in int_measure_keys :
                    value = int(ar[1])
                else:
                    value = ar[1]

                checksum = ar[2]
                trame[key] = value
                if b'\x03' in line:  # si caractère de fin dans la ligne, on insère la trame dans influx
                    del trame['ADCO']  # adresse du compteur : confidentiel!
                    time_measure = time.time()

                    # insertion dans influxdb
                    add_measures(trame, time_measure)

                    # ajout timestamp pour debugger
                    trame["timestamp"] = int(time_measure)
                    logging.debug(trame)

                    trame = dict()  # on repart sur une nouvelle trame
            except Exception as e:
                logging.error("Exception : %s" % e)
            line = ser.readline()


if __name__ == '__main__':
    if connected:
        main()


