import sqlite3
import json

DB_PATH = "seances.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS seances (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        theme TEXT UNIQUE NOT NULL,
        nom TEXT NOT NULL,
        musique TEXT,
        lumiere TEXT,
        directions TEXT,
        motivations TEXT,
        nombre_max_tours INTEGER,
        duree_phase INTEGER,
        pas_tours INTEGER,
        repetitions INTEGER,
        nbmintours INTEGER
    )
    """)
    conn.commit()
    conn.close()
init_db()

def get_all_seances():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM seances")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_seance_by_id(seance_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM seances WHERE id = ?", (seance_id,))
    row = cursor.fetchone()
    hey =  (
            row[0],
            row[1],

             row[2],
             row[3],
             row[4],
             json.loads(row[5]),
             json.loads(row[6]),
             row[7],
             row[8],
            row[9],
             row[10],
             row[11]
       ) 

    conn.close()
    return hey

def save_seance(theme, nom, musique, lumiere, directions, motivations,
                nombre_max_tours, duree_phase, pas_tours, repetitions, nbmintours, seance_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    if seance_id:
        cursor.execute("""
            UPDATE seances SET theme=?, nom=?, musique=?, lumiere=?, directions=?, motivations=?,
            nombre_max_tours=?, duree_phase=?, pas_tours=?, repetitions=?, nbmintours=? WHERE id=?
        """, (
            theme, nom, musique, lumiere,
            (directions),
            (motivations),
            nombre_max_tours, duree_phase, pas_tours, repetitions, nbmintours, seance_id
        ))
    else:
        cursor.execute("""
            INSERT INTO seances (theme, nom, musique, lumiere, directions, motivations,
            nombre_max_tours, duree_phase, pas_tours, repetitions, nbmintours)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            theme, nom, musique, lumiere,
            json.dumps(directions),
            json.dumps(motivations),
            nombre_max_tours, duree_phase, pas_tours, repetitions, nbmintours
        ))
    conn.commit()
    conn.close()

def ajouter_seance(theme, nom, musique, lumiere, directions, motivations, nombre_max_tours, duree_phase, pas_tours, repetitions , nbmintours=2):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO seances (theme, nom, musique, lumiere, directions, motivations, nombre_max_tours, duree_phase, pas_tours, repetitions,nbmintours)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        theme, nom, musique, lumiere,
        json.dumps(directions),
        json.dumps(motivations),
        nombre_max_tours, duree_phase, pas_tours, repetitions, nbmintours
    ))
    conn.commit()

# Exemple d'ajout
#ajouter_seance(
#    theme="zen_fluidite",
#    nom="Zen et Fluidité",
#    musique="https://stunnel1.cyber-streaming.com:9162/stream?",
#    lumiere="bleu doux",
#    directions=["gauche"],
#    motivations=["Respire profondément", "Laisse le mouvement te guider", "Tu es en harmonie"],
#    nombre_max_tours=20,
#    duree_phase=10,
#    pas_tours=2,
#    repetitions=2
#)

