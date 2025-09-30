import yaml

# Parametres de la seance
directions = ["la droite", "la gauche", "la droite ou la gauche"]
nombre_max_tours = 20
duree_phase = 10

# Structure YAML
seance = {
    "metadata": {
        "name": "seance hula hoop",
        "description": "Seance guidee avec tours progressifs et directions personnalisees"
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
    "okGoogle": "repte apres moi Bienvenue dans ta seance hula hoop",
    "devices": "Jardin de devant - Jardin de devant"
})

# Instructions selon direction
for tours in range(5, nombre_max_tours + 1):
    for direction in directions:
        message = f"Tourne vers {direction} pour {tours} tours"
        if "gauche" in direction:
            message += " c est le bon cote"

        seance["automations"]["actions"].append({
            "type": "assistant.command.OkGoogle",
            "okGoogle": f"repte apres moi {message}",
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
    "okGoogle": "repte apres moi Seance terminee bravo",
    "devices": "Jardin de devant - Jardin de devant"
})

# Ecriture dans le fichier YAML
with open("seance_hula_hoop.yaml", "w", encoding="utf-8") as fichier:
    yaml.dump(seance, fichier, sort_keys=False)

print("Fichier YAML cree avec succes")

