import boto3
from flask import Flask, jsonify, request
import uuid 
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['http://ent.svcs.social.s3-website-eu-west-1.amazonaws.com'])

dynamodb = boto3.resource('dynamodb')
db = dynamodb.Table('social-attendees-dev')

@app.route('/attendees', methods=['GET'])
def attendees_get():
  res = db.scan(
        Select='ALL_ATTRIBUTES'
  )
  print('res.items')
  print(len(res['Items']))
  return jsonify({'attendees': res['Items']})

@app.route('/attendees/new', methods=['POST'])
def attendee_new():
    name = request.args.get('name')
    diet = request.args.get('diet')
    uuidGen = str(uuid.uuid4())
    db.put_item(
        Item={
            'id': uuidGen,
            'name': name,
            "team":team_selection(),
            "diet": diet
        }
    )
    print("Written data into dynamoDB")
    return jsonify({'status': 'added'})

def count_attendees():
    res = db.scan(
        Select='ALL_ATTRIBUTES'
        )  
    print(len(res['Items']))
    return(len(res['Items']))

def team_selection():
    guestCount = count_attendees()
    print("db.count")
    print(db.item_count)
    teams = ["Double Flop", "Raging Bulls Eye", "Dart Vaders", "Smells Like Bulls Hit"]
    if guestCount % 4 == 0: 
        return teams[3]
    elif guestCount % 3 == 0:
        return teams[2]
    elif guestCount % 2 == 0:
        return teams[1]
    else:
        return teams[0]