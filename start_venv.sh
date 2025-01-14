#!/bin/bash

# Nom de l'environnement virtuel
VENV_DIR=".venv"

# Vérifie si l'environnement virtuel existe
if [ -d "$VENV_DIR" ]; then
    echo "L'environnement virtuel existe déjà. Activation..."
else
    echo "L'environnement virtuel n'existe pas. Création..."
    
    # Création de l'environnement virtuel
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "Erreur lors de la création de l'environnement virtuel."
        exit 1
    fi

    echo "Environnement virtuel créé. Installation des dépendances..."

    # Active l'environnement virtuel pour installer les dépendances
    . "$VENV_DIR/bin/activate"

    # Installe les dépendances depuis requirements.txt si le fichier existe
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        if [ $? -ne 0 ]; then
            echo "Erreur lors de l'installation des dépendances."
            deactivate
            exit 1
        fi
        echo "Dépendances installées avec succès."
    else
        echo "Fichier requirements.txt introuvable. Aucune dépendance installée."
    fi
fi

# Activation de l'environnement virtuel
. "$VENV_DIR/bin/activate"
if [ $? -eq 0 ]; then
    echo "L'environnement virtuel est activé."
else
    echo "Erreur lors de l'activation de l'environnement virtuel."
    exit 1
fi
