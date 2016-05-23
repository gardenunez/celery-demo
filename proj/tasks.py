from __future__ import absolute_import
from proj.celery import app

@app.task
def add(x, y):
    return x + y

@app.task
def split(a, b):
    print "from {0} to {1}".format(a,b)
    if a > b:
        split(b, a)
    if b - a <= 2:
        print "finish -> a:{0}, b:{1}".format(a, b)
        return a, b
    mid = (a + b)/2
    split(a, mid)
    split(mid, b)
