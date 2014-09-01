## README

[![Build Status](https://travis-ci.org/robottaway/unuo.svg?branch=master)](https://travis-ci.org/robottaway/unuo)

unuo is a simple Docker tool that allows you to kick off Docker builds from 
anywhere. Most likely this will involve a CI system calling, which in will 
prompt unuo to checkout the required Git repo and using the Dockerfile make a 
container. If you like it can push the container on build to a Docker registry.


## Install

Installing is pretty simple:

1. make a virtual environment and activate it
1. ```pip install -r requirements.txt```


## Running

To run the app ```python unuo/app.py```


## Unit Tests

First install dependencies: ```pip install -r requirements_test.txt```

To run the unit tests: ```python setup.py test```

or if you want to run them and get test coverage: ```./coverage.sh```
