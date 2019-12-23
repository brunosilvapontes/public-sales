# app.py
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import os
app = Flask(__name__)

load_dotenv()
# Connect to database
app.config["MONGO_URI"] = os.getenv('MONGODB_URI')
mongo = PyMongo(app)


@app.route('/getmsg/', methods=['GET'])
def respond():
    testMongo = mongo.db.testcollection.find_one({'test': 123321})
    print('GET GET ...')
    print(testMongo)

    # Retrieve the name from url parameter
    # name = request.args.get("name", None)
    name = 'bbrr'

    # For debugging
    print(f"got name {name}")

    response = {}

    # Check if user sent a name at all
    if not name:
        response["ERROR"] = "no name found, please send a name."
    # Check if the user entered a number not a name
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"Welcome {testMongo} to our awesome platform!!"

    # Return the response in json format
    return jsonify(response)


# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
