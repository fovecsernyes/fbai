from database import Database
from flask import *
import gameservice
app = Flask(__name__)
app.debug = True


@app.route('/', methods=['GET','POST'])
def HandleServicesRequest():
    return gameservice.handle_command(request.form)

if __name__ == "__main__":
    app.run()