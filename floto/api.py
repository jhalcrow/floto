from flask import Blueprint, request, current_app, session,\
 jsonify, send_file, abort, url_for
from StringIO import StringIO
import json
import time
from datetime import datetime
import pymongo
from bson import ObjectId
import uuid
from instagram import subscriptions
from .util import store_image
from .tasks import process_instagram_updates, verify_instagram_sig

api = Blueprint('api', __name__)

@api.route("/events/<event_id>/incoming", methods=["POST", "HEAD"])
def recieve_photo(event_id):
    '''
    Adds a new photo for an event, should be called by
    Mandrill when an email is recieved
    '''
    # This is for mandrill to test that the call is working
    if request.method == 'HEAD':
        return ""
    for message_event in json.loads(request.form['mandrill_events']):
        db = current_app.extensions['mongo']
        base_url = current_app.config['S3_BASE_URL']
        store_image(db, base_url, event_id, message_event)
    return "OK"


@api.route("/events/<event_id>/tip")
def get_tip(event_id):
    '''
    Get the metadata n most recent photos
    '''
    db = current_app.extensions['mongo']
    n = int(request.args.get('n', 6))
    recent = db.photos.find({'event': event_id}, 
        sort=[('ts', pymongo.DESCENDING)]).limit(n)
    response = {'photos': 
        [{'name': p['name'],
          'ts': time.mktime(p['ts'].timetuple()),
          'caption': p['caption'],
          'url': p['url'],
          'id': str(p['_id'])} for p in recent
        ]
    }
    if response['photos']:
        session['last_ts'] = response['photos'][0]['ts']
    return jsonify(response)
    

@api.route("/events/<event_id>/new")
def get_new(event_id):
    '''
    Get any new photos since the last call, up to n
    '''
    
    db = current_app.extensions['mongo']
    n = int(request.args.get('n', 6))
    query = {'event': event_id}
    if 'last_ts' in session:
        query['ts'] = {'$gt': datetime.fromtimestamp(session['last_ts'])}
    recent = db.photos.find(query,sort=[('ts', pymongo.DESCENDING)]).limit(n)
    response = {'photos': 
        [{'name': p['name'],
          'ts': time.mktime(p['ts'].timetuple()),
          'caption': p['caption'],
          'url': p['url'],
          'id': str(p['_id'])} for p in recent
        ]
    }
    if response['photos']:
        session['last_ts'] = response['photos'][0]['ts']
    return jsonify(response)

@api.route("/events/<event_id>/instagram_realtime", methods=["GET", "POST"])
def on_realtime_callback(event_id):
    mode = request.args.get("hub.mode")
    challenge = request.args.get("hub.challenge")
    verify_token = request.args.get("hub.verify_token")
    if challenge: 
        return challenge
    else:
        x_hub_signature = request.headers.get('X-Hub-Signature')
        if verify_instagram_sig(current_app.config['INSTAGRAM_CLIENT_SECRET'], request.data, x_hub_signature):
            process_instagram_updates(event_id, request.json)
            return 'OK'
        else:
            current_app.logger.error("Signature mismatch")
            return 'Bad request'
