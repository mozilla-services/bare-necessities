from celery import Celery
from src import config

BROKER_URL =  f"sqla+{config.SQLALCHEMY_DATABASE_URI}"
app = Celery('src.tasks.tasks', broker=BROKER_URL)

@app.task
def hello():
    return f"hello world from {hello.request.id}"