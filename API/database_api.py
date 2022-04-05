
from urllib import request
from flask import Flask, request, json, jsonify,render_template
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson.json_util import dumps
from bson import json_util
from flask_cors import CORS
import json

app=Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Hermes"
def parse_json(data):
    return json.loads(json_util.dumps(data))

mongo  = PyMongo(app)
CORS(app)
# signup and login functions below 
@app.route("/User/signup",methods=["POST"])
def signup():
    status = 200
    resp  ={}
    try:
        data = request.get_json("data")
        print(data)
        username = data["data"]["username"]
        email = data["data"]["email"]
        password = data["data"]["password"]
        database_check = mongo.db.users.find({"username":f"{username}","email":f"{email}"})
        if parse_json(database_check) == []:
            if username != "" and email !="" and password != "":

                payload = {
                    "username ":username ,
                    "email":email,
                    "password":password
                }
                mongo.db.user.insert_one(payload)   
                resp = {"message":"user made"}
        else:
            status = 300
            resp ={"message":"User credentials are in use"}
            return jsonify(resp),status 

    except Exception as e  :
        print("ERROR on /User/signup",e)

@app.route("/User/Login",methods=["POST"])
def login():
    status =200
    resp = {}
    try:
        data = request.get_json("data")
        username = data["data"]["username"]
        password = data["data"]["password"]
        if username != "" and password != "":
            database_check  = mongo.db.users.find({"username":f"{username}"})
            if parse_json(database_check) != []:
                print("User found")
                database_password  = database_check["password"]
                if password == database_password:
                    resp ={"message":"success"}
                else:
                    status =300
                    resp  ={"massage":"User password is incorrect"}
            else :
                status = 300
                resp = {"message":"User does not exsit"}
        return jsonify(resp),status
    except Exception as e:
        print("ERROR on /User/Login",e)
#"sending message arae below"
@app.route("/Send/message",methods=["POST"])
def send_message():
    status  = 200
    resp  = {}
    try:
        data = request.get_json("data")
        print(data)
        name = data["data"]["name"]
        message_arrray = []
        if name != '':
            check = mongo.db.messaege.find({"name":f"{name}"}) 
            if parse_json(check) != []:
                message_arrray  = check["message"]
        message  = data["data"]["message"]
        target = data["data"]["target"]
        message_arrray.append(message)
        if name != "" and message  != "":
            payload = {
                "name":name,
                "message":message_arrray,
                "target":target
            }
            mongo.db.message.insert_one(payload)
            resp = {"message":"message sent"}
            return jsonify(resp),status
    except Exception as e:
        print("ERROR on /Sent/message",e)
# making chat tye area below
@app.route("/Make/chat",methods =["POST"])
def make_chat():
    status  = 200
    resp = {}
    try:
        data = request.get_json("data")
        participant1 = data["data"]["participant1"]
        participant2 = data ["data"]["participant2"]
        if participant1 != "" and participant2 != "":
            payload ={
                "participant1":participant1,
                "participant2":participant2,
                "message":[]
            }
            database_check = mongo.db.chat.find({"participant1":f"{participant1}","participant2":f"{participant2}"})
            if parse_json(database_check) == []:
                mongo.db.chats.insert_one(payload)
                resp = {"messge":"chat created"}
            else :
                existant_chat  = parse_json(database_check)
                resp={"chat":existant_chat}
        return jsonify(resp),status
    except Exception as e :
        print("ERROR on /Sent/message",e)
@app.route("/Make/group_chat",methods =["POST"])
def make_chat():
    status  = 200
    resp = {}
    try:
        data = request.get_json("data")
        admin = data["data"]["admin"]
        group_name = data ["data"]["group_name"]
        if admin != "" and group_name != "":
            database_check  = mongo.db.group_chats.find({"group_name":f"{group_name}"})
            if parse_json(database_check) == []:
                payload ={
                    "admin":admin,
                    "group_name":group_name,
                    "group_memeber":[],
                    "messages":[]
                }
                mongo.db.group_chats.insert_one(payload)
                resp = {"messge":"chat created"}
            else :
                status =300
                resp = {"message":"group name has been taken"}
        return jsonify(resp),status
    except Exception as e :
        print("ERROR on /Make/group_chat",e)
#retrieve all chats function below 
@app.route("/Retrieve/chats",methods=["POST"])
def retrieve_chats():
    status = 200
    resp = {}
    try:
        data = request.get_json("data")
        username = data["data"]["username"]
        if username != "":
            chat_array = []
            chats = mongo.db.chats.find({"participant1":f"{username}"})
            if parse_json(chats) != []:
                chat_array.append(chats)
            group_chats  = mongo.db.group_chat.find({"admin":f"{username}"})
            if parse_json(group_chats) != []:
                chat_array.append(group_chats)
            membership = mongo.db.group_chat.find()
            if parse_json(membership) !=[]:
        
                group = parse_json(membership)[ "group_memeber"]
                if username in group :
                    group  = group["group_name"]
                    membership = mongo.db.group_chat.find({"group_name":f"{group}"})
                    chat_array.append(membership)
            if chat_array == []:
                status  = 300
                resp = {"message":"you have no chats"}
            else:
                resp  ={"chats":chat_array}
        return jsonify(resp),status

    except Exception as e  :
        print("ERROR on /Make/group_chat",e)

if __name__  =="__main__":
    app.run(debug=True)