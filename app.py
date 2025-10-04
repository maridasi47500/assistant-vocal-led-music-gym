from flask import Flask, render_template, request, redirect, url_for
from dbseances import init_db, get_all_seances, get_seance_by_id, save_seance
from flask import send_file
from generate_yaml import generer_yaml_depuis_formulaire
import json
from led_nest_mini_python import generer_seance_yaml, menu_seances  # Ton script renommé en module
import json
app = Flask(__name__)
init_db()

def charger_seances_depuis_db():
    rows = get_all_seances()
    seances = {}
    for row in rows:
        theme = row[1]
        seances[theme] = {
            "id": row[0],
            "theme": row[1],
            "nom": row[2],
            "musique": row[3],
            "lumiere": row[4],
            "directions": json.loads(row[5]),
            "motivations": json.loads(row[6]),
            "nombre_max_tours": row[7],
            "duree_phase": row[8],
            "pas_tours": row[9],
            "repetitions": row[10],
            "nbmintours": row[11]
        }
    return seances

menu_seances = charger_seances_depuis_db()









@app.route("/generer_yaml", methods=["POST"])
def generer_yaml():
    seance_id = request.form.get('theme')
    seance = get_seance_by_id(seance_id)

    if not seance:
        return "❌ Séance introuvable", 404

    # Préparer les paramètres comme tuple
    params = (
        seance[1],  # theme
        seance[2],  # nom
        seance[3],  # musique
        seance[4],  # lumiere
        seance[5],  # directions (JSON string)
        seance[6],  # motivations (JSON string)
        seance[7],  # nombre_max_tours
        seance[8],  # duree_phase
        seance[9],  # pas_tours
        seance[10], # repetitions
        seance[11]  # nbmintours
    )

    # Générer le fichier YAML
    nom_fichier = generer_yaml_depuis_formulaire(params)

    # Optionnel : proposer le téléchargement
    return send_file(nom_fichier, as_attachment=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    seances = charger_seances_depuis_db()
    if request.method == 'POST':
        theme = request.form.get('theme')
        if theme in menu_seances:
            generer_seance_yaml(theme)
            message = f"Séance '{menu_seances[theme]['nom']}' lancée avec succès !"
        else:
            message = "Thème invalide."

        return render_template('index.html', seances=seances, menu=menu_seances, message=message)
    return render_template('index.html', seances=seances, menu=menu_seances)





@app.route("/edit/<int:seance_id>")
def edit(seance_id):
    seance = get_seance_by_id(seance_id)
    return render_template("form.html", seance=seance)

@app.route("/new")
def new():
    return render_template("form.html", seance=None)

@app.route("/save", methods=["POST"])
def save():
    seance_id = request.form.get("id")
    save_seance(
        request.form["theme"],
        request.form["nom"],
        request.form["musique"],
        request.form["lumiere"],
        json.dumps(request.form["directions"]),
        json.dumps(request.form["motivations"]),
        int(request.form["nombre_max_tours"]),
        int(request.form["duree_phase"]),
        int(request.form["pas_tours"]),
        int(request.form["repetitions"]),
        int(request.form["nbmintours"]),
        seance_id=seance_id
    )

    return redirect(url_for("index"))



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

