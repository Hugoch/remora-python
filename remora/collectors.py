import threading
import requests
from requests.exceptions import RequestException
from queue import Queue


class AsyncCollector:
    '''Collector which uses threads to send the events asynchronously.

    Args:
        endpoint (url): URL endpoint
        method (str): 'put' or 'post'
        timeout (int): timeout for each request.
                       If timed out, event is discarded
        num_threads (int): number of threads to use for sending
    '''

    def __init__(self, endpoint, method='put', timeout=3,
                 num_threads=1):
        self.endpoint = endpoint
        self.method = method
        self.timeout = timeout
        self.queue = Queue()
        self.rlock = threading.RLock()

        # start the consuming threads
        for i in range(num_threads):
            t = threading.Thread(target=self.consume)
            t.daemon = True
            t.start()

    def send(self, evt):
        with self.rlock:
            self.queue.put(evt)

    def commit(self, evt):
        try:
            if self.method == 'put':
                requests.put(self.endpoint, json=evt.payload,
                             timeout=self.timeout)
            else:
                requests.post(self.endpoint, json=evt.payload,
                              timeout=self.timeout)

        except RequestException:
            pass  # TODO, retry.

    def consume(self):
        while True:
            evt = self.queue.get()
            self.commit(evt)
            self.queue.task_done()
