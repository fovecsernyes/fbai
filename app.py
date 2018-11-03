## @file app.py
#  @author Mark Vecsernyes
#
#  @brief Ez a fájl indítja el a backend szolgáltatásokat
#  @{ 

## A szükséges könyvtárak importálása
from flask import *
import json 
import _pickle as pickle
from net import *
from genetic import *
from database import Database

## Flask osztály példányosítása, ez kezeli a HTTP kommunikációt
app = Flask(__name__)
app.debug = True

## utási paramétek, amik a frontendről fognak jönni a /templates/ai.html fájlból
running_params = {  "generation":   0,
                    "gravity":      0,
                    "jump":         0,
                    "population":   0,
                    "gap":          0,
                    "distance":     0,
                    "bird_ids":    []}

## Neurális hálókat tartalmazó lista az "AI Player mode"-hoz
neural_networks = []

## GET kérés kezelése a / címen
#  @return index.html oldal
@app.route('/', methods=['GET'])
def IndexRequest():
    return render_template('index.html')

## GET kérés kezelése a /sp/ címen
#  @return sp.html
@app.route('/sp/', methods=['GET'])
def SingleRequest():
    return render_template('sp.html')

## GET kérés kezelése a /ai/ címen
#  @return ai.html
@app.route('/ai/', methods=['GET'])
def GetRequest():
    database_status=""
    return render_template('ai.html', database_status=database_status)

## POST kérés kezelése a /ai/ címen
#  Apply gomb megnyomása után: adatbázis inicializálása, illetve a running_params beállítása
#  @return ai.html, running_params 
@app.route('/ai/', methods=['POST'])
def ApplyRequest():
    running_params['bird_ids'] = []
    neural_networks = []

    database_status = database.create_tables()

    running_params['generation'] = 0
    running_params['gravity'] = int(request.form['gravity'])
    running_params['jump'] = int(request.form['jump'])
    running_params['population'] = int(request.form['population'])
    running_params['gap'] = int(request.form['gap'])
    running_params['distance'] = int(request.form['distance'])
    print("Parameters: " + str(running_params))
    return render_template('ai.html',   generation      = running_params['generation'],
                                        gravity         = running_params['gravity'],
                                        jump            = running_params['jump'],
                                        population      = running_params['population'],
                                        gap             = running_params['gap'],
                                        distance        = running_params['distance'],
                                        database_status = database_status)

## Post kérés kezelése a /ai/start címen
#  Start gomb megnyomása után: hálók generálása, és beszúrása a táblákba
#  @return ACK json
@app.route('/ai/start', methods=['POST'])
def StartRequest():
    for _ in range(running_params['population']):
        cycle_id = database.insert_cycle('')
        neural_network = generateNet()
        neural_networks.append(neural_network)
        neural_network = pickle.dumps( neural_network.state_dict() )
        bird_id = database.insert_bird( cycle_id, neural_network )
        running_params['bird_ids'].append(bird_id)
    return jsonify({"respond":"start"})

## Post kérés kezelése a /ai/startgen címen
#  Minden generáció előtti kérés: generáció növelése, hálók betöltése
#  @return running_params
@app.route('/ai/startgen', methods=['POST'])
def StartGenRequest():
    running_params['generation'] += 1
    birds_data = database.select_bird(running_params['population'])
    running_params['bird_ids'] = json.dumps( [str(i[0]) for i in birds_data] )
    j = 0
    for i in birds_data:
        neural_networks[j].load_state_dict( pickle.loads(i[1]) )
        j+=1
    return jsonify(running_params)

## Post kérés kezelése a /ai/finishgen címen
#  Minden generáció utáni kérés: fintess beszúrása az adatbázisba, evoluciós algoritmus futtatása
#  @return ACK json
@app.route('/ai/finishgen', methods=['POST'])
def FinishGenRequest():
    for i in request.json:
        bird_id, fitness_score = i.split('#')
        #print(bird_id, fitness_score)
        database.insert_fitness(bird_id, fitness_score)

    geneticAlgorithm(database, running_params['population'])

    return jsonify({"respond":"finishgen"})

## Post kérés kezelése a /ai/finishgen címen
#  Minden időpillantaban a madarak ugrásának kiértékelése a neurális háló alapján. 0 - semmi, 1 - ugrás
#  @return [0,1,1,1 .. 0, 1] lista
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

## Main függvény
if __name__ == "__main__":
    database = Database()
    app.run()

## @}
