from database import Database
from flask import Flask, render_template, request
app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET','POST'])
def dropdown():
    gravity = [x/10 for x in range(10, 21)]
    population = [5*x for x in range(1, 11)]
    gap = [5*x for x in range(14, 25)]
    rounds = [x for x in range(1, 11)]

    database_status = ""

    if request.method == 'POST':
        database_status = db.create_tables()
        print("Gravity:" + request.form['gravity'] + "    " +
            "Population:" + request.form['population'] + "    " +
            "Gap:" + request.form['gap'] + "    " +
            "Rounds:" + request.form['rounds']
        ) 

    return render_template('index.html', gravity=gravity, population=population,
                gap=gap, rounds=rounds, database_status=database_status)

if __name__ == "__main__":
    db = Database()
    app.run()