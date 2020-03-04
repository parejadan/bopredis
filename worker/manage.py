import os
import redis
import requests
from rq import Connection, Worker
from flask import Flask
from flask.cli import FlaskGroup

REDIS_URL = os.environ.get("REDIS_URL")
REDIS_QUEUE = os.environ.get("REDIS_QUEUE")


def create_app():
    app = Flask("worker")
    return app


cli = FlaskGroup(create_app=create_app)


@cli.command('run_worker')
def run_worker():
    redis_connection = redis.from_url(REDIS_URL)
    with Connection(redis_connection):
        worker = Worker([REDIS_QUEUE])
        worker.work()


if __name__ == "__main__":
    cli()