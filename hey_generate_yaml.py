import yaml
import json
import random
import json
import random

def nettoyer_json_embedded(data, max_depth=5):
    """Essaie de décoder un JSON encodé plusieurs fois."""
    for _ in range(max_depth):
        if isinstance(data, list):
            return data
        try:
            data = json.loads(data)
        except (json.JSONDecodeError, TypeError):
            break
    return data if isinstance(data, list) else []



def generer_yaml_depuis_formulaire(params):
    (
        theme, nom, musique, lumiere, directions_json, motivations_json,
        nombre_max_tours, duree_phase, pas_tours, repetitions, nbmintours
    ) = params

    #directions = json.loads(json.loads(str(directions_json)))
    directions = nettoyer_json_embedded(directions_json)
    motivations = nettoyer_json_embedded(motivations_json)
    print(directions,motivations)

    seance = {
        "metadata": {
            "name": nom,
            "description": f"Seance '{theme}' avec musique, lumières et encouragements"
        },
        "automations": {
            "starters": [
                {
                    "type": "assistant.event.OkGoogle",
                    "eventData": "query",
                    "is": f"demarrer seance {theme}"
                }
            ],
            "actions": []
        }
    }

    seance["automations"]["actions"].extend([
        {
            "type": "assistant.command.Broadcast",
            "message": f"Bienvenue dans ta seance {nom}",
            "devices": "Jardin de devant - Jardin de devant"
        },
        {
            "type": "assistant.command.OkGoogle",
            "okGoogle": f"joue {musique}",
            "devices": "Jardin de devant - Jardin de devant"
        },
        {
            "type": "device.command.ActivateScene",
            "activate": "true",
            "devices": f"en mode {lumiere}"
        }
    ])

    for _ in range(repetitions):
        for tours in range(nbmintours, nombre_max_tours + 1, pas_tours):
            for direction in directions:
                message_direction = f"Tourne vers {direction} pour {tours} tours"
                if "gauche" in direction:
                    message_direction += " tu peux y arriver"
                message_motivation = random.choice(motivations)

                seance["automations"]["actions"].extend([
                    {
                        "type": "time.delay",
                        "for": f"5sec"
                    },
                    {
                        "type": "assistant.command.Broadcast",
                        "message": f"{message_direction}",
                        "devices": "Jardin de devant - Jardin de devant"
                    },
                    {
                        "type": "time.delay",
                        "for": f"5sec"
                    },
                    {
                        "type": "assistant.command.Broadcast",
                        "message": f"{message_motivation}",
                        "devices": "Jardin de devant - Jardin de devant"
                    },
                    {
                        "type": "time.delay",
                        "for": f"5sec"
                    },
                    {
                        "type": "assistant.command.OkGoogle",
                        "okGoogle": f"compter de 1 a {tours}",
                        "devices": "Jardin de devant - Jardin de devant"
                    },

                    {
                        "type": "device.command.ActivateScene",
                        "activate": "true",
                        "devices": "en mode flash"
                    },
                    {
                        "type": "time.delay",
                        "for": f"{duree_phase}sec"
                    }
                ])

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

    nom_fichier = f"seance_{theme}.yaml"
    with open(nom_fichier, "w", encoding="utf-8") as fichier:
        yaml.dump(seance, fichier, sort_keys=False)

    print(f"✅ Fichier YAML '{nom_fichier}' généré avec succès.")

    return nom_fichier  # ← retourne le nom du fichier


