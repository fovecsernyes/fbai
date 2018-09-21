from database import Database
from flask import *
import json
app = Flask(__name__)
app.debug = True

running_params = { "generation":0,
                "gravity":0,
                "population":0,
                "gap": 0,
                "rounds": 0}


@app.route('/', methods=['GET'])
def GetRequest():
    database_status=""
    return render_template('index.html', database_status=database_status)

@app.route('/', methods=['POST'])
def ApplyRequest():
    running_params['generation'] = 0
    running_params['gravity'] = request.form['gravity']
    running_params['population'] = request.form['population']
    running_params['gap'] = request.form['gap']

    database_status = database.create_tables()
    return render_template('index.html', generation=running_params['generation'],
                                        gravity=running_params['gravity'],
                                        population=running_params['population'],
                                        gap=running_params['gap'],
                                        database_status=database_status)


@app.route('/start', methods=['POST'])
def StartRequest():
    print("Game started")
    return jsonify(running_params)

@app.route('/startgen', methods=['POST'])
def StartGenRequest():
    running_params['generation'] += 1
    print(str(running_params['generation'])+ ". generation started")
    return jsonify({"generation":running_params['generation']})

@app.route('/finishgen', methods=['POST'])
def FinishGenRequest():
    print(str(running_params['generation'])+ ". generation finished")
    return jsonify({"respond":"finishgen"})

if __name__ == "__main__":
    database = Database()
    app.run()