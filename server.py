import datetime
import time

import  flask

from flask import Flask, request

app = Flask(__name__)
messages = [
    {'username': "Jack", 'time': time.time(), 'text': 'Hello!'},
    {'username': "Mary", 'time': time.time(), 'text': 'Hi, Jack!'},
]
users =  {
    "Jack":"Black",
    "Mary":"1234"
}
@app.route("/")
def hello():
    return '<a href=/status>Status page</a><br><a href=/messages>Messages page</a>'

@app.route("/status")
def status():
    d = {
        "status" : True,
        "time" : datetime.datetime.now().strftime('%Y-%m-%d %H:%M.%S'),
        "users" : len(users),
        "messages" : len(messages)
    }
    return d

@app.route("/messages")
def messages_view():
    print(request.args)
    after = float(request.args['after'])
    filtered_messages = []
    print(after)
    for msg in messages:
        if msg['time'] > after:
            filtered_messages.append(msg)
    print(filtered_messages)
    return {'messages':filtered_messages}

@app.route("/send", methods = ['POST'])
def send_view():
    """
     Send messages here
    :input: {"username":str, "password": str, "text":str}
    :return:
    """
    print(request.json)
    username = request.json["username"]
    password = request.json["password"]
    text = request.json["text"]
    if username not in users or users[username] !=password:
        return {'ok':False}
    messages.append({"username":username, "time":time.time(),"text":text})
    return {'ok':True}

@app.route("/login", methods = ['POST'])
def login_view():
    """
     Send messages here
    :input: {"username":str, "password": str, "text":str}
    :return:
    """
    print(request.json)
    username = request.json["username"]
    password = request.json["password"]

    if username not in users:
        users[username] = password
        return {'ok': True}
    elif users[username] == password:
        return {'ok': True}
    return {'ok':False}

if __name__ == "__main__":
    app.run()