import proj.tasks as tasks
from faker import Factory

if __name__ == "__main__":
    tasks.split.delay(0,10)

    fake = Factory.create()
    for i in xrange(5):
        url = fake.url()
        tasks.crawl.apply_async((url,), countdown=i*2)