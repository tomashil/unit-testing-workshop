import logging
import os
import sys

from service_wrappers.dynamo_service import DynamoService
from workshop_exceptions.exceptions import WorkshopError, EmptyEventValue, EventValidationError, MissingEventKeyError

logger = logging.getLogger()
logger.setLevel(logging.getLevelName(os.environ['LOGGING_LEVEL']))

dynamo_service = DynamoService(
    os.environ['VOTES_TABLE_NAME'],
    os.environ['VOTES_TABLE_PARTITION_KEY']
)

def handler(event, context):
    """Lambda entry point.  Retrieves count of vote type provided in event.

    Args:
        event: invoking service information
        context: runtime information

    Returns:
        Number of votes for a given vote type.
    """
    try:
        return get_count(event)
    except WorkshopError as e:
        logger.error(e.message)
        sys.exit()

def get_count(event):
    """Performs Lambda logic.  Determines count of vote type provided in event.

    Args:
        event: invoking service information

    Returns:
        dict representing JSON-response structure
    """
    parse_event(event)
    vote_type = event['Details']['Parameters']['VoteType'].upper()

    if vote_type == 'ALL':
        total = 0
        items = dynamo_service.scan()

        for item in items:
            total += int(item['Count'])
            
        return {
            'Id': 'ALL',
            'Count': total
        }
    else:
        return dynamo_service.query(vote_type)

def parse_event(event):
    """Parse event for required parameters.
    
    Args:
        event: Lambda event to parse
        
    Raises:
        EmptyEventValue: if required event value is empty
        EventValidationError: if parameter does not satisfy constraints
        MissingEventKeyError: if required parameter key is missing
    """
    try:
        vote_type = event['Details']['Parameters']['VoteType']
    except KeyError:
        raise MissingEventKeyError('VoteType')

    if vote_type == '' or vote_type is None:
        raise EmptyEventValue('VoteType')

    vote_type = vote_type.upper()
    enum_value_set = os.environ['VALID_VOTE_TYPES'].split(',')

    if not vote_type in enum_value_set:
        raise EventValidationError(
            'VoteType',
            vote_type,
            f'Member must satisfy enum value set: {enum_value_set}'
        )
