from gtts import gTTS
import pychromecast
import time

# Génère le message vocal
tts = gTTS("Bienvenue dans ta séance Zen et Fluidité", lang='fr')
tts.save("message.mp3")

# Lance un serveur HTTP local (dans un terminal séparé)
# python3 -m http.server 8000

# Initialise le Chromecast
chromecasts, browser = pychromecast.get_chromecasts()
cast = next((cc for cc in chromecasts if cc.name == "Jardin de devant"), None)
if cast is None:
    print("❌ Aucun Chromecast nommé 'Salon' trouvé.")
    exit(1)
cast.wait()
mc = cast.media_controller

# Diffuse le fichier audio
mc.play_media("http://192.168.1.18:8000/message.mp3", "audio/mp3")  # Remplace par l’IP de ton PC
mc.block_until_active()
mc.play()

