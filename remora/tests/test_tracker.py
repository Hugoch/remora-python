import unittest
from remora.tracker import Tracker
from remora.collectors import AsyncCollector


class TestTracker(unittest.TestCase):
    def test_send_payload(self):
        collector = AsyncCollector('http://127.0.0.1', port=8080)
        t = Tracker(collector, namespace='foo', app_id='bar')
        t.track_application_start()
