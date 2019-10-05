# Téléinfo
## Hardware
### Optocoupleur
Afin de pouvoir convertir le signal téléinfo modulé a 50Hz en un signal numérique standard vosu aurez besoin un petit montage assez simple à base d'optocoupleur.
Il vous faudra pour celà : 

- 1 optocoupleur SFH620A
- 1 résistance 1.2 kΩ
- 1 résistance 3.3 kΩ

![](http://www.magdiblog.fr/wp-content/uploads/2014/05/teleinfo_schema.jpg)

### Raspberry Pi

## Software
### Rapsbian

Dans le fichier ```/boot/cmdline.txt``` :
```
- supprimer la ligne :
console=serial0,115200
- ajouter la ligne : 
enable_uart=1
```

### InfluxDB
#### RPi <= 2B (ARMv6 et ARMv7)
```
wget https://dl.influxdata.com/influxdb/releases/influxdb_1.7.8_armhf.deb
sudo dpkg -i influxdb_1.7.8_armhf.deb
```
#### RPi > 2B (ARM64)
```
wget https://dl.influxdata.com/influxdb/releases/influxdb_1.7.8_arm64.deb
sudo dpkg -i influxdb_1.7.8_arm64.deb
```

```
sudo systemctl enable influxdb
sudo systemctl start influxdb
```

### Grafana 
#### RPi < 2B (ARMv6)
```
wget https://dl.grafana.com/oss/release/grafana-rpi_6.4.1_armhf.deb
sudo dpkg -i grafana-rpi_6.4.1_armhf.deb
```
#### RPi == 2B (ARMv7)
```
wget https://dl.grafana.com/oss/release/grafana_6.4.1_armhf.deb
sudo dpkg -i grafana_6.4.1_armhf.deb 
```
#### RPi > 2B (ARM64)
```
wget https://dl.grafana.com/oss/release/grafana_6.4.1_arm64.deb
sudo dpkg -i grafana_6.4.1_arm64.deb
```

```
sudo systemctl enable grafana-server
sudo systemctl start grafana-server
```

### Script Téléinfo

Editer ```/etc/rc.local``` pour lancer le script dans un tmux au démarrage
ajouter la ligne
``` su -l pi -c "/usr/bin/tmux new-session -s teleinfo -d  'python /home/pi/teleinfo/teleinfo.py' \; set -t teleinfo remain-on-exit on"```

```
sudo apt install tmux

mkdir /var/log/teleinfo
sudo chown pi /var/log/teleinfo

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python get-pip.py
sudo pip install serialpy
sudo pip install influxdb
```

Sources:

http://www.magdiblog.fr/gpio/teleinfo-edf-suivi-conso-de-votre-compteur-electrique/

https://github.com/SebastienReuiller/teleinfo-linky-with-raspberry
