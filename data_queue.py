# Shared data queue between flaskApp.py file and smsGateway.py file
from multiprocessing import Queue

# Creates a shared Queue
data_queue = Queue()