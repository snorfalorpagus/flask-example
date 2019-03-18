# Example Flask application

A minimal example of a Python web application using:

  * [Flask](http://flask.pocoo.org/) - a web application microframework
  * [Gunicorn](https://gunicorn.org/) -  a WSGI HTTP server
  * [Docker](https://www.docker.com/) - a container runtime
  * [Pipenv](https://pipenv.readthedocs.io/en/latest/) - a package/environment manager
  * [PyTest](https://docs.pytest.org/en/latest/) - a testing framework

## Installing dependencies

Requires Python 3.6 or later, because [f-strings are awesome](https://www.python.org/dev/peps/pep-0498/).

To install dependencies in a virtual environment using Pipenv:

```
$ pipenv install      
Creating a virtualenv for this project…
Pipfile: /Users/snorf/Desktop/flask-example/Pipfile
Using /usr/local/bin/python3.7m (3.7.0) to create virtualenv…

✔ Successfully created virtual environment! 
Virtualenv location: /Users/snorf/.local/share/virtualenvs/flask-example-ngbzQ1mW
Installing dependencies from Pipfile.lock (78bcfc)…
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 9/9 —
```

To activate the virtual environment:

```
$ pipenv shell
Launching subshell in virtual environment…
 . /Users/snorf/.local/share/virtualenvs/flask-example-ngbzQ1mW/bin/activate
➜  flask-example git:(master) ✗  . /Users/snorf/.local/share/virtualenvs/flask-example-ngbzQ1mW/bin/activate
(flask-example) $
```

More information available in the [Pipenv documentation](https://pipenv.readthedocs.io/en/latest/).

## Starting the application

### Development

To run the application in development mode:

```
$ FLASK_APP=app flask run
 * Serving Flask app "app"
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

### Production

To run the application in production using gunicorn:

```
$ gunicorn app.wsgi --worker-class gevent --bind 0.0.0.0:5000

[2019-03-18 21:22:16 +0000] [41951] [INFO] Starting gunicorn 19.9.0
[2019-03-18 21:22:16 +0000] [41951] [INFO] Listening at: http://0.0.0.0:5000 (41951)
[2019-03-18 21:22:16 +0000] [41951] [INFO] Using worker: gevent
[2019-03-18 21:22:16 +0000] [41954] [INFO] Booting worker with pid: 41954
```

## Testing

Unit tests are written using the PyTest framework. Fixtures defined in `tests/conftest.py` are used to initialise the application and provide easy access to the test client. The current directory is automatically added to the `PYTHONPATH` to allow `import app` in the tests.

To run unit tests:

```
$ pytest tests
============================= test session starts ==============================
platform darwin -- Python 3.7.0, pytest-4.3.1, py-1.8.0, pluggy-0.9.0
rootdir: /Users/snorf/Desktop/docker-example, inifile:
collected 2 items                                                              

tests/test_hello.py ..                                                   [100%]

=========================== 2 passed in 0.02 seconds ===========================
```

## Docker

Docker can be used to run the application in production. The `Dockerfile` demonstrates some best practices:

  * Pipenv is run with `--deploy` for reproducible builds
  * Using a small (ish) base image `python:3.7-slim-stretch` produces a 216MB container. Using a smaller image such as `python:3.7-alpine` isn't possible without more work, as `gevent` doesn't provide wheels on PyPI.
  * Dependencies are installed prior to copying the application itself, maximising the use of Docker's layer cache for subsequent builds.

To build a Docker container with the application:

```
$ docker build -t flask-example
Sending build context to Docker daemon  142.8kB
Step 1/7 : FROM python:3.7-slim-stretch
 ---> f9c1866f07ea
Step 2/7 : RUN pip install pipenv
 ---> Using cache
 ---> 75b1c76598bd
Step 3/7 : ADD Pipfile Pipfile.lock ./
 ---> Using cache
 ---> b3199d824780
Step 4/7 : RUN pipenv install --system --deploy
 ---> Using cache
 ---> 14b0ae1c4f16
Step 5/7 : ADD app/ app/
 ---> Using cache
 ---> a125c0595c72
Step 6/7 : EXPOSE 5000
 ---> Using cache
 ---> 9f83830741d8
Step 7/7 : ENTRYPOINT [ "gunicorn", "app.wsgi", "--worker-class", "gevent", "--bind", "0.0.0.0:5000" ]
 ---> Using cache
 ---> 695d1b887f7a
Successfully built 695d1b887f7a
Successfully tagged flask-docker:latest
```

To run the container:

```
$ docker run -p 5000:5000 flask-example
[2019-03-18 21:24:12 +0000] [1] [INFO] Starting gunicorn 19.9.0
[2019-03-18 21:24:12 +0000] [1] [INFO] Listening at: http://0.0.0.0:5000 (1)
[2019-03-18 21:24:12 +0000] [1] [INFO] Using worker: gevent
[2019-03-18 21:24:12 +0000] [8] [INFO] Booting worker with pid: 8
```