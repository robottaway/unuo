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


## Unuo File

The unuo file is simple. It is merely a dynamic [Docker file](https://docs.docker.com/reference/builder/). This means you can
add in logic. It uses Jinja to render itself. Once rendered it will be passed
to the ```docker build``` command via stdin.

How should you get started? Just drop a file named Unuo in the base of your
project to be cloned from Git. It probably will be best to start by writing it
in the standard Docker file format. Once you get comfortable you can start 
adding dynamic features.


## Kicking off Builds

This is why you want unuo. You can kick off a build to unuo by simply POSTing
to ```/build/<profile name>```. This endpoint will create a variable ```payload```
which contains a hash created from the POST body. This means the POST body must
be a JSON object.

So what good does this do? Well for one the payload is available in your unuo
file! This means you can do things like pass in the repo, branch and commit
hash mapping to a push to a Git repo. With this data you can clone that repo,
checkout that branch and version, all in your unuo file. Now you are building
Docker containers that track your pushes!

Another powerful feature is passing in the Docker file FROM value. For example
say you want to test your project against 2 or more versions of MySQL. Simply
configure 2 calls to the build endpoint on push, each specifying a different
FROM value. Now you have 2 containers that you can then use to test your
application. You can do that manually or have another process that will take
the containers and automatically test them.


## Github

We pretty much have built unuo to handle Github webhooks :)

That means we are interested in ```push``` events, and will kick off a build
when a webhook from Github calls on such.

It would be useful to most users to check out the documentation on the push
payload, [found here](https://developer.github.com/v3/activity/events/types/#event-name-17).

The payload of any call to kick off a build will always be mapped to the 
variable ```payload```, which means it can then be utilized in your unuo file
to do things like check out a specfic branch and commit hash so that you can
track checkins with builds!


