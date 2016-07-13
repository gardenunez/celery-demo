from __future__ import absolute_import
from proj.celery import app
from celery.utils.log import get_task_logger
from celery import Task
from celery.exceptions import Reject
import requests

logger = get_task_logger(__name__)


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


@app.task(bind=True,max_retries=3, default_retry_delay=2)
def crawl(self, url):
    logger.info("START crawling {0}".format(url))
    try:
        r = requests.get(url)
        logger.info("FINISHED status_code: {0} content-type:{1}".format(r.status_code, r.headers['content-type']))
    except requests.exceptions.RequestException as req_exc:
        logger.error("ERROR occur for {}".format(url))
        self.retry(url, exc=req_exc)


class CrawlTask(Task):

    def __init__(self):
        self.max_retries = 3
        self.default_retry_delay = 1
        self.rate_limit = 1
        self.name = 'proj.tasks.CrawlTask'
        self.ignore_result = True

    def run(self, url):
        logger.info("START crawling {0}".format(url))
        try:
            r = requests.get(url)
            logger.info("url:{0} -> status_code: {1} content-type:{2}".format(url, r.status_code, r.headers['content-type']))
        except requests.exceptions.RequestException as req_exc:
            logger.error("ERROR occur for {}".format(url))
            self.retry(exc=req_exc)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.warn("Task: {} failed".format(self.name))

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        logger.warn("Task: {} is retrying".format(self.name))

    def on_success(self, retval, task_id, args, kwargs):
        logger.info("Task: {} has finished".format(self.name))

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        if self.max_retries == self.request.retries or status == "FAILURE":
            raise Reject(reason=einfo, requeue=False)
