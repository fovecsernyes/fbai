from database import Database
from flask import *
import json
app = Flask(__name__)
app.debug = True

running_params = { "gravity":0,
                "population":0,
                "gap": 0,
                "rounds": 0}


@app.route('/', methods=['GET'])
def GetRequest():
    database_status=""
    return render_template('index.html', database_status=database_status)

@app.route('/', methods=['POST'])
def ApplyRequest():
    running_params['gravity'] = request.form['gravity']
    running_params['population'] = request.form['population']
    running_params['gap'] = request.form['gap']

    database_status = database.create_tables()
    return render_template('index.html', gravity=running_params['gravity'],
                                        population=running_params['population'],
                                        gap=running_params['gap'],
                                        database_status=database_status)


@app.route('/start', methods=['POST'])
def StartRequest():
    print("Game started")
    return jsonify(running_params)

@app.route('/startgen', methods=['POST'])
def StartGenRequest():
    print("Generation Started")
    return jsonify({"startgen":"respond"})

@app.route('/finishgen', methods=['POST'])
def FinishGenRequest():
    print("finished generation")
    return jsonify({"finishgen":"respond"})

if __name__ == "__main__":
    database = Database()
    app.run()