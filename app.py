# app.py
# Python 3.7.4
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
import os
import flex_leiloes
from database import service, models

app = Flask(__name__)

load_dotenv()

app.config['MONGODB_SETTINGS'] = {
    'host': os.getenv('MONGODB_URI')
}

# Connect to database
db = MongoEngine(app)


@app.route('/testdb/', methods=['GET'])
def testDb():
    print('testing DB DB DB')
    currentAuctions = flex_leiloes.getCurrentAuctions(models.Auction)
    print(f'Current flex leiloes auctions #: {len(currentAuctions)}')
    service.updateAuctions(flex_leiloes.source, currentAuctions)
    print('END testing DB E N D')
    return "<h1>UNDER CONSTRUCTION </h1>"


@app.route('/getmsg/', methods=['GET'])
def respond():
    print('GET GOT ....')

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
    # TODO remove debug?
    app.run(threaded=True, port=5000, debug=True)

