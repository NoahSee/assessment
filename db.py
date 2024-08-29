import sqlite3


def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    with open("schema.sql", "r") as f:
        sql_script = f.read()
    cursor.executescript(sql_script)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
