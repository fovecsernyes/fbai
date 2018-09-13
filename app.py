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
                DROP TABLE IF EXISTS birds;
            """,
            """
            CREATE TABLE birds (
                network VARCHAR(255) NOT NULL
            )
            """)

        cur = self.conn.cursor()
        for command in commands:
             cur.execute(command)
        cur.close()
        self.conn.commit()

        #print(population + " neural networks are generated")


@app.route('/', methods=['GET','POST'])
def dropdown():
    gravity = [x/10 for x in range(10, 21)]
    population = [5*x for x in range(1, 11)]
    gap = [5*x for x in range(14, 25)]

    if request.method == 'POST':
        db.initialize(request.form['population'])

    return render_template('index.html', gravity=gravity, population=population, gap=gap)

if __name__ == "__main__":
    db = Database()
    app.run()