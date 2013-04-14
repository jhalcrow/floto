import unittest
import floto
import bson
import pymongo
import uuid
from floto.config import TestingConfig
from floto.util import store_image
import base64

class DisplayTest(unittest.TestCase):

    def setUp(self):
        self.app = floto.create_app(TestingConfig)
        self.db = pymongo.Connection().test

    def tearDown(self):
        self.db.photos.remove()

    def test_get_photo(self):
        _id = insert_mock_photo(self.db, 'Name', 'subject', 1)
        client = self.app.test_client()
        rv = client.get('/floto/api/photos/%s' % _id)
        self.assertEquals(rv.data, '1234')
        self.assertEquals(rv.content_type, 'image/jpeg')

    def test_no_photo(self):
        client = self.app.test_client()
        rv = client.get("/floto/api/photos/not_real")
        self.assertEquals(rv.status_code, 404)

    def test_store_image(self):
        photo_raw = open('test/indian.jpg').read()
        mandrill_event = { 
            'msg':{
                'from_name': 'Test name',
                'subject': 'Test subject',
                'text': 'Test text',
                'attachments': {
                    'indian.jpg': 
                        { 'content':base64.b64encode(photo_raw),
                          'type': 'image/jpeg'
                        }
                }
            },
            'ts': 1
        }
        
        store_image(self.db, 'test', mandrill_event)

        stored = self.db.photos.find_one()
        expected_raw = open('test/indian-expected.jpg').read()
        self.assertEquals(stored['event'], 'test')
        self.assertEquals(str(stored['raw']), expected_raw)



def insert_mock_photo(db, name, subject, ts):
    _id = uuid.uuid4()
    db.photos.save({
        '_id': _id,
        'from_name': name,
        'subject':subject,
        'ts':ts,
        'raw':bson.Binary('1234'),
        'type':'image/jpeg'
    }, safe=True)
    
    return _id

if __name__ == '__main__':
    unittest.main()