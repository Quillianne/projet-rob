from gtts import gTTS
import os

def lire_texte(texte, voix="fr", accent="com"):
    tts = gTTS(text=texte, lang=voix, tld=accent)
    tts.save("sortie.mp3")
    os.system("mpg321 sortie.mp3")

lire_texte("Salut", voix="fr", accent="ca")  # "ca" pour un accent canadien
