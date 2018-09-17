from database import Database
from flask import *
import gameservice
app = Flask(__name__)
app.debug = True


@app.route('/', methods=['GET','POST'])
def HandleServicesRequest():
    return gameservice.handle_command(request.data)

if __name__ == "__main__":
    db = Database()
    app.run()