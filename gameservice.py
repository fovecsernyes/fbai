from flask import Flask, render_template, request
from database import Database

database = Database()


def handle_command(flask_request: str) -> str:

    print(flask_request)


    database_status = ""
    #database_status = database.create_tables()
        

    return render_template('index.html', database_status=database_status)
