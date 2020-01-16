import json
import logging
import enum

logger = logging.getLogger(__name__)

class ObfuscationPattern(enum.Enum):
    BEGINING = 1 #
    END = 2
    MIDDLE = 3
    ALL = 4


class Event():
    '''
    Parses an event JSON and provides convenience methods to access and
    ofuscate the data
    '''

    expected_attr = ['account', 'region', 'time', 'id']
    
    @staticmethod
    def factory(type, payload):
        type = type.lower()
        
        if type == "cw_event":
            return CloudWatchEvent(payload)
        if type == "cw_alarm":
            return CloudWatchAlarm(payload)

    def __init__(self, payload):
        '''
        Initialize an event object
    
        Raises a JSONDecodeError if the JSON is malformed and cannot be decoded.
        '''

        self.payload = self._parse_payload(payload)
        
    
    def _parse_payload(self, payload):
        '''
        Parses the payload json into an object and logs any anomalies
        '''
        parsed_payload = json.loads(payload)
        logger.debug('Parsed event payload successfully')
        
        for attribute in self.expected_attr:
            if not hasattr(payload, attribute):
                logger.warning(f'Event is missing {attribute}')

        return parsed_payload
        
    def get_obfuscated_attr(self, attribute, num_clear_chars=2, \
                            pattern=ObfuscationPattern.MIDDLE, \
                            hidden_char='*'):
        '''
        Returns an obfuscated string of the event attribute requested leaving 
        a number of unobfuscated characters.

        If pattern is ObfuscationPattern.BEGINING
        "account": "123456789012" becomes "account": "**********12"

        If pattern is ObfuscationPattern.END
        "account": "123456789012" becomes "account": "12**********"

        If pattern is ObfuscationPattern.MIDDLE
        "account": "123456789012" becomes "account": "12********12"

        If pattern is ObfuscationPattern.ALL
        "account": "123456789012" becomes "account": "************"

        :param attribute: Name of attribute to obfuscate
        :param num_clear_chars: Number of characters to leave unobfuscated
        :param pattern: Determine whether the begining, end, middle, or all characters are obfuscated
        :type ObfuscationPattern:
        '''
        attr_val = getattr(self.payload, attribute)
        attr_val_len = len(attr_val)
        
        char_num = 0
        obfuscated_val =''
        for char in attr_val:
            char_num += 1
            if pattern == ObfuscationPattern.ALL:
                obfuscated_val += hidden_char
            elif pattern == ObfuscationPattern.BEGINING and \
                 char_num < attr_val_len - num_clear_chars:
                obfuscated_val += hidden_char
            elif pattern == ObfuscationPattern.END and \
                 char_num > num_clear_chars:
                obfuscated_val += hidden_char
            elif pattern == ObfuscationPattern.MIDDLE and \
                 char_num > num_clear_chars and \
                 char_num < attr_val_len - num_clear_chars:
                obfuscated_val += hidden_char
            else:
                obfuscated_val = char

        return obfuscated_val
        
    def get_attr(self, attribute):
        '''
        Retrieve an attribute from the event

        :returns: A string or list of the attribute requested
        '''
        return getattr(self.payload, attribute)


class CloudWatchEvent(Event):
    '''
    Parses a Cloud Watch event payload and provides convenience methods
    '''
    
    expected_attr = ['account', 'region', 'time', 'id', 'resources']

    def __init__(self, payload):
        '''
        Initialize an CloudWatchEvent object
    
        Raises a JSONDecodeError if the JSON is malformed and cannot be decoded.
        '''
        super().__init__(payload)

class CloudWatchAlarm(Event):
    '''
    Parses a Cloud Watch alarm payload and provides convenience methods
    '''
    
    expected_attr = ['account', 'region', 'time', 'id', 'resources']

    def __init__(self, payload):
        '''
        Initialize an CloudWatchAlarm object
    
        Raises a JSONDecodeError if the JSON is malformed and cannot be decoded.
        '''
        super().__init__(payload)