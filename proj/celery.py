from __future__ import absolute_import

from celery import Celery

app = Celery('proj',
             broker='amqp://',
             include=['proj.tasks'])

# more info here: http://docs.celeryproject.org/en/latest/configuration.html
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
    CELERYD_CONCURRENCY=1,
    CELERY_DEFAULT_RATE_LIMIT=5
)

if __name__ == '__main__':
    app.start()
