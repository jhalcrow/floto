from datetime import datetime
from flask import current_app
import pymongo
import instagram
from threading import Thread
import hmac
import hashlib

next_tag_update = None

def verify_instagram_sig(secret, message, signature):
    '''Taken from official Instagram client'''
    digest = hmac.new(secret.encode('utf-8'),
                      msg=message.encode('utf-8'),
                      digestmod=hashlib.sha1
            ).hexdigest()
    return digest == signature


def poll_instagram(tag, instagram_client_id, db, event_id):
    instagram_api = instagram.InstagramAPI(client_id=instagram_client_id)

    photos, next = instagram_api.tag_recent_media(tag_name=tag, client_id=instagram_client_id)
    for photo in photos:
        entry = {
            'name': photo.user.full_name,
            'event': event_id,
            'caption': photo.caption.text if photo.caption else '',
            'username': photo.user.username,
            'url': photo.get_standard_resolution_url(),
            'source': 'instagram',
            'ts': photo.created_time,
        }

        db.photos.save(entry)

def process_instagram_updates(event_id, updates):
    for update in updates:
        Thread(target=poll_instagram,
            args=(
            update['object_id'],
            current_app.config['INSTAGRAM_CLIENT_ID'],
            current_app.extensions['mongo'],
            event_id
            )
        ).start()
