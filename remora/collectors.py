import threading
from requests import put, post
from requests.exceptions import RequestException
from queue import Queue


class AsyncCollector:
    '''Collector which uses threads to send the events asynchronously.

    Args:
        endpoint (url): URL endpoint
        port (int): port to use for request
        method (str): 'put' or 'post'
        timeout (int): timeout for each request.
                       If timed out, event is discarded
        num_threads (int): number of threads to use for sending
    '''

    def __init__(self, endpoint, port=8080, method='put', timeout=3,
                 num_threads=1):
        self.endpoint = endpoint
        self.port = port
        self.method = method
        self.timeout = timeout
        self.queue = Queue()

        # start the consuming threads
        for i in range(num_threads):
            t = threading.Thread(target=self.consume)
            t.daemon = True
            t.start()

    def send(self, evt):
        self.queue.put(evt)

    def commit(self, evt):
        try:
            endpoint = '{0}:{1}'.format(self.endpoint, self.port)
            if self.method == 'put':
                put(endpoint, json=evt.payload, timeout=self.timeout)
            else:
                post(endpoint, json=evt.payload, timeout=self.timeout)

        except RequestException:
            pass  # TODO, retry.

    def consume(self):
        while True:
            evt = self.queue.get()
            self.commit(evt)
            self.queue.task_done()
