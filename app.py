from database import Database
from flask import *
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
    print(request.form)
    status = "ack"
    return render_template('index.html', status=status) #not working
    


if __name__ == "__main__":
    database = Database()
    app.run()