from flask import Flask, render_template, request
from database import Database

database = Database()


def handle_command(flask_request: str) -> str:
    gravity = [x/10 for x in range(10, 21)]
    population = [5*x for x in range(1, 11)]
    gap = [5*x for x in range(14, 25)]
    rounds = [x for x in range(1, 11)]
    print(flask_request)


    database_status = ""
    #database_status = database.create_tables()
        

    return render_template('index.html', gravity=gravity, population=population,
               gap=gap, rounds=rounds, database_status=database_status)
