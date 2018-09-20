from database import Database
from flask import *
import random, json
app = Flask(__name__)
app.debug = True


@app.route('/', methods=['GET'])
def GetRequest():
    database_status=""
    return render_template('index.html', database_status=database_status)

@app.route('/', methods=['POST'])
def ApplyRequest():
    print(request.form)
    database_status = database.create_tables()
    return render_template('index.html', database_status=database_status)

@app.route('/start', methods=['POST'])
def StartRequest():
    data = request.get_json()
    print(data)
    return jsonify({"data_modositott" : "datavalue_modositott"})
    


if __name__ == "__main__":
    database = Database()
    app.run()