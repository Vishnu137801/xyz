import time
from flask import Flask
from celery import Celery

app = Flask(__name__)

# Configure Celery
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379"
app.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379"

celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])

# Define a Celery task
@celery.task(name="long_running_task")
def long_running_task():
    time.sleep(5)
    return "The task is done!"

# A simple endpoint that starts the Celery task
@app.route("/")
def index():
    task = long_running_task.delay()
    return "The task has been started. Check the logs to see when it's done."

if __name__ == "__main__":
    app.run()
