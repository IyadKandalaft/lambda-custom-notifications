from __future__ import print_function

import json
import urllib
import events
import notifications

print('Loading message function...')

def send_to_sns(payload, context):
    
    event = events.Event.factory('cw_event', payload)
    notification = notifications.Notification.factory('cw_event', event)
    
    notification.send()
    
    return (event.payload)
    
if __name__=='__main__':
    send_to_sns("", "")