import yaml

# Paramètres personnalisables
direction_sequence = ["droite", "gauche", "les deux côtés"]
max_tours = 6
duree_par_phase = 10  # en secondes

# Génération des actions dynamiques
actions = [
    {
        "type": "assistant.command.Broadcast",
        "message": "Bienvenue à ta séance de hula hoop personnalisée !",
        "devices": "Jardin de devant - Jardin de devant"
    }
]

for tours in range(3, max_tours + 1):
    for direction in direction_sequence:
        actions.append({
            "type": "assistant.command.Broadcast",
            "message": f"Prépare-toi à tourner vers {direction}… {tours} tours !",
            "devices": "Jardin de devant - Jardin de devant"
        })
        actions.append({
            "type": "assistant.command.OkGoogle",
            "okGoogle": f"compte de 1 à {tours}",
            "devices": "Jardin de devant - Jardin de devant"
        })

        actions.append({
            "type": "assistant.command.OkGoogle",
            "okGoogle": f"attends {duree_par_phase} secondes",
            "devices": "Jardin de devant - Jardin de devant"
        })

# Clôture de la séance
actions.append({
    "type": "assistant.command.Broadcast",
    "message": "Bravo ! Tu as atteint le maximum de tours 💫",
    "devices": "Jardin de devant - Jardin de devant"
})

# Structure YAML
hula_hoop_yaml = {
    "metadata": {
        "name": "hula hoop dynamique",
        "description": "Séance avec direction, tours progressifs et durée personnalisée."
    },
    "automations": {
        "starters": [
            {
                "type": "assistant.event.OkGoogle",
                "eventData": "query",
                "is": "lance séance hula hoop dynamique"
            }
        ],
        "actions": actions
    }
}

# Écriture dans le fichier YAML
with open("seance_hula_hoop_dynamique.yaml", "w", encoding="utf-8") as file:
    yaml.dump(hula_hoop_yaml, file, allow_unicode=True, sort_keys=False)

print("✅ Fichier YAML généré avec paramètres : seance_hula_hoop_dynamique.yaml")

