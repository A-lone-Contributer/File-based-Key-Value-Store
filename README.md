# Freshworks Backend Assignment

A Key-Value DataStore that supports CRD operations by creating a local database on the local machine.

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Testing](#Testing)


<hr>

<!-- ABOUT THE PROJECT -->
# About The Project

A file-based key-value data store that supports the basic CRD  (create, read, and delete)
operations. This data store is meant to be used as a local storage for one single process on one
laptop. The data store must be exposed as a library to clients that can instantiate a class and work
with the data store.


**The data store supports the following functional requirements :**

1. It can be initialized using an optional file path. If one is not provided, it will reliably
create itself in a reasonable location on the laptop.

2. A new key-value pair can be added to the data store using the Create operation. The key
is always a string - capped at 32chars. The value is always a JSON object - capped at
16KB.

3. If Create is invoked for an existing key, an appropriate error must be returned.

4. A Read operation on a key can be performed by providing the key, and receiving the
value in response, as a JSON object.

5. A Delete operation can be performed by providing the key.

6. Every key supports setting a Time-To-Live property when it is created. This property is
optional. If provided, it will be evaluated as an integer defining the number of seconds
the key must be retained in the data store. Once the Time-To-Live for a key has expired,
the key will no longer be available for Read or Delete operations.

7. Appropriate error responses must always be returned to a client if it uses the data store in
unexpected ways or breaches any limits.



**The data store will also support the following non-functional requirements :**

1. The size of the file storing data must never exceed 1GB.

2. More than one client process cannot be allowed to use the same file as a data store at any
given time.

3. A client process is allowed to access the data store using multiple threads, if it desires to.
The data store must therefore be thread-safe.

4. The client will bear as little memory costs as possible to use this data store, while
deriving maximum performance with respect to response times for accessing the data
store.

<hr>

### Built With
* [Python](https://www.python.org/)
* [Unittest](https://docs.python.org/3/library/unittest.html)

<hr>

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

1. **Python**

To check, if python is installed, type <code>python</code> in command line. If this opens <code>python3</code> interpreter then you are good to go. 

else, <code>python3</code> follow [this](https://www.python.org/downloads/) link to download the latest version.

2. **Git**

You can download the latest version of <code>git</code> [here](https://git-scm.com/downloads).

### Installation

* Clone the repo

```sh
git clone https://github.com/A-lone-Contributer/File-based-Key-Value-Store.git
```

<hr>

<!-- USAGE EXAMPLES -->
## Usage

### Import the class
```python
from ds.__init__ import DataStore
```

### Create DataStore Object 
```python
db = DataStore('./data_store.json') # location is optional
```

### Creating a key value pair

```python
db.create('Student', {'Name': 'John Doe'})

# Optional Time-To-Live (TTL) argument 
db.create('TempStudent', {'Name': 'Steven'}, 2) # this {key:json obj} expires in 2 seconds
```

## Reading the key 
```python
name = db.read('Student')
```

## Deleting a key
```python
db.delete('Student')
```



# Testing

To run the unittests, follow the below written steps

1. Navigate to the test folder
```shell
cd tests
```

2. Run the tests file
```
python3 tests.py 
```

After running this file, all the 12 tests cases show run successfully indicating unittest coverage.

### Output

![Product Name Screen Shot][product-screenshot]



[product-screenshot]: unittests.png

<hr>

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/A-lone-Contributer/File-based-Key-Value-Store/issues) for a list of proposed features (and known issues).

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- LICENSE -->
## License

Distributed under the Apache-2.0 License. See `LICENSE` for more information.

<!-- CONTACT -->
## Contact

Nishkarsh Tripathi : nishkarsh78@gmail.com

Project Link : [DFile-based-Key-Value-Store](https://github.com/A-lone-Contributer/File-based-Key-Value-Store)

