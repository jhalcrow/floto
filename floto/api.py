from flask import Blueprint, request, current_app, session,\
 jsonify, send_file, abort, url_for
from StringIO import StringIO
import json
import pymongo
from bson import ObjectId
import uuid
from .util import store_image

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
        store_image(event_id, message_event)
    return "OK"

@api.route("/photos/<photo_id>")
def get_photo(photo_id):
    '''
    Return a particular image
    '''
    db = current_app.extensions['mongo']
    photo = db.photos.find_one({'_id': uuid.UUID(photo_id)})
    if photo:
        return send_file(StringIO(photo['raw']), mimetype=photo['type'])
    else:
        abort(404) 

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
        [{'name': p['from_name'],
           'ts': p['ts'], 
          'id': str(p['_id'])} for p in recent]
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
        query['ts'] = {'$gt': session['last_ts']}
    recent = db.photos.find(query,sort=[('ts', pymongo.DESCENDING)]).limit(n)
    response = {'photos': 
        [{'name': p['from_name'],
          'ts': p['ts'],
          'url': url_for('.get_photo', photo_id=str(p['_id'])),
          'id': str(p['_id'])} for p in recent]
    }
    if response['photos']:
        session['last_ts'] = response['photos'][0]['ts']
    return jsonify(response)
