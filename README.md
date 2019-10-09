# Téléinfo
## Informations techniques
### Singal téléinfo
1200 bps
7 bits/car
parité paire
1 bit de stop
## Hardware
### Optocoupleur
Afin de pouvoir convertir le signal téléinfo modulé à 50kHz en un signal numérique standard vous aurez besoin d'un petit montage assez simple à base d'optocoupleur.
Il vous faudra pour celà : 

- 1 optocoupleur SFH620A
- 1 résistance 1.2 kΩ
- 1 résistance 3.3 kΩ

![](http://www.magdiblog.fr/wp-content/uploads/2014/05/teleinfo_schema.jpg)

Effectuer les brachements sur le RPi:
GND -> GND
3.3V -> 3.3V
RX -> GPIO15 (RXD)

![](https://www.elektronik-kompendium.de/sites/raspberry-pi/fotos/raspberry-pi-15b.jpg)

### Raspberry Pi
Testé sur RPi 3B et 3A+ avec Raspbian Buster

## Software
### Rapsbian

Dans le fichier ```/boot/config.txt``` :
```
- ajouter la ligne : 
enable_uart=1
```

### InfluxDB
```
wget https://dl.influxdata.com/influxdb/releases/influxdb_1.7.8_armhf.deb
sudo dpkg -i influxdb_1.7.8_armhf.deb
sudo systemctl enable influxdb
sudo systemctl start influxdb
```

### Grafana 
```
wget https://dl.grafana.com/oss/release/grafana_6.4.1_armhf.deb
sudo dpkg -i grafana_6.4.1_armhf.deb 
sudo systemctl enable grafana-server
sudo systemctl start grafana-server
```

### Script Téléinfo

Modifier le script ```téléinfo.py``` en fonction de votre compteur et abonnement (lignes 31 à 50)

Editer ```/etc/rc.local``` pour lancer le script dans un tmux au démarrage
ajouter la ligne (modifier le path du script teleinfo.py)
``` su -l pi -c "/usr/bin/tmux new-session -s teleinfo -d  'python /home/pi/teleinfo/teleinfo.py' \; set -t teleinfo remain-on-exit on"```

```
sudo apt install tmux

sudo mkdir /var/log/teleinfo
sudo chown pi /var/log/teleinfo

sudo pip install influxdb
```
Finalement redémarrez votre RPi et tout devrai démarrer automatiquement, RDV ensuite sur {rpi-address}:3000

# Grafana
## Source
Séléctionnez InfluxDB comme source, avec pour adresse "http://localhost:8086" et pour table "teleinfo"
Ensuite vous pouvez importer le dashboard correspondant à votre installation éléctrique


Sources:

http://www.magdiblog.fr/gpio/teleinfo-edf-suivi-conso-de-votre-compteur-electrique/

https://github.com/SebastienReuiller/teleinfo-linky-with-raspberry

https://www.domotique-info.fr/technologies-domotique/teleinformation/