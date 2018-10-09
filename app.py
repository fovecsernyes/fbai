from flask import *
import json
from net import *
from genetic import *
from database import Database
#initializing flask
app = Flask(__name__)
app.debug = True

#these are the running parameters which are sent as a response
running_params = { "generation":0, "gravity":0, "population":0,
                    "gap": 0, "distance": 0, "bird_ids":[]}

neural_networks = []

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
    neural_networks = []
    bird_ids = []
    for _ in range(running_params['population']):
        cycle_id = database.insert_cycle('')
        neural_network = generateNet()
        neural_networks.append(neural_network)
        bird_id = database.insert_bird(cycle_id, str(neural_network))
        bird_ids.append(bird_id)

    return jsonify({"respond":"start"})

#handling post requests at '/startgen'. it is called before every generation
@app.route('/startgen', methods=['POST'])
def StartGenRequest():
    if running_params['generation']:
        geneticAlgorithm(database)
    running_params['generation'] += 1

    running_params['bird_ids'] = json.dumps(database.select_bird(running_params['population']))
    print(running_params['bird_ids'])
    return jsonify(running_params)

#handling post requests at '/finishgen'. it is called after every generation
@app.route('/finishgen', methods=['POST'])
def FinishGenRequest():
    #fitness_scores = []
    for i in request.json:
        bird_id, fitness_score = i.split('#')
        print(bird_id, fitness_score)
        #fitness_scores.append(_)
        database.insert_fitness(bird_id, fitness_score)
    return jsonify({"respond":"finishgen"})

#handling post requests at '/jumpbird'. it is called after bird update
@app.route('/jumpbird', methods=['POST'])
def JumpBirdRequest():
    #out = neural_network(autograd.Variable(torch.tensor([1.2, 3.1, 4.1])))
    return jsonify()

#main function
if __name__ == "__main__":
    database = Database()
    app.run()
