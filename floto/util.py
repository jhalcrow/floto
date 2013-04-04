from flask import current_app
import base64
import bson
import uuid
from PIL import Image
ORIENTATION_TAG = 0x0112 # EXIF Orientation tag

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
            raw_bytes = base64.b64decode(attachment['content'])
            img = Image.open(StringIO.StringIO(raw_bytes))
            img = orient_img(img)
            photo['raw'] = bson.Binary(img.tostring())
            photo['type'] = attachment['type']
            db.photos.save(photo)
    else:
        current_app.logger.warning('No attachments on email.')

def orient_img(img):
    '''
    Reorients an image to EXIF orientation 1 (aka normal)
    '''
    device_orientation = img._getexif()[ORIENTATION_TAG]
    if device_orientation == 2:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    elif device_orientation == 3:
        img = img.transpose(Image.ROTATE_180)
    elif device_orientation == 4:
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
    elif device_orientation == 5:
        img = img.transpose(Image.ROTATE_270).transpose(Image.FLIP_LEFT_RIGHT)
    elif device_orientation == 6:
        img = img.transpose(Image.ROTATE_270)
    elif device_orientation == 7:
        img = img.transpose(Image.ROTATE_90).transpose(Image.FLIP_LEFT_RIGHT)
    elif device_orientation == 8:
        img = img.transpose(Image.ROTATE_90)

    return img

