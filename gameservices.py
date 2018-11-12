## @file gameservices.py
#  @author Mark Vecsernyes
#
#  @brief This app contains the app logic
#  @{ 

## Import modules
from flask import *
import json 
import _pickle as pickle
from net import *
from genetic import *
from database import Database

##connect database
database = Database()

## Running parameters as global varible
running_params = {  "generation":   0,
                    "gravity":      0,
                    "jump":         0,
                    "population":   0,
                    "gap":          0,
                    "distance":     0,
                    "hidden":       0,
                    "selection":    0,
                    "deletion":     0,
                    "crossover":    0,
                    "mutation1":    0,
                    "mutation2":    0,
                    "threshold":    0,
                    "bird_ids":     []}

## Neural networks as global variable
neural_networks = []

## This method handles the procedures after pressing the Apply button
#  such as initializing database and setting running params
#  @return ai.html, running_params
def apply_request(request):
    global running_params
    running_params['bird_ids'] = []

    database_status = database.create_tables()

    running_params['generation'] = 0
    running_params['gravity'] = int(request.form['gravity'])
    running_params['jump'] = int(request.form['jump'])
    running_params['population'] = int(request.form['population'])
    running_params['gap'] = int(request.form['gap'])
    running_params['distance'] = int(request.form['distance'])
    running_params['hidden'] = int(request.form['hidden'])
    running_params['selection'] = int(request.form['selection'])
    running_params['deletion'] = int(request.form['deletion'])
    running_params['crossover'] = int(request.form['crossover'])
    running_params['mutation1'] = int(request.form['mutation1'])
    running_params['mutation2'] = int(request.form['mutation2'])
    running_params['threshold'] = int(request.form['threshold'])

    #print("Parameters: " + str(running_params))
    return render_template('ai.html',   generation      = running_params['generation'],
                                        gravity         = running_params['gravity'],
                                        jump            = running_params['jump'],
                                        population      = running_params['population'],
                                        gap             = running_params['gap'],
                                        distance        = running_params['distance'],
                                        hidden          = running_params['hidden'],
                                        selection       = running_params['selection'],
                                        deletion        = running_params['deletion'],
                                        crossover       = running_params['crossover'],
                                        mutation1       = running_params['mutation1'],
                                        mutation2       = running_params['mutation2'],
                                        threshold       = running_params['threshold'],
                                        database_status = database_status )


## This method handles the procedures after pressing the 'Start' button
#  such as generating neural networks randomly and insterting the into the database
#  @return json (ACK string)
def start_request(request):
    #game id
    global running_params
    global neural_networks
    neural_networks = []
    for _ in range(running_params['population']):
        cycle_id = database.insert_cycle('')
        neural_network = generate_net(running_params['hidden'])
        neural_networks.append(neural_network)
        neural_network = pickle.dumps( neural_network.state_dict() )
        bird_id = database.insert_bird( cycle_id, neural_network )
        running_params['bird_ids'].append(bird_id)
    return jsonify({"respond":"start"})


## This method handles the procedures before every generations
#  such as increasing generation number and loading neural networks, 
#  @return running_params
def start_gen_request(request):
    global running_params
    running_params['generation'] += 1
    birds_data = database.select_bird(running_params['population'])
    running_params['bird_ids'] = json.dumps( [str(i[0]) for i in birds_data] )

    j = 0
    global neural_networks
    for i in birds_data:
        neural_networks[j].load_state_dict( pickle.loads(i[1]) )
        j+=1

    return jsonify(running_params)


## This method handles the procedures after every generations
#  such as inserting fitness scores, and calling genetic algorithm
#  @return json (ACK string)
def finish_gen_request(request):
    global running_params
    for i in request.json:
        bird_id, fitness_score = i.split('#')
        database.insert_fitness(bird_id, fitness_score)

    genetic_algorithm(database, running_params['population'],
                                running_params['hidden'],
                                running_params['selection'],
                                running_params['deletion'],
                                running_params['crossover'],
                                running_params['mutation1'],
                                running_params['mutation2'])

    return jsonify({"respond":"finishgen"})


## This method handles the procedures after every bird update
#  such as creating a command list where 0 means nothing 1 means jumping
#  @return [0, 1, 1, 1 .. 0, 1] list
def jump_bird_request(request):
    #respont contains the jumping commands. 0 means not to, 1 means to jump
    global running_params
    global neural_networks
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
            input = torch.tensor([float(bY), float(pX), float(pY)])
            index = (int(bird_id) - int(first_id))
            out = neural_networks[index](input)
            respond.append ( 1 if int(out) > 0 else 0 ) 
    return jsonify( respond )


## @}
