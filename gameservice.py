from flask import Flask, render_template, request
from database import Database

database = Database()

def NoKey():
    database_status=""
    return render_template('index.html', database_status=database_status)

def ApplyCommand():
    database_status = database.create_tables()
    return render_template('index.html', database_status=database_status)

def StartRoundCommand():
    status="ACK"
    return render_template("index.html", status=status)
    


def handle_command(flask_request: str) -> str:


    command = str(flask_request.get("command"))
    print(flask_request)

    commands = {"None": NoKey,
                "Apply" : ApplyCommand,
                "StartRound" : StartRoundCommand,
    }

    return commands[command]()    
