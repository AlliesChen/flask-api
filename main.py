import os
from flask import Flask, Response, request
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)
load_dotenv()
MONGODB_URI = os.getenv('MONGODB_URI')
client = MongoClient(MONGODB_URI)
db = client["thirty_days_of_python"]

def initiate_data():
    if "students" in db.list_collection_names():
        print("db is ready")
        return None

    students = [
        {
            'name': 'Asabeneh',
            'country': 'Finland',
            'city': 'Helsinki',
            'skills': ['HTML', 'CSS', 'JavaScript', 'Python']
        },
        {
            'name': 'David',
            'country': 'UK',
            'city': 'London',
            'skills': ['Python', 'MongoDB']
        },
        {
            'name': 'John',
            'country': 'Sweden',
            'city': 'Stockholm',
            'skills': ['Java', 'C#']
        }
    ]
    try:
        db.students.insert_many(students)
        print("Adding init data to db")

    except Exception as err:
        print(f"Something wrong while initiating data - Error: {err}")

    return None


@app.route("/api/v1.0/students", methods=["GET", "POST"])
def students():
    if request.method == "POST":
        student = request.json
        print(student)

        try:
            result = db.students.insert_one(student)
            new_student = db.students.find_one({"_id": result.inserted_id})
            json_data = dumps(new_student)

            return Response(json_data, mimetype="application/json")

        except Exception as err:
            return f"Something wrong while POSTing students - Error: {err}"

    else:
        try:
            students = db.students.find()
            json_data = dumps(students)

            return Response(json_data, mimetype="application/json")

        except Exception as err:

            return f"Something wrong while GETting students - Error: {err}"

@app.route("/api/v1.0/students/<id>", methods=["GET"])
def single_student(id):
    try:
        student = db.students.find({"_id": ObjectId(id)})
        json_data = dumps(student)

        return Response(json_data, mimetype="application/json")
    except Exception as err:

        return f"Something wrong while GETting student - Error: {err}"

@app.route("/api/v1.0/students/<id>", methods=["PUT"])
def update_student(id):
    query = {"_id": ObjectId(id)}
    new_value = {"$set": request.json}

    try:
        db.students.update_one(query, new_value)
        updated_value = db.students.find_one(query)
        json_data = dumps(updated_value)

        return Response(json_data, mimetype="application/json")

    except Exception as err:

        return f"Something wrong while updating student's info - Error: {err}"

@app.route("/api/v1.0/students/<id>", methods=["DELETE"])
def delete_student(id):
    query = {"_id": ObjectId(id)}

    try:
        db.students.delete_one(query)
        updated_data = db.students.find()
        json_data = dumps(updated_data)

        return Response(json_data, mimetype="application/json")

    except Exception as err:

        return f"Something wrong while DELETing student's info - Error: {err}"

if __name__ == "__main__":
    initiate_data()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
