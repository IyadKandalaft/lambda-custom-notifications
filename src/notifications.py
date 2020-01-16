import logging
from jinja2 import Environment, FileSystemLoader, select_autoescape
import boto3

logger = logging.getLogger(__name__)

class Notification():
    jinja_template_file = 'generic.j2'

    @staticmethod
    def factory(event, notification_type):
        notification_type = type.lower()
        if notification_type == "cw_ok":
            return OKNotification(event)
        if notification_type == "cw_alarm":
            return AlarmNotification(event)
        if notification_type == "cw_event":
            return EventNotification(event)
        
        return Notification(event)
    
    def __init__(self, event):
        self.event = event
        self.template = self.load_template()
    
    def load_template(self):
        logger.debug('Loading template {}'.format(self.jinja_template_file))
        
        env = Environment(
            loader=FileSystemLoader('./notification_templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )
    
    def get_message(self):
        return self.template.render()
    
    def send(self):
        sns = boto3.client('sns')
    
        response = sns.publish(
            TopicArn="arn:aws:sns:ca-central-1:363003170430:CloudWatchAlarmChangeNotification",
            Subject="Cloud Watch Alarm",
            Message="This is a sample message"
        )
        

class OKNotification(Notification):
    '''
    Sends notification for Cloud Watch when state change is Okay
    '''
    jinja_template_file = 'cw_ok_template.j2'
    def __init__(self, event):
        self.type = 'Cloud Watch Alarm Recovery'
        super().__init__(event)


class AlarmNotification(Notification):
    '''
    Sends notification for Cloud Watch when state change is Alarm
    '''
    jinja_template_file = 'cw_alarm_template.j2'
    def __init__(self, event):
        self.type = 'Cloud Watch Alarm Warning'
        super().__init__(event)
    
class EventNotification(Notification):
    '''
    Sends notification for generic Cloud Watch events that don't involve a state
    change such as scheduled events.
    '''
    jinja_template_file = 'cw_event_template.j2'
    def __init__(self, event):
        self.type = 'Cloud Watch Event'
        super().__init__(event)