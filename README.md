Overview
========

REST API functional tests for https://jsonplaceholder.typicode.com/

Software requirements
=====================

- Python v3.5 and higher.
- Docker stable release (for run tests from a docker container).

Test structure
==============

The tests are written against a black box. They cover all resources (user, post, comment, album, photo, todo) and actions under them (get, create, update, delete, filter). Assumed `jsonplaceholder` server processes all received data verifying just one required field - resource id.

The tests are written using the following test design techniques: Boundary Value Analysis, Equivalence Partitioning, Use Case Testing, Error Guessing.

Information about available resources is taken from https://jsonplaceholder.typicode.com/.

The tests are separated by groups:
- default_endpoints
- users
- posts
- comments
- albums
- photos
- todos

The group `default_endpoints` checks availability of default resource endpoints (/users, /posts, /comments, /albums, /photos, /todos) and allowed methods.

Other groups check the following actions under the corresponding resource: get, create, update, delete, filter, nested resources (please take a look at https://github.com/typicode/jsonplaceholder#nested-resources).

These group names may be used to run the corresponding test group - use flag `-m group_name`. For example, `users` group can be executed by the following command:

```bash
pytest -m users
```

_for more details please take a look at the chapter `How to run tests`_

How to run tests
================

Assume you satisfy the software requirements. And you are ready to run tests.  

There are two recommended ways where tests should be run:
- inside a python virtualenv
- inside a docker container

**Note:** the following commands are performed in the project root directory. 

**Note:** the following commands are performed for Ubuntu 16.04. If you want to execute tests somewhere else you need to find out ways how to do it yourself.

From a virtual env
------------------

Install the system dependencies:

```bash
sudo apt-get install -y virtualenv
```

Create a virtual env and install requirements:

```bash
virtualenv --python=<path to Python interpreter. It must be v3.5 and higher> venv
source venv/bin/activate
pip install --no-cache-dir -r requirements.txt
```

Run tests:

```bash
pytest --junit-xml test_result.xml
```

The test result will be stored in `test_result.xml`. You can change where store result by passing argument `--junit-xml`.

If you want to run a certain group of tests use flag `-m` with name of test group as value:

```bash
pytest --junit-xml test_result.xml -m TEST_GROUP_NAME
```


From a docker container
-----------------------

Build a docker image:

```bash
docker build -t placeholdertests ./
```

If you run docker using `sudo` you probably will meet problem with permission to result saving. To avoid it create directory where test result will be stored on your host machine:

```bash
mkdir -p $(pwd)/testres
```

Run a docker container:

```bash
docker run --rm -v $(pwd)/testres:/testres -e TESTMOUNTDIR=/testres --user $(id -u $(whoami)):$(id -g $(whoami)) placeholdertests

```

**Note:** the environment variable `TESTMOUNTDIR` must be a mount point of your host directory where you expect saving test results.

**Note:** the passing your user ID and group ID by argument `--user` is needed to avoid a creation of test result xml with root permissions.

If you want to run a certain group of tests use flag `-m` with name of test group as value:

```bash
docker run --rm -v $(pwd)/testres:/testres -e TESTMOUNTDIR=/testres --user $(id -u $(whoami)):$(id -g $(whoami)) placeholdertests -m TEST_GROUP_NAME

```
