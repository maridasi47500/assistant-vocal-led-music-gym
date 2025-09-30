import yaml

# Parametres de la seance
directions = ["droite", "gauche", "droite ou à gauche"]
nombre_max_tours = 20
duree_phase = 10

# Structure YAML
seance = {
    "metadata": {
        "name": "seance hula hoop",
        "description": "Seance guidee avec tours progressifs et directions"
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

# Actions vocales
seance["automations"]["actions"].append({
    "type": "assistant.command.OkGoogle",
    "okGoogle": "repete apres moi Bienvenue dans ta seance hula hoop",
    "devices": "Jardin de devant - Jardin de devant"
})

for tours in range(3, nombre_max_tours + 1):
    for direction in directions:
        seance["automations"]["actions"].append({
            "type": "assistant.command.OkGoogle",
            "okGoogle": f"repete apres moi Tourne vers {direction} pour {tours} tours",
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

seance["automations"]["actions"].append({
    "type": "assistant.command.OkGoogle",
    "okGoogle": "repete apres moi Seance terminee bravo",
    "devices": "Jardin de devant - Jardin de devant"
})

# Ecriture dans le fichier YAML
with open("seance_hula_hoop.yaml", "w", encoding="utf-8") as fichier:
    yaml.dump(seance, fichier, sort_keys=False)

print("Fichier YAML cree avec succes")

