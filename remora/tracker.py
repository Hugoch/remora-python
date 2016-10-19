import time
from six import iteritems
from functools import wraps

class Event:
    '''Hold all the information about an event.

    Args:
        name (str): name of the event
        message (str): an optional message to attach to the event
    '''

    def __init__(self, name, user_id=None, message=None):
        self.payload = {'name': name}
        if message is not None:
            self.add('message', message)

    def add(self, key, attr):
        if key in self.payload:
            raise AttributeError("Field {0} already exists in the event. You cannot overwrite it!")
        self.payload[key] = attr


class Tracker:
    '''Tracks predefined events and sends them to a collector.

    Args:
        collector: an instance of a collector
        namespace (str): a namespace added to all your events
        app_id (str): an application ID added to all your events
        kwargs (str): add any additional fields you like in kwargs. Those will be added in each event.
    '''

    def __init__(self, collector, namespace, app_id, **kwargs):
        self.collector = collector
        self.namespace = namespace
        self.app_id = app_id
        self.additional_fields = kwargs
        self.user_id = None

    def set_user_id(self, id):
        '''Set the tracker to use a user id'''
        self.user_id = id

    def unset_user_id(self):
        '''Unset the user ID'''
        self.user_id = None

    def send(self, evt):
        '''Add namespace and app_id then send to the collector.'''
        evt.add('app_id', self.app_id)
        evt.add('namespace', self.namespace)
        # add any field that was given when instantiating the tracker. Warning, fields must be accepted by the server.
        for (key, value) in iteritems(self.additional_fields):
            evt.add(key, value)
        if self.user_id is not None:
            evt.add('user_id', self.user_id)
        self.collector.send(evt)

    def track_application_start(self):
        '''Track an application start event.'''
        evt = Event('start')
        self.send(evt)

    def track_page_view(self, page_name):
        '''Track a page view'''
        evt = Event('pageview')
        evt.add('page_name', page_name)
        self.send(evt)

    def track_custom_event(self, event_name, message=None, **kwargs):
        '''Track a custom event with optional fields'''
        evt = Event(event_name, message=message)
        # add optional kwargs fields. Warning, fields must be accepted by the server.
        for (key, value) in iteritems(kwargs):
            evt.add(key, value)
        self.send(evt)

    def track_duration(self, event_name):
        '''Decorator to track the execution time of a function.

        Use example:
        def test(arg):
            pass
        t = Tracker(collector, namespace='foo', app_id='bar')
        t.track_duration('a_duration')(test)(1)
        '''
        def do_track(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                res = func(*args, **kwargs)
                end_time = time.time()
                self.track_custom_event(event_name, message="", duration=end_time - start_time)
                return res
            return wrapper
        return do_track