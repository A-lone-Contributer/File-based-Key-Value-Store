import json
import os
from threading import Lock
from time import time

from dataStoreExceptions import *


class DataStore:
    """
    A class used to define a file based key-value datastore
    """

    __instance = None

    def __init__(self, file_path=None):
        """
         Parameters
         ----------
         file_path : str, optional
             The name of the animal (defaultFile_path = current directory +'\\data_store.json')

        Raises
        ------
        FileNotFoundException
            If the file specified is not found.

        FileNotAccessibleException
            If the file specified is not accessible.

        IOErrorOccurredException
            If IO operation of a file fails.
        """

        if DataStore.__instance is not None:
            raise Exception("This is a Singleton Class!")
        else:
            self.__file_path = file_path
            self.__lock = Lock()
            if self.__file_path:
                if not os.access(self.__file_path, os.F_OK):
                    raise FileNotFoundException
                elif not os.access(self.__file_path, os.R_OK):
                    raise FileNotAccessibleException
                try:
                    with open(self.__file_path):
                        pass
                except IOError:
                    raise IOErrorOccurredException
            else:
                self.__file_path = os.getcwd() + '\\data_store.json'

            # creating of JSON file if the default file path is chosen for the first time
            with open(self.__file_path, 'a+'):
                pass

            self.__file_size = os.stat(self.__file_path).st_size

    @staticmethod
    def __ValidateKey(self):
        """
        A private function to validate key length and type

        Raises
        ------
        InvalidKeyException
            If the specified key is not in string format.

        KeyLengthExceededException
            If the key specified exceeds 32 character.
        """

        # check for key type
        if type(self.__key) is not str:
            raise InvalidKeyException

        # check for key length
        elif len(self.__key) > 32:
            raise KeyLengthExceededException

    def create(self, key, value, timeToLive=-1):

        """
         Creates new entry to json file, with specified key, value and timeToLive Property

         Parameters
         ----------
         key :  <class 'str'> with maximum length of 32 characters
             The key in string format

        value : <class 'jsonObject' > with maximum size of 16KB
            The value for key

        timeToLive : int, optional
            An integer defining the number of seconds the key must be retained in the data store

        Raises
        ------
        InvalidJsonObjectException
            If the object is not a valid JSON Object.

        ValueSizeExceededException
            If the value size exceeds 16 KB.

        FileSizeExceededException
            If the file size exceeds 1GB.

        timeToLiveValueError
            If there is a type mismatch for timeToLive property.

        DuplicateKeyException
            If the key already exists.

        InvalidJSONFileException
            If json file contains json array, valid json file requires to be a JSON Object.
        """
        self.__key = key
        self.__value = value
        self.__timeToLive = timeToLive

        # get size of JSON Object value
        self.__value_size = self.__value.__sizeof__()
        self.__ValidateKey(self)

        try:

            # check if value is valid json object
            json.loads(self.__value)

        except json.JSONDecodeError:
            raise InvalidJsonObjectException

        # locks the client process and provide thread safe
        with self.__lock:

            # to get dataStore file size
            self.__file_size = os.stat(self.__file_path).st_size

            # Check for JSON object size (>16KB) (1 KiloByte = 1024 Bytes)
            if self.__value_size > (1024 * 16):
                raise ValueSizeExceededException

            # check for file size
            elif (self.__value_size + self.__file_size) > (1024 * 1024 * 1024):
                raise FileSizeExceededException

            # check for timeToLive type

            if type(self.__timeToLive) is not int:
                raise TimeToLiveValueErrorException

            if self.__timeToLive > 0:
                try:
                    self.__timeToLive = int(self.__timeToLive)
                except:
                    raise TimeToLiveValueErrorException
            else:
                pass

            # getting time of creation to manipulate timeToLive property
            self.__timeStamp = int(time())

            # adding key, value pair to dataStore
            with open(self.__file_path, 'r+') as self.__dataStoreFptr:

                # data is python object, dict() and Key has a tuple value (jsonObject, time to live attribute in
                # seconds, time of creation of the KeyValue pair) making the key value immutable data
                self.__data = {self.__key: (json.loads(self.__value), self.__timeToLive,
                                            self.__timeStamp)}

                if self.__file_size == 0:

                    # Serialize python object to a JSON formatted string and added to dataStore file
                    self.__dataStoreFptr.write(json.dumps(self.__data, indent=4))
                    print("Key creation successful!")

                else:
                    try:
                        self.__data_store = json.load(self.__dataStoreFptr)

                    # Deserialize JSON file to a Python object, dict ()
                    except json.JSONDecodeError:
                        raise InvalidJsonFileException

                    # check if key is already in datastore
                    if self.__key in self.__data_store:
                        raise DuplicateKeyException(self.__key)
                    else:
                        try:
                            # data added to data_store object containing all data from json file
                            self.__data_store.update(self.__data)

                        except AttributeError:
                            raise InvalidJsonFileException

                        # resets the file pointer to position 0
                        self.__dataStoreFptr.seek(0)

                        # overwrite json file with data_store dict()
                        json.dump(self.__data_store, self.__dataStoreFptr, indent=4)

                        print("Key creation successful!")

    def read(self, key):
        """
         Reads the file, validates the key requested from client

         Parameters
         ----------
         key : str
             The key in string format

        Returns
        -------
        The response from DataStore, if Time-To-Live condition satisfied

        Raises
        ------
        EmptyFileException
            If the datastore is empty.

        InvalidJsonFileException
            If the file is doesn't contain JSON in specified format

        KeyNotExistException
            If the key is not found

        """
        with self.__lock:
            self.__file_size = os.stat(self.__file_path).st_size
            self.__key = key
            self.__ValidateKey(self)

            if self.__file_size == 0:
                raise EmptyFileException

            with open(self.__file_path, 'r') as self.__dataStoreFptr:
                try:
                    self.__data_store = json.load(self.__dataStoreFptr)
                except json.JSONDecodeError:
                    raise InvalidJsonFileException

                # Deserialize JSON file to a Python object, dict () and check Key existence
                if self.__key not in self.__data_store:
                    raise KeyNotExistException(self.__key)

                else:
                    self.__data = self.__data_store[self.__key]
                    try:

                        if self.__data[1] < 0:
                            return self.__data[0]

                        self.__isValidTimeToLive = (int(time()) - self.__data[2]) < self.__data[1]
                    except:
                        raise InvalidJsonFileException

                    # check if difference between current time and time of creation is less than time-to-Live value
                    if self.__isValidTimeToLive:
                        return json.loads(json.dumps(self.__data[0]))
                    else:
                        raise KeyExpiredException(self.__key)

    def delete(self, key):
        """
        Deletes or removes JSONObject for given Key,if Valid key and Time-To-Live condition satisfied

        Raises
        ------
        EmptyFileException
            If the datastore is empty.

        InvalidJsonFileException
            If the file is doesn't contain JSON in specified format

        KeyNotExistException
            If the key is not found

        KeyExpiredException
            If the key has expired
        """
        with self.__lock:
            self.__file_size = os.stat(self.__file_path).st_size
            self.__key = key
            self.__ValidateKey(self)

            # check for empty file
            if self.__file_size == 0:
                raise EmptyFileException

            with open(self.__file_path, 'r+') as self.__dataStoreFptr:
                try:
                    self.__data_store = json.load(self.__dataStoreFptr)
                except json.JSONDecodeError:
                    raise InvalidJsonFileException

            # Deserialize JSON file to a Python object, dict () and check Key existence
            if self.__key not in self.__data_store:
                raise KeyNotExistException(self.__key)
            else:
                self.__data = self.__data_store[self.__key]

                # check if difference between current time and time of creation is less than time-to-Live value
                self.__isValidTimeToLive = (int(time()) - self.__data[2]) < self.__data[1]

                if self.__data[1] == -1 or self.__isValidTimeToLive > 0:

                    # delete the file and recreate with new data store
                    del self.__data_store[self.__key]
                    print("Key deletion successful!")
                    os.remove(self.__file_path)
                else:
                    raise KeyExpiredException(self.__key)

                with open(self.__file_path, 'w') as self.__dataStoreFptr:
                    json.dump(self.__data_store, self.__dataStoreFptr, indent=4)
