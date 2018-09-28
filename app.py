from flask import *
import json
from agent import *
from database import Database
#initializing flask
app = Flask(__name__)
app.debug = True

#these are the running parameters which are sent as a response
running_params = { "generation":0, "gravity":0, "population":0,
                    "gap": 0, "distance": 0 }

#handling get requests at '/' it is called when the page is (re)loaded
@app.route('/', methods=['GET'])
def GetRequest():
    database_status=""
    return render_template('index.html', database_status=database_status)

#handling post requests at '/'. it is called when 'Apply' button is pressed
@app.route('/', methods=['POST'])
def ApplyRequest():
    database_status = database.create_tables()
    running_params['generation'] = 0
    running_params['gravity'] = int(request.form['gravity'])
    running_params['population'] = int(request.form['population'])
    running_params['gap'] = int(request.form['gap'])
    running_params['distance'] = int(request.form['distance'])
    print("Parameters: " + str(running_params))
    return render_template('index.html', generation=running_params['generation'],
                                        gravity=running_params['gravity'],
                                        population=running_params['population'],
                                        gap=running_params['gap'],
                                        distance=running_params['distance'],
                                        database_status=database_status)

#handling post requests at '/'. it is called when 'Start' button is pressed
@app.route('/start', methods=['POST'])
def StartRequest():
    print("Generating neural networks")
    return jsonify(running_params)

#handling post requests at '/startgen'. it is called before every generation
@app.route('/startgen', methods=['POST'])
def StartGenRequest():
    if running_params['generation']:
        geneticAlgorithm(database)
    running_params['generation'] += 1
    print(str(running_params['generation'])+ ". generation started")
    return jsonify(running_params)

#handling post requests at '/finishgen'. it is called after every generation
@app.route('/finishgen', methods=['POST'])
def FinishGenRequest():
    print(str(running_params['generation'])+ ". generation finished")
    return jsonify({"respond":"finishgen"})

#main function
if __name__ == "__main__":
    database = Database()
    app.run()
