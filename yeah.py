import yaml
import random

# Parametres de la seance
directions = ["droite", "gauche", "droite ou a gauche"]
nombre_max_tours = 20
duree_phase = 10

# Liste de messages d'encouragement
messages_motivation = [
    "Tu peux le faire",
    "Continue comme ca",
    "Ne lache rien",
    "Garde le rythme",
    "Tu assures",
    "Bravo tu progresses",
    "Tu geres",
    "C est ton moment",
    "Tu es au top",
    "Encore un tour",
    "Plus vite si tu peux",
    "Respire et continue",
    "Tu tiens le rythme",
    "Tu maitrises le mouvement",
    "Belle rotation",
    "Tu es dans la danse"
]

# Structure YAML
seance = {
    "metadata": {
        "name": "seance hula hoop",
        "description": "Seance guidee avec tours progressifs, directions et encouragements"
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

# Message d'accueil
seance["automations"]["actions"].append({
    "type": "assistant.command.OkGoogle",
    "okGoogle": "repete apres moi Bienvenue dans ta seance hula hoop",
    "devices": "Jardin de devant - Jardin de devant"
})

# Instructions et motivation
for tours in range(5, nombre_max_tours + 1):
    for direction in directions:
        message_direction = f"Tourne vers {direction} pour {tours} tours"
        if "gauche" in direction:
            message_direction += " meme si c est plus difficile a gauche, tu peux y arriver"

        message_motivation = random.choice(messages_motivation)

        seance["automations"]["actions"].append({
            "type": "assistant.command.OkGoogle",
            "okGoogle": f"repete apres moi {message_direction}",
            "devices": "Jardin de devant - Jardin de devant"
        })
        seance["automations"]["actions"].append({
            "type": "assistant.command.OkGoogle",
            "okGoogle": f"repete apres moi {message_motivation}",
            "devices": "Jardin de devant - Jardin de devant"
        })
        seance["automations"]["actions"].append({
            "type": "assistant.command.OkGoogle",
            "okGoogle": f"compter de 1 a {tours}",
            "devices": "Jardin de devant - Jardin de devant"
        })
        seance["automations"]["actions"].append({
            "type": "assistant.command.OkGoogle",
            "okGoogle": f"attendre {duree_phase} secondes",
            "devices": "Jardin de devant - Jardin de devant"
        })

# Message de fin
seance["automations"]["actions"].append({
    "type": "assistant.command.OkGoogle",
    "okGoogle": "repete apres moi Seance terminee bravo",
    "devices": "Jardin de devant - Jardin de devant"
})

# Ecriture dans le fichier YAML
with open("seance_hula_hoop.yaml", "w", encoding="utf-8") as fichier:
    yaml.dump(seance, fichier, sort_keys=False)

print("Fichier YAML cree avec succes")

