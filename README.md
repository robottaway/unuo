## README

[![Build Status](https://travis-ci.org/robottaway/unuo.svg?branch=master)](https://travis-ci.org/robottaway/unuo) [![Coverage Status](https://img.shields.io/coveralls/robottaway/unuo.svg)](https://coveralls.io/r/robottaway/unuo?branch=master)

unuo is a simple Docker tool that allows you to kick off Docker builds from 
anywhere. It provides a simple RESTful api which allows other tools and scripts
to integrate and have the ability to dockerize.

Most likely this will involve a CI system calling, which in will 
prompt unuo to checkout the required Git repo and using the Dockerfile make a 
container. If you like it can push the container on build to a Docker registry.


## Requirements

There aren't many. You can run on Linux or Mac. You will need:

- [Python](https://www.python.org/) 2.7
- [docker](https://www.docker.com/) 1+
- [boot2docker](http://boot2docker.io/) (if running on Mac)
- [pip](https://pip.readthedocs.org/en/latest/)

nice to have for installation:

- [virtualenv](http://virtualenv.readthedocs.org/en/latest/) (to keep from crufting up the Python site packages)
- [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) (to make working with VEs easy)


## Install

Installing is pretty simple:

1. make a virtual environment and activate it
  - e.g. ```mkvirtualenv unuo``` with virtualenvwrapper
1. ```pip install -r requirements.txt```
1. ```python setup.py develop``` if you are developing, otherwise ```python setup.py install```


## Running on Linux

To run the app ```python unuo/app.py```


## Running on Mac

You will be using boot2docker on a mac, which provides a docker command which 
while acting like the usual docker command actually proxies request to a linux
VM running a bonafide docker process.

To make this work you will need to ensure that the shell has been configured 
properly which means exporting the connection details for this proxy command.
When you run ```boot2docker start``` it will finish by printing the 'export' 
command you will need to run to make this work. 

Make sure that you do this prior to running unuo in a shell otherwise it will
fail to properly invoke the docker proxy command.


## Unit Tests

First install dependencies: ```pip install -r requirements_test.txt```

To run the unit tests: ```python setup.py test```

or if you want to run them and get test coverage: ```./coverage.sh```


