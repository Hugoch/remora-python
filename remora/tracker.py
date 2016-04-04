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
        self.payload[key] = attr


class Tracker:
    '''Tracks predefined events and sends them to a collector.

    Args:
        collector: an instance of a collector
        namespace (str): a namespace added to all your events
        app_id (str): an application ID added to all your events
    '''

    def __init__(self, collector, namespace, app_id, app_version=None):
        self.collector = collector
        self.namespace = namespace
        self.app_id = app_id
        self.app_version = app_version
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
        evt.add('app_version', self.app_version)
        if self.user_id is not None:
            evt.add('user_id', self.user_id)
        self.collector.send(evt)

    def track_application_start(self, user_id=None):
        '''Track an application start event.'''
        evt = Event('start')
        self.send(evt)

    def track_page_view(self, page_name):
        '''Track a page view'''
        evt = Event('pageview')
        evt.add('page_name', page_name)
        self.send(evt)

    def track_custom_event(self, event_name, message=None):
        '''Track a custom event'''
        evt = Event(event_name, message=message)
        self.send(evt)

