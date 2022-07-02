from flask import Flask, jsonify, request
  
# creating a Flask app
app = Flask(__name__)

@app.route("/replacement", methods = ['GET'])
def replace():
    inp = request.args.get('input')
    specialChar = ["Oracle","Google","Microsoft","Deloitte","Amazon"]
    for ch in specialChar:
        if ch in inp:
            inp = inp.replace(ch,ch+u"\u00a9")
    return inp

@app.route("/", methods = ['GET'])
def replacing():
    return "hello"
