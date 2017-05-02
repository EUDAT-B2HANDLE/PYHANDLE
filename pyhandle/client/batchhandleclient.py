import logging

from .. import util

logging.basicConfig(level=logging.INFO)


LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(util.NullHandler())
REQUESTLOGGER = logging.getLogger('log_all_requests_of_testcases_to_file')
REQUESTLOGGER.propagate = False

class BatchHandleClient(object):
    """The BatchHandleClient class"""
    
    def __init__(self, **args):
        util.log_instantiation(LOGGER, 'BatchHandleClient', args, ['password', 'reverselookup_password'], with_date=True)

        LOGGER.debug('\n' + 60 * '*' + '\nInstantiation of BatchHandleClient\n' + 60 * '*')
           
    def create_batch_file(self):
    	LOGGER.debug('BatchHandleClient')
    
    def create_handle_record(self):
        LOGGER.debug("Creating a handle (batch)")

    def delete_handle(self):
        LOGGER.debug("Deleting a handle (batch)")
    
    def modify_handle(self):
        LOGGER.debug("Modifying a value of handle (batch)")