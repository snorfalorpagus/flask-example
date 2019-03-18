FROM python:3.7-slim-stretch

RUN pip install pipenv
ADD Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

ADD app/ app/

EXPOSE 5000

ENTRYPOINT [ "gunicorn", "app.wsgi", "--worker-class", "gevent", "--bind", "0.0.0.0:5000" ]
