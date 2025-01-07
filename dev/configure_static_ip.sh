#!/bin/bash

# Liste des interfaces disponibles
echo "Interfaces réseau disponibles :"
ip link show | awk -F': ' '/^[0-9]+: /{print $2}' | grep -v "lo"

# Demande à l'utilisateur de choisir une interface
read -p "Entrez le nom de l'interface à configurer : " INTERFACE

# Vérification si l'interface existe
if ! ip link show "$INTERFACE" > /dev/null 2>&1; then
    echo "Erreur : L'interface $INTERFACE n'existe pas."
    exit 1
fi

# Récupération des paramètres actuels
IP=$(ip -4 addr show $INTERFACE | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
NETMASK=$(ip -4 addr show $INTERFACE | grep -oP '(?<=inet\s)\d+(\.\d+){3}/\d+' | cut -d/ -f2)
GATEWAY=$(ip route show default | grep $INTERFACE | awk '{print $3}')
DNS=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}')

# Vérification si tous les paramètres sont récupérés
if [[ -z "$IP" || -z "$NETMASK" || -z "$GATEWAY" || -z "$DNS" ]]; then
    echo "Erreur : Impossible de récupérer les paramètres réseau de $INTERFACE"
    exit 1
fi

# Affichage des paramètres actuels
echo "Paramètres actuels de l'interface $INTERFACE :"
echo "  Adresse IP : $IP"
echo "  Masque : $NETMASK"
echo "  Passerelle : $GATEWAY"
echo "  DNS : $DNS"

# Demande à l'utilisateur une nouvelle adresse IP
read -p "Entrez la nouvelle adresse IP statique (actuelle: $IP) : " NEW_IP
NEW_IP=${NEW_IP:-$IP} # Si l'utilisateur n'entre rien, garder l'adresse actuelle

# Génération du fichier Netplan
NETPLAN_FILE="/etc/netplan/01-netcfg.yaml"

cat <<EOL | sudo tee $NETPLAN_FILE
network:
  version: 2
  renderer: networkd
  ethernets:
    $INTERFACE:
      addresses:
        - $NEW_IP/$NETMASK
      gateway4: $GATEWAY
      nameservers:
        addresses:
          - $DNS
EOL

# Application de la configuration
echo "Configuration appliquée :"
cat $NETPLAN_FILE
sudo netplan apply

echo "Configuration réseau statique appliquée pour $INTERFACE avec l'adresse IP $NEW_IP"
