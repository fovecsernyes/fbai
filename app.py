from database import Database
from flask import Flask, render_template, request
app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET','POST'])
def dropdown():
    gravity = [x/10 for x in range(10, 21)]
    population = [5*x for x in range(1, 11)]
    gap = [5*x for x in range(14, 25)]

    database_status = ""

    if request.method == 'POST':
        db.create_tables()
        database_status = "OK"
    return render_template('index.html', gravity=gravity, population=population, gap=gap, database_status=database_status)

if __name__ == "__main__":
    db = Database()
    app.run()