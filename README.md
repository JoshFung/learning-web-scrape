# learning-web-scrape

## Installation
Ensure you install RabbitMQ as it will be needed to run alongside Celery

Currently, Chromedriver v103 is broken. Thus, you will also need to install the Chromedriver beta for now.
Furthermore, set the path to the chromedriver file in the `.env` file.

## Steps

1. Install RabbitMQ
2. Ensure that your environment variables are set up in `.env`
3. Start up RabbitMQ using `rabbitmq-server` in a terminal
   1. Wait until it completes when message `Starting broker... completed with x plugins`
4. Start up the actual service with the Celery command: `celery -A script worker -B -l INFO`
   1. `-A script` specifies which project
   2. `-B` tells it to run on the given beat schedule (10 minutes per run)
   3. `-l INFO` tells it log information

### Alternative Steps Without a Schedule

1. Do the same first three steps as above
2. Start up the Celery service using: `celery -A script worker -l INFO`
   - Note that we don't use `-B` as we don't want it on a service
3. Open up a third terminal and enter the Python console (just use `python`)
4. Import the `scrape()` function by using: `from script import scrape`
5. Run `scrape()` by using: `scrape.delay()`
   - `delay()` sends a task message to RabbitMQ which further tells Celery it has a job to do
     - Further, note that `delay()` is a shortcut for `apply_async()` as it does not have execution options
