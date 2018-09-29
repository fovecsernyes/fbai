import psycopg2
from config import config

class Database(object):
    def __init__(self):
        self.conn = None
        try:
            # read connection parameters
            self.params = config()
    
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(**self.params)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def __del__(self):
        self.conn.close()
        print('Database connection closed.')

    def create_tables(self):

        commands = (
            """
            CREATE TABLE IF NOT EXISTS cycle (
                id SERIAL PRIMARY KEY,
                parameters TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS bird (
                id  SERIAL PRIMARY KEY,
                neural_network TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS fitness (
                id SERIAL PRIMARY KEY,
                fitness INTEGER,
                bird_id INTEGER,
                cycle_id INTEGER
            )
            """
            )
        cur = self.conn.cursor()
        for command in commands:
             cur.execute(command)
        cur.close()
        self.conn.commit()
        print("Database intialized")
        return "OK"

    def insert_bird(self, bird_list):
        sql = "INSERT INTO bird(neural_network) VALUES(%s)"
        conn = None
        try:
            cur = self.conn.cursor()
            cur.executemany(sql,bird_list)
            self.conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()