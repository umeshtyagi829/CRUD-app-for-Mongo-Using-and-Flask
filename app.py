from flask import Flask, render_template
from flask.helpers import url_for
from flask.wrappers import Response
from bson.json_util import dumps
from flask.json import jsonify, request
from bson.objectid import ObjectId
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/arthtask38"
mongo = PyMongo(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/insert")
def insert():
    return render_template("insert.html")

@app.route("/upd")
def update():
    return render_template("update.html")
    

@app.route("/del")
def delete():
    return render_template("delete.html") 

@app.route('/create', methods=["POST"])
def add_student():
    db = {
      "name": request.form.get("name"), 
      "roll_no": request.form.get("roll"), 
      "marks": request.form.get("marks"), 
      "age": request.form.get("age")
    }

    mongo.db.studentdata.insert(db)
    resp = jsonify("Student data added Successfully")
    resp.status_code = 200
    return resp 

@app.route('/read', methods=["GET"])
def students():
    students = mongo.db.studentdata.find()
    resp = dumps(students)
    return resp

@app.route('/delete', methods=['POST'])
def delete_students():
      id = request.form.get("id")
      db = {
         "_id": ObjectId(id)
      }
        
      mongo.db.studentdata.delete_one(db)  
      resp = jsonify("Student data deleted successfully")
      resp.status_code = 200
      
      return resp    


@app.route('/update', methods=['POST'])
def update_students():
    id = request.form.get("id")
    db = {
         "_id": ObjectId(id)
      }
    data = {
      "name": request.form.get("name"), 
      "roll_no": request.form.get("roll"), 
      "marks": request.form.get("marks"), 
      "age": request.form.get("age")
    }
        
    mongo.db.studentdata.update_one(db, {"$set": data })  
    resp = jsonify("Student Data Updated successfully")
    resp.status_code = 200
      
    return resp    


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message' : 'Not Found' + request.url
    }          
    resp = jsonify(message)
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
