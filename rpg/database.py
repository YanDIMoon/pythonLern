import sqlite3

def save_game(player, enemy):
    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saves (
        id INTEGER PRIMARY KEY,
        player_x INTEGER,
        player_y INTEGER,
        enemy_x INTEGER,
        enemy_y INTEGER,
        player_hp INTEGER,
        enemy_hp INTEGER
    )""")

    cursor.execute("DELETE FROM saves")
    cursor.execute("INSERT INTO saves (player_x, player_y, enemy_x, enemy_y, player_hp, enemy_hp) VALUES (?, ?, ?, ?, ?, ?)",
                   (player.x, player.y, enemy.x, enemy.y, player.hp, enemy.hp))
    conn.commit()
    conn.close()

def load_game():
    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM saves")
    data = cursor.fetchone()
    conn.close()
    return data




