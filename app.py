from config import config
from flask import Flask, render_template, request
import psycopg2
import random
import string
app = Flask(__name__)
app.debug = True

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

    def initialize(self, population):

        commands = (
            """
            CREATE TABLE IF NOT EXISTS Cycle (
                id SERIAL PRIMARY KEY,
                parameters TEXT NOT NULL,
                parent_id SERIAL REFERENCES Cycle UNIQUE,
                sum_fitness INTEGER NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS Bird (
                id  SERIAL PRIMARY KEY,
                neural_network TEXT NOT NULL,
                cycle_id SERIAL,
                FOREIGN KEY (cycle_id) REFERENCES Cycle(parent_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS Fitness (
                id SERIAL PRIMARY KEY,
                fitness INTEGER,
                bird_id SERIAL,
                cycle_id SERIAL,
                FOREIGN KEY (bird_id) REFERENCES Bird(id),
                FOREIGN KEY (cycle_id) REFERENCES Cycle(id)
            )
            """
            )
        cur = self.conn.cursor()
        for command in commands:
             cur.execute(command)
        cur.close()
        self.conn.commit()
        print("Database intialized")

@app.route('/', methods=['GET','POST'])
def dropdown():
    gravity = [x/10 for x in range(10, 21)]
    population = [5*x for x in range(1, 11)]
    gap = [5*x for x in range(14, 25)]

    database_status = ""

    if request.method == 'POST':
        db.initialize(request.form['population'])
        database_status = "OK"
    #ebbe menjen a valasz
    return render_template('index.html', gravity=gravity, population=population, gap=gap, database_status=database_status)

if __name__ == "__main__":
    db = Database()
    app.run()