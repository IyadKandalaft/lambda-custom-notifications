from __future__ import print_function

import json
import urllib
import boto3
import event_parser

print('Loading message function...')


def send_to_sns(event, context):
    sns = boto3.client('sns')
    
    response = sns.publish(
        TopicArn="arn:aws:sns:ca-central-1:363003170430:CloudWatchAlarmChangeNotification",
        Subject="Cloud Watch Alarm",
        Message="This is a sample message"
    )
    
    return (response)
