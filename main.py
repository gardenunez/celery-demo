import proj.tasks as tasks
from faker import Factory

if __name__ == "__main__":
    fake = Factory.create()
    tasks.split.delay(0,10)

    for i in xrange(2):
        url = fake.url()
        tasks.crawl.apply_async((url,), countdown=i*2)

    for i in xrange(2):
        url = fake.url()
        task = tasks.CrawlTask()
        task.apply_async((url, ), countdown=i*2)