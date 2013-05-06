from flask import current_app, make_response, request
from datetime import datetime, timedelta
from functools import update_wrapper

import StringIO
import base64
import bson
import uuid
import random
from PIL import Image
from boto.s3.key import Key

ORIENTATION_TAG = 0x0112 # EXIF Orientation tag

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

def store_image(db, base_url, event, mandrill_event):
    email = mandrill_event['msg']

    default = lambda obj, key, val: obj[key] if key in obj else val

    if 'attachments' in email:
        for attachment in email['attachments'].values():
            photo = {
                '_id': uuid.uuid4(),
                'event': event,
                'ts': datetime.fromtimestamp(mandrill_event['ts']),
                'name': default(email, 'from_name', ''),
                'username': default(email, 'from_email', ''),
                'caption': email['subject'],
                'source': 'email',
                'random': random.random(),
            }
            photo_id = str(photo['_id'])
            photo['url'] = base_url + photo_id

            raw_bytes = base64.b64decode(attachment['content'])
            processed_bytes = process_image_bytes(raw_bytes)
            s3upload(processed_bytes, photo_id)
            db.photos.save(photo)

    else:
        current_app.logger.warning('No attachments on email.')

def s3upload(bytes, key):
    bucket = current_app.extensions['s3_bucket']
    k = Key(bucket)
    k.key = key
    k.set_contents_from_string(bytes)
    k.make_public()

def process_image_bytes(bytes):
    img = Image.open(StringIO.StringIO(bytes))
    img = orient_img(img)
    img = resize_img(img)

    img_buf = StringIO.StringIO()
    format = img.format or 'JPEG'
    img.save(img_buf, format)
    return img_buf.getvalue()


def orient_img(img):
    '''
    Reorients an image to EXIF orientation 1 (aka normal)
    '''
    if img._getexif() and ORIENTATION_TAG in img._getexif():
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

def resize_img(img, width=1280, max_height=720):
    '''
    Scales an image to the specified width
    '''
    orig_w, orig_h = img.size
    scale_w = float(width) / orig_w
    scale_h = float(max_height) / orig_h
    scale = min(scale_w, scale_h)
    return img.resize((int(scale*orig_w), int(scale*orig_h)), Image.ANTIALIAS)

