from datetime import datetime
import pymongo
import instagram
import gevent

next_tag_update = None

def poll_instagram(tag, instagram_client_id, db):
    instagram_api = instagram.InstagramAPI(client_id=instagram_client_id)

    photos, next = instagram_api.tag_recent_media(tag_name=tag, client_id=instagram_client_id)
    for photo in photos:
        entry = {
            'name': photo.user.full_name,
            'caption': photo.caption.text if photo.caption else '',
            'username': photo.user.username,
            'url': photo.get_standard_resolution_url(),
            'source': 'instagram',
            'ts': datetime.utcnow()
        }

        db.photos.save(entry)

def process_instagram_update(update):
    gevent.spawn(poll_instagram,
        update['object_id'],
        current_app.config['INSTAGRAM_CLIENT_ID'],
        current_app.extensions['mongo']
    )


