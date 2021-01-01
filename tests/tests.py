import json
import os
import unittest
from threading import Thread

from dataStoreExceptions import *
from ds.__init__ import DataStore

location = os.getcwd() + '\\data_store.json'


class DBTestCases(unittest.TestCase):
    """ A class to cover unit tests """

    def setUp(self) -> None:
        self.db = DataStore()

    def test_location(self):
        self.assertTrue(os.path.exists(location))

    def test_createDB(self):
        self.db.create('key', json.dumps({'a': 'test'}))

    def test_d_read(self):
        self.assertEqual('test', self.db.read("key")["a"])

    def test_delete(self):
        self.db.delete("key")

        with self.assertRaises(KeyNotExistException):
            self.db.read("key")

    def test_deletes_with_ttl_expired(self):

        # deliberately expired
        self.db.create('time', json.dumps({}), -10)

        with self.assertRaises(KeyExpiredException):
            self.db.delete('time')

    def test_json_overflow(self):

        # loading JSON data of 20KB
        with open('tests/overflow.json') as f:
            data = json.load(f)

        with self.assertRaises(ValueSizeExceededException):
            self.db.create('big', json.dumps(data))

    def test_key_overflow(self):

        with self.assertRaises(KeyLengthExceededException):
            self.db.create("abcdefghijklmnopqrtuvwa12345623253132", json.dumps({}))

    def test_inserts_parallel(self):
        def inserte(val):
            try:
                self.db.create('time', json.dumps({}), val)
            except:
                pass

        p1 = Thread(target=inserte, args=(1,))
        p2 = Thread(target=inserte, args=(2,))

        p1.start()
        p2.start()

        p1.join()
        p2.join()

        self.assertIsNotNone(self.db.read('time'))

    def test_negative_NonExistentKey(self):
        with self.assertRaises(KeyNotExistException):
            self.db.read('new')

    def test_negative_NumericKey(self):
        with self.assertRaises(InvalidKeyException):
            self.db.create(1, json.dumps({}))

    def test_negative_NotAJson(self):
        with self.assertRaises(InvalidJsonObjectException):
            self.db.create('cx', 'string')

    def test_negative_StringTTL(self):
        with self.assertRaises(TimeToLiveValueErrorException):
            self.db.create('a', json.dumps({}), 'aaa')


# driver code
if __name__ == '__main__':
    unittest.main()
