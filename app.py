#this file handles the backend

from flask import *
import json 
import _pickle as pickle
from net import *
from genetic import *
from database import Database

#initializing flask
app = Flask(__name__)
app.debug = True

#these are the running parameters which are sent as a response
running_params = { "generation":0, "gravity":0, "jump":0, "population":0,
                    "gap": 0, "distance": 0, "bird_ids":[]}

#neural network is a global list type variable
neural_networks = []

@app.route('/', methods=['GET'])
def IndexRequest():
    return render_template('index.html')

#single player page
@app.route('/sp/', methods=['GET'])
def SingleRequest():
    return render_template('sp.html')

#handling get requests at '/ai' it is called when the page is (re)loaded
@app.route('/ai/', methods=['GET'])
def GetRequest():
    database_status=""
    return render_template('ai.html', database_status=database_status)

#handling post requests at '/ai/'. it is called when 'Apply' button is pressed
@app.route('/ai/', methods=['POST'])
def ApplyRequest():
    #bird ids and neural networks must be empty
    running_params['bird_ids'] = []
    neural_networks = []

    #creating tables if not exist
    database_status = database.create_tables()
    #setting and returning the running parameters from the post request
    running_params['generation'] = 0
    running_params['gravity'] = int(request.form['gravity'])
    running_params['jump'] = int(request.form['jump'])
    running_params['population'] = int(request.form['population'])
    running_params['gap'] = int(request.form['gap'])
    running_params['distance'] = int(request.form['distance'])
    print("Parameters: " + str(running_params))
    return render_template('ai.html', generation=running_params['generation'],
                                        gravity=running_params['gravity'],
                                        jump=running_params['jump'],
                                        population=running_params['population'],
                                        gap=running_params['gap'],
                                        distance=running_params['distance'],
                                        database_status=database_status)

#handling post requests at '/ai/start'. it is called when 'Start' button is pressed
@app.route('/ai/start', methods=['POST'])
def StartRequest():
    #generating and writing bird ids and neural networks to database
    for _ in range(running_params['population']):
        cycle_id = database.insert_cycle('')
        neural_network = generateNet()
        neural_networks.append(neural_network)
        neural_network = pickle.dumps( neural_network.state_dict() )
        bird_id = database.insert_bird( cycle_id, neural_network )
        running_params['bird_ids'].append(bird_id)
    return jsonify({"respond":"start"})

#handling post requests at '/ai/startgen'. it is called before every generation
@app.route('/ai/startgen', methods=['POST'])
def StartGenRequest():
    #generation number is must be increased
    running_params['generation'] += 1
    #bird ids and neural networks are read from the database here
    birds_data = database.select_bird(running_params['population'])
    running_params['bird_ids'] = json.dumps( [str(i[0]) for i in birds_data] )
    j = 0
    for i in birds_data:
        neural_networks[j].load_state_dict( pickle.loads(i[1]) )
        j+=1
    return jsonify(running_params)

#handling post requests at '/ai/finishgen'. it is called after every generation
@app.route('/ai/finishgen', methods=['POST'])
def FinishGenRequest():
    #after every generation the fitness score is written to the database
    for i in request.json:
        bird_id, fitness_score = i.split('#')
        print(bird_id, fitness_score)
        database.insert_fitness(bird_id, fitness_score)

    #after every generation the genetic algorithm runs
    geneticAlgorithm(database, running_params['population'])

    return jsonify({"respond":"finishgen"})

#handling post requests at '/ai/jumpbird'. it is called after every bird update
@app.route('/ai/jumpbird', methods=['POST'])
def JumpBirdRequest():
    #respont contains the jumping commands. 0 means not to, 1 means to jump
    respond = []
    for i in request.json:
        #birds datas from post request, like id, bY, pX, pY
        ids = json.loads(running_params['bird_ids'])
        #fist bird id
        first_id = ids[0]
        bird_id, params = i.split('#')
        #running the neural network
        if params != 'dead':
            bY,pX,pY = params.split(',')
            input = autograd.Variable(torch.tensor([float(bY), float(pX), float(pY)]))
            index = (int(bird_id) - int(first_id))
            out = neural_networks[index](input)
            respond.append ( 1 if float(out) > 0 else 0 ) 
    return jsonify( respond )

#main function
if __name__ == "__main__":
    database = Database()
    app.run()
