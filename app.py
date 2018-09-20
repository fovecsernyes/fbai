from database import Database
from flask import *
import json
app = Flask(__name__)
app.debug = True

running_params = { "gravity":0,
                "population":30,
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
    running_params['rounds'] = request.form['rounds']

    database_status = database.create_tables()
    return render_template('index.html', gravity=running_params['gravity'],
                                        population=running_params['population'],
                                        gap=running_params['gap'],
                                        rounds=running_params['rounds'],
                                        database_status=database_status)


@app.route('/start', methods=['POST'])
def StartRequest():
    data = request.get_json()
    return jsonify(running_params)

@app.route('/round', methods=['POST'])
def RoundRequest():
    print("Cycle instert(default, POST-on jott, onmaga, 0)")
    print("if 0 == select count(*) from bird where cycleID == cycle.parentID")
    for i in range(0, int(running_params['population'])):
        print("\t" + str(i) + ". bird instert(currentID, neuralishalo)")
    return jsonify({"round":"respond"})

@app.route('/finishround', methods=['POST'])
def FinishRoundRequest():
    print("receive post(array[birdID ,fitness])")
    for i in range(0, int(running_params['population'])):
        print("\t" + str(i) + ". fitness insert(default,fitness, birdID, cycleID)")
    print("cycle.update(sum fitness)")

    return jsonify({"roundfinish":"respond"})

if __name__ == "__main__":
    database = Database()
    app.run()