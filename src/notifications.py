import logging
import enum
import Jinja2

logger = logging.getLogger(__name__)

class Notification():
    def factory(type, event):
        if type == "OK":
            return OKNotification(event)
        if type == "Alarm":
            return AlarmNotification(event)
        if type == "Event":
            return EventNotification(event)
    
    factory = staticmethod(factory)

class OKNotification(Notification):
    '''
    Sends notification for Cloud Watch when state change is  recovery
    '''
    template = 'cw_ok_template.j2'
    def __init__()
        return
    
    

class AlarmNotification(Notification):
    '''
    Sends notification for Cloud Watch Alarm
    '''
    template - 'cw_alarm_template.j2'
    def __init__():
        return
    
class EventNotification(Notification):
    '''
    Sends notification for generic Cloud Watch events that don't involve a state
    change such as scheduled events.
    '''
    template = 'cw_event_template.j2'
    def __init__():
        return