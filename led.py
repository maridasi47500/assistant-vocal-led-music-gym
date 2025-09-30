import yaml
import random

# Parametres de la seance
directions = ["droite", "gauche", "droite ou a gauche"]
nombre_max_tours = 20
duree_phase = 10

# Messages d'encouragement sans caracteres speciaux
messages_motivation = [
    "Tu peux le faire", "Continue comme ca", "Ne lache rien", "Garde le rythme",
    "Tu assures", "Bravo tu progresses", "Tu geres", "C est ton moment",
    "Tu es au top", "Encore un tour", "Plus vite si tu peux", "Respire et continue",
    "Tu tiens le rythme", "Tu maitrises le mouvement", "Belle rotation", "Tu es dans la danse"
]

# Structure YAML
seance = {
    "metadata": {
        "name": "seance hula hoop",
        "description": "Seance guidee avec tours progressifs, la lampe, musique rythmee et encouragements"
    },
    "automations": {
        "starters": [
            {
                "type": "assistant.event.OkGoogle",
                "eventData": "query",
                "is": "demarrer seance hula hoop"
            }
        ],
        "actions": []
    }
}

# Message d accueil + lancement musique et lumieres
seance["automations"]["actions"].extend([
    {
        "type": "assistant.command.OkGoogle",
        "okGoogle": "repete apres moi Bienvenue dans ta seance hula hoop",
        "devices": "Jardin de devant - Jardin de devant"
    },
    {
        "type": "assistant.command.OkGoogle",
        "okGoogle": "joue playlist hulahoop Rythme sur spotify",
        "devices": "Jardin de devant - Jardin de devant"
    },
    {
        "type": "device.command.ActivateScene",
        "activate": "true",
        "devices": "en mode arc en ciel"
    }
])

# Instructions et motivation
for tours in range(3, nombre_max_tours + 1):
    for direction in directions:
        message_direction = f"Tourne vers {direction} pour {tours} tours"
        if "gauche" in direction:
            message_direction += " meme si c est plus difficile a gauche, tu peux y arriver"

        message_motivation = random.choice(messages_motivation)

        seance["automations"]["actions"].extend([
            {
                "type": "assistant.command.OkGoogle",
                "okGoogle": f"repete apres moi {message_direction}",
                "devices": "Jardin de devant - Jardin de devant"
            },
            {
                "type": "assistant.command.OkGoogle",
                "okGoogle": f"repete apres moi {message_motivation}",
                "devices": "Jardin de devant - Jardin de devant"
            },
            {
                "type": "assistant.command.OkGoogle",
                "okGoogle": f"compter de 1 a {tours}",
                "devices": "Jardin de devant - Jardin de devant"
            },
            {
                "type": "assistant.command.OkGoogle",
                "okGoogle": f"attendre {duree_phase} secondes",
                "devices": "Jardin de devant - Jardin de devant"
            },
            {       
                "type": "device.command.ActivateScene",
                "activate": "true",
                "devices": "en mode flash"
            }           

        ])

# Message de fin + arret musique et lumieres
seance["automations"]["actions"].extend([
    {
        "type": "assistant.command.OkGoogle",
        "okGoogle": "repete apres moi Seance terminee bravo",
        "devices": "Jardin de devant - Jardin de devant"
    },
    {
        "type": "assistant.command.OkGoogle",
        "okGoogle": "arrete la musique",
        "devices": "Jardin de devant - Jardin de devant"
    },
    {
        "type": "assistant.command.OkGoogle",
        "okGoogle": "eteins la lampe",
        "devices": "Jardin de devant - Jardin de devant"
    }
])

# Ecriture dans le fichier YAML
with open("seance_hula_hoop_led_musique.yaml", "w", encoding="utf-8") as fichier:
    yaml.dump(seance, fichier, sort_keys=False)

print("Fichier YAML sans caracteres speciaux cree avec succes")

