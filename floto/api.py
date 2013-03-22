from flask import Blueprint, request, current_app

api = Blueprint('api', __name__)

@api.route("/events/<event_id>/incoming", methods=["POST"])
def recieve_photo(event_id):
    '''
    Adds a new photo for an event, should be called by
    Mandrill when an email is recieved
    '''
    message = request.json
    current_app.logging.debug(json.dumps(message))

@api.route("/photos/<photo_id>")
def get_photo(photo_id):
    '''
    Return a particular image
    '''
    return "Get photo %s" % photo_id

@api.route("/events/<event_id>/tip")
def get_tip(event_id):
    '''
    Get the metadata n most recent photos
    '''
    n = int(request.args.get('n', 5))
    return "Get %s" % n


@api.route("/events/<event_id>/new")
def get_new(event_id):
    '''
    Get any new photos since the last call, up to n
    '''
    n = int(request.args.get('n', 5))
    return "Get %s" % n