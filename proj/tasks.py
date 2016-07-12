from __future__ import absolute_import
from proj.celery import app
from celery.utils.log import get_task_logger
import requests

logger = get_task_logger(__name__)


@app.task
def add(x, y):
    return x + y


@app.task
def split(a, b):
    logger.info("from {0} to {1}".format(a,b))
    if a > b:
        split(b, a)
    if b - a <= 2:
        logger.info("finish -> a:{0}, b:{1}".format(a, b))
        return a, b
    mid = (a + b)/2
    split(a, mid)
    split(mid, b)


@app.task(max_retries=3, default_retry_delay=2, rate_limit=1)
def crawl(url):
    logger.info("START crawling {0}".format(url))
    r = requests.get(url)
    logger.info("FINISHED status_code: {0} content-type:{1}".format(r.status_code, r.headers['content-type']))





