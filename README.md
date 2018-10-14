Overview
========

REST API functional tests for https://jsonplaceholder.typicode.com/

Software requirements
=====================

- Python v3.5 and higher.
- Docker stable release (for run tests from a docker container).

Test structure
==============

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
docker run -v $(pwd)/testres:/testres -e TESTMOUNTDIR=/testres --user $(id -u $(whoami)):$(id -g $(whoami)) placeholdertests

```

**Note:** the environment variable `TESTMOUNTDIR` must be a mount point of your host directory where you expect saving test results.

**Note:** the passing your user ID and group ID by argument `--user` is needed to avoid a creation of test result xml with root permissions.