from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
from calendar import monthrange

app = Flask(__name__)


@app.route("/add_events", methods=['POST'])
def add_events():
    try:
        db = sqlite3.connect("kalendari.sqlite")
        name = request.args.get('name')
        description = request.args.get('description')
        date = request.args.get('date').split(".")
        time = request.args.get('time')
        if int(date[0]) > 31 or int(date[1]) > 12 or int(date[2]) > datetime.now().year + 50:
            raise Exception('bad date format')
        db.cursor().execute(
            f'''
            INSERT INTO event(name, description, day, month, year, time) 
            VALUES({"'" + name + "'" if name else "Null"}, '{description}', {date[0]}, {date[1]}, {date[2]}, '{time}')
            '''
        )
        db.commit()
        response = jsonify({"message": "ok", "status": 200})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        return response
    except Exception as e:
        response = jsonify({"message": "Internal server error",
                            "status": 500,
                            "error_message": str(e)}
                           )
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        return response


@app.route("/change_events", methods=['POST'])
def change_events():
    try:
        db = sqlite3.connect("kalendari.sqlite")
        id_event = request.args.get('id')
        q = db.cursor().execute(f"""SELECT * FROM event WHERE id = {id_event}""").fetchall()
        if not q:
            response = jsonify({"message": "Event not found", "status": 400})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            return response
        name = request.args.get('name')
        description = request.args.get('description')
        date = request.args.get('date').split(".")
        time = request.args.get('time')
        name = name if name else q[0][1]
        description = description if description else q[0][2]
        date = date if date else [q[0][4], q[0][5], q[0][6]]
        time = time if time else q[0][3]
        if int(date[0]) > 31 or int(date[1]) > 12 or int(date[2]) > datetime.now().year + 50:
            raise Exception('bad date format')
        db.cursor().execute(
            f"""UPDATE event 
                  SET 
                    name = '{name}', 
                    description = '{description}', 
                    day = {date[0]}, 
                    month = {date[1]}, 
                    year = {date[2]}, 
                    time = '{time}' 
                  WHERE id = {id_event}
            """)
        db.commit()
        response = jsonify({"message": "ok", "status": 200})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        return response
    except Exception as e:
        response = jsonify({"message": "Internal server error",
                            "status": 500,
                            "error_message": str(e)}
                           )
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        return response


@app.route("/delete_events", methods=['POST'])
def delete_events():
    try:
        db = sqlite3.connect("kalendari.sqlite")
        id_event = request.args.get('id')
        q = db.cursor().execute(f"""SELECT * FROM event WHERE id = {id_event}""").fetchall()
        if not q:
            response = jsonify({"message": "Event not found", "status": 400})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            return response
        db.cursor().execute(f"""DELETE FROM event WHERE id = {id_event}""")
        db.commit()
        response = jsonify({"message": "ok", "status": 200})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        return response
    except Exception as e:
        response = jsonify({"message": "Internal server error",
                            "status": 500,
                            "error_message": str(e)}
                           )
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        return response


@app.route("/get_events_to_month")
def get_events_to_month():
    try:
        db = sqlite3.connect("kalendari.sqlite")
        date = request.args.get("date")
        date = date.split(".")
        days = monthrange(int(date[2]), int(date[1]))[1]
        if int(date[0]) > 31 or int(date[1]) > 12 or int(date[2]) > datetime.now().year + 50:
            raise Exception('bad date format')
        events = db.cursor().execute(
            f"""SELECT * FROM event 
                WHERE day BETWEEN 1 AND {days} AND month = {date[1]} AND year = {date[2]}"""
        ).fetchall()
        response = jsonify({"message": "ok", "status": 200, "data": events})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        return response
    except Exception as e:
        response = jsonify({"message": "Internal server error",
                            "status": 500,
                            "error_message": str(e)}
                           )
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        return response


if __name__ == "__main__":
    app.run(debug=True)
