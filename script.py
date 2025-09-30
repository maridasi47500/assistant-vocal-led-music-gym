import yaml

# Structure de la seance sans tirets, accents ni points de suspension
session = {
    "metadata": {
        "name": "hula hoop session",
        "description": "Guided hula hoop session with counts and directions"
    },
    "automations": {
        "starters": [
            {
                "type": "assistant.event.OkGoogle",
                "eventData": "query",
                "is": "start hula hoop session"
            }
        ],
        "actions": []
    }
}

# Parametres
directions = ["right", "left", "both sides"]
max_turns = 5
duration = 10

# Construction des actions
session["automations"]["actions"].append({
    "type": "assistant.command.OkGoogle",
    "okGoogle": "say Welcome to your hula hoop session",
    "devices": "Jardin de devant - Jardin de devant"
})

for count in range(3, max_turns + 1):
    for direction in directions:
        session["automations"]["actions"].append({
            "type": "assistant.command.OkGoogle",
            "okGoogle": f"say Turn to the {direction} for {count} turns",
            "devices": "Jardin de devant - Jardin de devant"
        })
        session["automations"]["actions"].append({
            "type": "assistant.command.OkGoogle",
            "okGoogle": f"count from 1 to {count}",
            "devices": "Jardin de devant - Jardin de devant"
        })
        session["automations"]["actions"].append({
            "type": "assistant.command.OkGoogle",
            "okGoogle": f"wait {duration} seconds",
            "devices": "Jardin de devant - Jardin de devant"
        })

session["automations"]["actions"].append({
    "type": "assistant.command.OkGoogle",
    "okGoogle": "say Session complete Good job",
    "devices": "Jardin de devant - Jardin de devant"
})

# Ecriture dans le fichier YAML
with open("hula_hoop_session.yaml", "w", encoding="utf-8") as file:
    yaml.dump(session, file, sort_keys=False)

print("YAML file created successfully")

