from flask import current_app
import base64
import bson
import uuid

def store_image(event, mandrill_event):
    db = current_app.extensions['mongo']
    email = mandrill_event['msg']

    default = lambda obj, key, val: obj[key] if key in obj else val

    if 'attachments' in email:
        for attachment in email['attachments'].values():
            photo = {
                '_id': uuid.uuid4(),
                'event': event,
                'ts': mandrill_event['ts'],
                'from_name': default(email, 'from_name', ''),
                'from_email': default(email, 'from_email', ''),
                'subject': email['subject'],
                'text': email['text'],
            }
            photo['raw'] = bson.Binary(base64.b64decode(attachment['content']))
            photo['type'] = attachment['type']
            db.photos.save(photo)
    else:
        current_app.logger.warning('No attachments on email.')