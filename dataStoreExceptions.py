"""
This file contains custom exceptions
"""


class DataStoreException(Exception):
    """ Base class for user defined exceptions """
    pass


class FileNotFoundException(DataStoreException):
    def __init__(self, message="File does not exist. Requires valid file path."):
        self.message = message
        super().__init__(self.message)


class FileNotAccessibleException(DataStoreException):
    def __init__(self, message="File can not be accessed. Requires file accessibility to read or write."):
        self.message = message
        super().__init__(self.message)


class IOErrorOccurredException(DataStoreException):
    def __init__(self, message="Caught IO Exception. File can not be accessed."):
        self.message = message
        super().__init__(self.message)


class InvalidKeyException(DataStoreException):
    def __init__(self, message="Key must be a string."):
        self.message = message
        super().__init__(self.message)


class KeyLengthExceededException(DataStoreException):
    def __init__(self, message="Requires valid Key not exceeding the maximum size of 32 characters."):
        self.message = message
        super().__init__(self.message)


class DuplicateKeyException(DataStoreException):
    def __init__(self, key, message=" already exists. Create is invoked for an existing key."):
        self.key = key
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.key} {self.message}'


class InvalidJsonObjectException(DataStoreException):
    def __init__(self, message="Requires value as a valid JSON object."):
        self.message = message
        super().__init__(self.message)


class ValueSizeExceededException(DataStoreException):
    def __init__(self, message="Requires valid JSON object not exceeding the maximum size of 16KB."):
        self.message = message
        super().__init__(self.message)


class FileSizeExceededException(DataStoreException):
    def __init__(self, message="Reached Maximum file size. New data can not be stored."):
        self.message = message
        super().__init__(self.message)


class TimeToLiveValueErrorException(DataStoreException):
    def __init__(self, message="Invalid argument. Requires numerical value defining the number of seconds."):
        self.message = message
        super().__init__(self.message)


class EmptyFileException(DataStoreException):
    def __init__(self, message="File does not have any json object."):
        self.message = message
        super().__init__(self.message)


class KeyNotExistException(DataStoreException):
    def __init__(self, key, message=" does not exist. Requires Valid Key."):
        self.message = message
        self.key = key
        super().__init__(self.message)

    def __str__(self):
        return f'{self.key} {self.message}'


class KeyExpiredException(DataStoreException):
    def __init__(self, key, message="Key exceeded Time-To-Live. Can not be accessed for read or delete operation."):
        self.message = message
        super().__init__(self.message)


class InvalidJsonFileException(DataStoreException):
    def __init__(self, message="Requires valid JSON file containing JSON object in standard format."):
        self.message = message
        super().__init__(self.message)
