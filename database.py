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
                parameters TEXT NOT NULL,
                parent_id INTEGER REFERENCES cycle UNIQUE,
                sum_fitness INTEGER NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS bird (
                id  SERIAL PRIMARY KEY,
                neural_network TEXT NOT NULL,
                cycle_id SERIAL,
                FOREIGN KEY (cycle_id) REFERENCES cycle(parent_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS fitness (
                id SERIAL PRIMARY KEY,
                fitness INTEGER,
                bird_id INTEGER,
                cycle_id INTEGER,
                FOREIGN KEY (bird_id) REFERENCES bird(id),
                FOREIGN KEY (cycle_id) REFERENCES cycle(id)
            )
            """
            )
        cur = self.conn.cursor()
        for command in commands:
             cur.execute(command)
        cur.close()
        self.conn.commit()
        print("Database intialized")