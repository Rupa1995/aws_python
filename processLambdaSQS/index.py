import logging
import json

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

def handler(event, context):
    LOGGER.info('Received Event: %s', event)
    for rec in event['Records']:
        content = rec['body']
        LOGGER.info('Record: %s', content)
    return {
        'statuscode': 200,
        'body': json.dumps(content)
    }