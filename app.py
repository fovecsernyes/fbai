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
    return render_template('index.html')


## GET request at /sp/ - single player mode
#  @return sp.html
@app.route('/sp/', methods=['GET'])
def SingleRequest():
    return render_template('sp.html')


## GET request at /ai/ - ai player mode
#  @return ai.html
@app.route('/ai/', methods=['GET'])
def AiRequest():
    return render_template('ai.html')


## POST request at /ai/
@app.route('/ai/', methods=['POST'])
def ApplyRequest():
    return apply_request(request)


## Post request at /ai/start
@app.route('/ai/start', methods=['POST'])
def StartRequest():
    return start_request(request)


## Post request at /ai/startgen
@app.route('/ai/startgen', methods=['POST'])
def StartGenRequest():
    return start_gen_request(request)


## Post request at /ai/finishgen
@app.route('/ai/finishgen', methods=['POST'])
def FinishGenRequest():
    return finish_gen_request(request)


## Post request at /ai/jumpbird
@app.route('/ai/jumpbird', methods=['POST'])
def JumpBirdRequest():
    return jump_bird_request(request)


## Main function
#  initialising database and running the flask service
if __name__ == "__main__":
    app.run()

## @}
