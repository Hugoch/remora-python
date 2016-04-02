class Event:
    '''Hold all the information about an event.

    Args:
        name (str): name of the event
    '''

    def __init__(self, name):
        self.payload = {'name': name}

    def add(self, key, attr):
        self.payload[key] = attr


class Tracker:
    '''Tracks predefined events and sends them to a collector.

    Args:
        collector: an instance of a collector
        namespace (str): a namespace added to all your events
        app_id (str): an application ID added to all your events
    '''

    def __init__(self, collector, namespace, app_id):
        self.collector = collector
        self.namespace = namespace
        self.app_id = app_id

    def send(self, evt):
        '''Add namespace and app_id then send to the collector.'''
        evt.add('app_id', self.app_id)
        evt.add('namespace', self.namespace)
        self.collector.send(evt)

    def track_application_start(self):
        '''Track an application start event.'''
        evt = Event('start')
        self.send(evt)
