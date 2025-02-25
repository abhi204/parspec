import os

'''
Run this script using command: gunicorn --config gunicorn_config.py app:app
'''

MAX_CONCURRENT_REQUESTS = 40
WORKER_COUNT = os.cpu_count() * 2 # spawn 2x as many workers as there are cores
THREAD_COUNT = 40 / WORKER_COUNT # allow supporting MAX_CONCURRENT_REQUESTS connections per second by allowing workers to use threads for io-bound tasks

workers = int(os.environ.get('GUNICORN_PROCESSES', WORKER_COUNT))
threads = int(os.environ.get('GUNICORN_THREADS', THREAD_COUNT))

bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:8080')

forwarded_allow_ips = '*'