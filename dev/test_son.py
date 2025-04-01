# import pyttsx3
# import time

# engine = pyttsx3.init()
# engine.setProperty('voice', engine.getProperty('voices')[1].id)
# engine.say("Bonjour, comment ça va ?")
# engine.runAndWait()
# engine.stop()

# # voices = engine.getProperty('voices')
# # for i, voice in enumerate(voices):
# #     print(f"{i}: {voice.name} ({voice.languages}) - {voice.id}")

# # engine.setProperty('voice', voices[34].id)  # Remplace par l'ID trouvé
# # # engine.setProperty('rate', 150)  # Ajuste la vitesse si besoin
# # engine.say("Bonjour, je parle français avec pyttsx3.")
# # engine.runAndWait()


from gtts import gTTS
from playsound import playsound

# Texte à convertir en parole
text = "Bonjour, comment ça va ?"

# Génération de la parole en MP3
tts = gTTS(text, lang='fr')

# Sauvegarder le fichier MP3 sur le disque
mp3_file = "output.mp3"
tts.save(mp3_file)

# Jouer le fichier MP3 après l'avoir sauvegardé
playsound(mp3_file)
