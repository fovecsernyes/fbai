from flask import Flask, render_template, request
app = Flask(__name__)
app.debug = True


@app.route('/', methods=['GET','POST'])
def dropdown():
    gravity = [x/10 for x in range(10, 21)]
    population = [5*x for x in range(1, 11)]
    gap = [5*x for x in range(14, 25)]

    if request.method == 'GET':
         print("Gravity: " + request.args.get('gravity', "None") )
         print("Population: " + request.args.get('population', "None") )
         print("Gap: " + request.args.get('gap', "None") )

    return render_template('index.html', gravity=gravity, population=population, gap=gap)

if __name__ == "__main__":
    app.run()