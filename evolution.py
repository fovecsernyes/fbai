from flask import Flask, render_template, request
import psycopg2
from config import config
app = Flask(__name__)
app.debug = True
 
def connect():
    """ Connect to the PostgreSQL database server """
    print("/////*************************//////")
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
 
        # create a cursor
        cur = conn.cursor()
        
 # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
 
        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
     # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


@app.route('/', methods=['GET','POST'])
def dropdown():
    gravity = [x/10 for x in range(10, 21)]
    population = [5*x for x in range(1, 11)]
    gap = [5*x for x in range(14, 25)]

    if request.method == 'POST':
        print("Gravity: " + request.form['gravity'] )
        print("Population: " + request.form['population'] )
        print("Gap: " + request.form['gap'] )

        conn = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="postgres")

    return render_template('index.html', gravity=gravity, population=population, gap=gap)

if __name__ == "__main__":
    connect()
    app.run()