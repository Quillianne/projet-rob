import subprocess

def photo():
    """
    Utilise l'exécutable save_rgb pour prendre une photo avec la Kinect et l'enregistrer dans le dossier courant
    sous le nom "kinect_photo_rgb.png".
    """
    # Chemin vers l'exécutable
    executable_path = "./save_rgb"  # Chemin vers l'exécutable

    # Appeler l'exécutable en utilisant subprocess
    try:
        subprocess.run([executable_path], check=True)  # Exécute l'exécutable sans arguments
        print("Photo prise et enregistrée avec succès.")
        
        # # Copier l'image au presse-papier avec xclip
        # image_path = "kinect_photo_rgb.png"  # Le nom de l'image à ajouter au presse-papier
        # subprocess.run(["xclip", "-selection", "clipboard", "-t", "image/png", "-i", image_path])
        # print(f"L'image {image_path} a été copiée dans le presse-papier.")
        
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de l'exécutable : {e}")
    except FileNotFoundError as e:
        print(f"Erreur : L'exécutable n'a pas été trouvé : {e}")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")

if __name__ == "__main__":
    photo()
