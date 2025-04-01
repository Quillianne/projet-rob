from gtts import gTTS
from playsound import playsound
import os
from pydub import AudioSegment



class Sound():
    def __init__(self):
        current_directory = os.path.dirname(os.path.realpath(__file__))
        mp3_filename = "output.mp3"
        self.name_file = os.path.join(current_directory, mp3_filename)


    def text_to_speech(self, text, speed=1.5):  # speed=1.5 pour 1.5x plus rapide
        # Générer l'audio avec gTTS
        tts = gTTS(text, lang='fr', slow=False)
        tts.save(self.name_file)

        # Charger et accélérer l'audio
        audio = AudioSegment.from_file(self.name_file, format="mp3")
        faster_audio = audio.speedup(playback_speed=speed)  # Augmenter la vitesse
        faster_audio.export(self.name_file, format="mp3")  # Réenregistrer le fichier

        # Lire le fichier
        playsound(self.name_file)


if __name__ == "__main__":
    texte = "Une autre solution est d'accélérer l'audio après son enregistrement à l’aide de la bibliothèque pydub. Tu peux utiliser audio.speedup() pour augmenter la vitesse :"
    son = Sound()
    son.text_to_speech(texte)