from flask import Flask, render_template, request
from led_nest_mini_python import generer_seance_yaml, menu_seances  # Ton script renommé en module

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        theme = request.form.get('theme')
        if theme in menu_seances:
            generer_seance_yaml(theme)
            message = f"Séance '{menu_seances[theme]['nom']}' lancée avec succès !"
        else:
            message = "Thème invalide."
        return render_template('index.html', menu=menu_seances, message=message)
    return render_template('index.html', menu=menu_seances)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

