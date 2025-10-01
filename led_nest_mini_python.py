import yaml
from gtts import gTTS
import random
import flux_led
import pychromecast

# Initialisation Chromecast
chromecasts, browser = pychromecast.get_chromecasts()
cast = next((cc for cc in chromecasts if cc.name == "Jardin de devant"), None)
if cast is None:
    print("❌ Aucun Chromecast nommé 'Jardin de devant' trouvé.")
    exit(1)

cast.wait()
mc = cast.media_controller

# Initialisation LED
led = flux_led.WifiLedBulb("192.168.1.12")  # IP de l’ampoule LED

# Menu des séances
menu_seances = {
    "zen_fluidite": {
        "nom": "Zen et Fluidité",
        "musique": "https://example.com/chill_playlist.mp3",
        "lumiere": "bleu doux",
        "directions": ["gauche"],
        "motivations": [
            "Respire profondément", "Laisse le mouvement te guider", "Tu es en harmonie"
        ],
        "nombre_max_tours": 20,
        "duree_phase": 10,
        "pas_tours": 2
    },
    "challenge_express": {
        "nom": "Challenge Express",
        "musique": "https://example.com/cardio_boost.mp3",
        "lumiere": "flash intense",
        "directions": ["droite", "gauche"],
        "motivations": [
            "Accélère", "C’est le sprint final", "Donne tout maintenant"
        ],
        "nombre_max_tours": 30,
        "duree_phase": 5,
        "pas_tours": 5
    },
    "seance_duo": {
        "nom": "Séance En Duo",
        "musique": "https://example.com/duo_dynamique.mp3",
        "lumiere": "double flash",
        "directions": ["droite", "gauche"],
        "motivations": [
            "Fais équipe avec ton partenaire", "Synchronisez vos mouvements", "Un pour tous, tous pour un"
        ],
        "nombre_max_tours": 20,
        "duree_phase": 10,
        "pas_tours": 2
    }
}

def effet_lumiere(style):
    if style == "bleu doux":
        led.setRgb(0, 0, 255)
    elif style == "flash intense":
        for _ in range(5):
            led.turnOn()
            led.setRgb(255, 255, 255,brightness=100)
            led.turnOff()
    elif style == "double flash":
        for _ in range(2):
            led.turnOn()
            led.setRgb(255, 255, 0)
            led.turnOff()

def jouer_musique(url):
    mc.play_media(url, 'audio/mp3')
    mc.block_until_active()
    mc.play()

def arreter_musique():
    mc.stop()

# Fonction principale
def generer_seance_yaml(theme):
    params = menu_seances[theme]

    print(f"\n🎵 Lecture de la musique : {params['musique']}")
    jouer_musique(params["musique"])

    print(f"💡 Effet lumière : {params['lumiere']}")
    effet_lumiere(params["lumiere"])

    for tours in range(3, params["nombre_max_tours"] + 1, params["pas_tours"]):
        for direction in params["directions"]:
            mytext=""
            print(f"\n➡️ {tours} tours vers {direction}")
            mytext+=(f"\n {tours} tours vers {direction}, ")
            if "gauche" in direction:
                print("💬 Même si c’est plus difficile à gauche, tu peux y arriver")
                mytext+=(" Même si c’est plus difficile à gauche, tu peux y arriver, ")
            print(f"💬 Motivation : {random.choice(params['motivations'])}")
            mytext+=(f" Motivation : {random.choice(params['motivations'])}, ")
            print(f" Attente de {params['duree_phase']} secondes")
            mytext+=(f" Attente de {params['duree_phase']} secondes,")
# Génération du message vocal
            tts = gTTS(mytext, lang='fr')
            tts.save("message.mp3")
            
            # Diffusion du message
            mc.play_media("http://192.168.1.18:8000/message.mp3", "audio/mp3")  # Remplace par l’URL accessible depuis ton réseau
            mc.block_until_active()
            mc.play()


            effet_lumiere("flash intense")

    msgfin=("\n🏁 Séance terminée ! Bravo 👏")
    print(msgfin)
    tts = gTTS(msgfin, lang='fr')
    tts.save("message.mp3")
    
    # Diffusion du message
    mc.play_media("http://192.168.1.18:8000/message.mp3", "audio/mp3")  # Remplace par l’URL accessible depuis ton réseau
    mc.block_until_active()
    mc.play()
    arreter_musique()
    led.turnOff()

    # YAML export
    nom_fichier = f"seance_hula_hoop_{theme}.yaml"
    with open(nom_fichier, "w", encoding="utf-8") as fichier:
        yaml.dump({"theme": theme, "params": params}, fichier, sort_keys=False)
    print(f"✅ Fichier YAML '{nom_fichier}' créé avec succès")

# Exemple d'utilisation
if __name__ == "__main__":
    print("Choisis ton theme :")
    for key, val in menu_seances.items():
        print(f"- {key} : {val['nom']}")
    
    choix = input("Tape le nom du theme (ex: zen_fluidite) : ").strip()
    if choix in menu_seances:
        generer_seance_yaml(choix)
    else:
        print("❌ Theme invalide. Relance le script et choisis parmi les options.")

