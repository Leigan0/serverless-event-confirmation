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
  return jsonify({'attendees': res['Items']})

@app.route('/attendees/new', methods=['POST'])
def attendee_new():
    name = request.args.get('name')
    gf = request.args.get('gf')
    uuidGen = str(uuid.uuid4())
    db.put_item(
        Item={
            'id': uuidGen,
            'name': name,
            "GF": gf,
            "team":'2'
        }
    )
    print("Written data into dynamoDB")
    return jsonify({'status': 'added'})