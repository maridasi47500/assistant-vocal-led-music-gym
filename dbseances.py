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
        nbmintours INTEGER,
    )
    """)
    conn.commit()
    conn.close()

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
    conn.close()
    return row

def save_seance(data, seance_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    if seance_id:
        cursor.execute("""
        UPDATE seances SET theme=?, nom=?, musique=?, lumiere=?, directions=?, motivations=?,
        nombre_max_tours=?, duree_phase=?, pas_tours=?, repetitions=?, nbmintours WHERE id=?
        """, (*data, seance_id))
    else:
        cursor.execute("""
        INSERT INTO seances (theme, nom, musique, lumiere, directions, motivations,
        nombre_max_tours, duree_phase, pas_tours, repetitions, nbmintours)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, data)
    conn.commit()
    conn.close()

