# celery-demo

Following the First Steps with Celery and Next Steps guides, plus some custom features.

Run the app
---
1. Install rabbitmq:`$ sudo apt-get install rabbitmq-server`
2.  Install celery:`$ pip install celery`
3. Run the worker: `$ celery -A proj worker -l info`
4. Run:`python main.py`
