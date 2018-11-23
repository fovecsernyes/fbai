## @file app.py
#  @author Mark Vecsernyes
#
#  @brief This app starts the backend
#  @{ 

## Import modules
from flask import *
from gameservices import *

#disable request messages
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


## Initializing flask app
app = Flask(__name__)
## To show consol messages
app.debug = True


## GET request at / - home page
#  @return index.html
@app.route('/', methods=['GET'])
def IndexRequest():
	#print("TEST: index page")
	return render_template('index.html')


## GET request at /sp/ - single player mode
#  @return sp.html
@app.route('/sp/', methods=['GET'])
def SingleRequest():
	#print("TEST: singleplayer page")
	return render_template('sp.html')


## GET request at /ai/ - ai player mode
#  @return ai.html
@app.route('/ai/', methods=['GET'])
def AiRequest():
	#print("TEST: aiplayer page")
	return render_template('ai.html')


## POST request at /ai/
@app.route('/ai/', methods=['POST'])
def ApplyRequest():
	#print("TEST: Apply button pressed")
	return apply_request(request)


## Post request at /ai/start
@app.route('/ai/start', methods=['POST'])
def StartRequest():
	#print("TEST: Start button pressed")
	return start_request(request)


## Post request at /ai/startgen
@app.route('/ai/startgen', methods=['POST'])
def StartGenRequest():
	#print(TEST: StartGenRequest() called)
    return start_gen_request(request)


## Post request at /ai/finishgen
@app.route('/ai/finishgen', methods=['POST'])
def FinishGenRequest():
	#print(TEST: StartGenRequest() called)
    return finish_gen_request(request)


## Post request at /ai/jumpbird
@app.route('/ai/jumpbird', methods=['POST'])
def JumpBirdRequest():
	#print(TEST: StartGenRequest() called)
    return jump_bird_request(request)


## Main function
#  initialising database and running the flask service
if __name__ == "__main__":
    app.run()

## @}
