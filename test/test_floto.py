import unittest
import floto
import bson
import pymongo
import uuid
from floto.config import TestingConfig
from datetime import datetime
import floto.util
import base64
from mock import patch, Mock


class DisplayTest(unittest.TestCase):

    def setUp(self):
        with patch('floto.s3_setup'):
            floto.s3_setup.return_value = (Mock(), Mock())
            self.app = floto.create_app(TestingConfig)
        self.db = pymongo.Connection().test

    def tearDown(self):
        self.db.photos.remove()

    def test_store_image(self):
        
        mandrill_event = { 
            'msg':{
                'from_name': 'Test name',
                'subject': 'Test subject',
                'text': 'Test text',
                'attachments': {
                    'indian.jpg': 
                        { 'content':'original',
                          'type': 'image/jpeg'
                        }
                }
            },
            'ts': 1
        }
        
        with patch('floto.util.process_image_bytes'), patch('floto.util.s3upload'):
            mock_bytes = Mock()
            floto.util.process_image_bytes.return_value = 'processed'
            floto.util.store_image(self.db, 'http://test/', 'test', mandrill_event)
            stored = self.db.photos.find_one()
            
            photo_id = str(stored['_id'])
            floto.util.s3upload.assert_called_with('processed', photo_id)
            
            self.assertEquals(stored['event'], 'test')
            self.assertEquals(stored['name'], 'Test name')
            self.assertEquals(stored['caption'], 'Test subject')
            self.assertEquals(stored['ts'], datetime.fromtimestamp(1))
            self.assertEquals(stored['url'], 'http://test/%s' % photo_id)


    def test_process_image(self):
        photo_raw = open('test/indian.jpg').read()
        expected_raw = open('test/indian-expected.jpg').read()
        out = floto.util.process_image_bytes(photo_raw)
        self.assertEquals(out, expected_raw)



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