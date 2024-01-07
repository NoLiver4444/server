from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
from calendar import monthrange
import json

app = Flask(__name__)


@app.route("/add_events", methods=['POST'])
def add_events():
    db = sqlite3.connect("kalendari.sqlite")
    name = request.args.get('name')
    description = request.args.get('description')
    date = request.args.get('date').split(".")
    time = request.args.get('time')
    if name == "" or time == "":
        return jsonify({"message": "Bad Request", "status": 400})

    db.cursor().execute(
        "insert into event(name, description, day, month, year, time) values('" + name + "', '" + description + "', " + date[0] +
        ", " + date[1] + ", " + date[2] + ", '" + time + "')")
    db.commit()
    response = jsonify({"message": "ok", "status": 200})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response


@app.route("/change_events", methods=['POST'])
def change_events():
    db = sqlite3.connect("kalendari.sqlite")
    id_event = request.args.get('id')
    name = request.args.get('name')
    description = request.args.get('description')
    date = request.args.get('date').split(".")
    time = request.args.get('time')

    if name == "" or time == "":
        return jsonify({"message": "Bad Request", "status": 400})
    db.cursor().execute(
        "update event set name = '" + name + "', description = '" + description + "', day = " + date[0] + ", month = " + date[1] + ", year = " + date[2] + ", time = '"
        + time + "' where id = " + id_event)
    db.commit()
    response = jsonify({"message": "ok", "status": 200})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response


@app.route("/delete_events", methods=['POST'])
def delete_events():
    db = sqlite3.connect("kalendari.sqlite")
    id_event = request.args.get('id')
    db.cursor().execute("delete from event where id = " + id_event)
    db.commit()
    response = jsonify({"message": "ok", "status": 200})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response


@app.route("/get_events_to_month")
def get_events_to_month():
    db = sqlite3.connect("kalendari.sqlite")
    date = request.args.get("date")
    d = date.split(".")
    days = monthrange(int(d[2]), int(d[1]))[1]
    if int(d[0]) > 31 or int(d[1]) > 12 or int(d[2]) > datetime.now().year + 50:
        return jsonify({"message": "Bad Request", "status": 400})
    events = db.cursor().execute(
        "SELECT * from event where day between 1 and " + str(
            days) + " and month = " + d[1] + " and year = " + d[2]).fetchall()
    response = jsonify({"message": "ok", "status": 200, "data": events})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response


if __name__ == "__main__":
    app.run(debug=True)
