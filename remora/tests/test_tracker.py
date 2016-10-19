import unittest
from remora.tracker import Tracker
from remora.collectors import AsyncCollector
import requests_mock
import json

class TestTracker(unittest.TestCase):
    def test_send_payload(self):
        url = 'http://127.0.0.1:31311'
        with requests_mock.mock() as m:
            req = m.put(url)
            collector = AsyncCollector('http://127.0.0.1:31311')
            t = Tracker(collector, namespace='foo', app_id='bar')
            t.track_application_start()
            collector.queue.join()
            res = json.loads(req.last_request.text)
            assert res['name'] == 'start'
            assert res['app_id'] == 'bar'
            assert res['namespace'] == 'foo'

    def test_send_payload_with_custom_fields(self):
        url = 'http://127.0.0.1:31311'
        with requests_mock.mock() as m:
            req = m.put(url)
            collector = AsyncCollector('http://127.0.0.1:31311')
            t = Tracker(collector, namespace='foo', app_id='bar', cpu_count=4, user_type='internal')
            t.track_application_start()
            collector.queue.join()
            res = json.loads(req.last_request.text)
            assert res['name'] == 'start'
            assert res['app_id'] == 'bar'
            assert res['namespace'] == 'foo'
            assert res['cpu_count'] == 4
            assert res['user_type'] == 'internal'

    def test_duration_decorator(self):
        url = 'http://127.0.0.1:31311'
        with requests_mock.mock() as m:
            req = m.put(url)
            def test(arg):
                pass
            collector = AsyncCollector('http://127.0.0.1:31311')
            t = Tracker(collector, namespace='foo', app_id='bar')
            t.track_duration('a_duration')(test)(1)
            collector.queue.join()
            res = json.loads(req.last_request.text)
            assert 'duration' in res
