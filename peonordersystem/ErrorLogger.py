'''
@author: Carl McGraw
@contact: cjmcgraw.u.washington.edu
@version: 1.0
'''

from peonordersystem.path import SYSTEM_LOG_PATH
from peonordersystem.CustomExceptions import NoSuchSelectionError,\
    InvalidReservationError, InvalidOrderError, InvalidItemError

import traceback

import logging
import inspect

def generate_logger(log_type=logging.DEBUG, file_name='debug.log'):
    """Generates the logger object and stores it in the
    module wide variable logger.
    
    @keyword log_type: int value representing the log type that
    this logger will utilize. By default log_type=logging.DEBUG
    
    @keyword file_name: str representing the name of the log
    that the logger will output to.
    
    @return: logging.Logger object that represents the newly
    created logger.
    """
    fmt = '%(asctime)s | %(levelname)s: %(message)s'
    date_fmt = "%Y-%m-%d, %H:%M:%S"
    formatter = logging.Formatter(fmt=fmt, datefmt=date_fmt)
    
    new_logger = logging.getLogger('peon_logger')
    new_logger.setLevel(log_type)
    new_logger.propagate = 0
    
    directory = SYSTEM_LOG_PATH + '/' + file_name
    
    file_handler = logging.FileHandler(directory)
    file_handler.setLevel(log_type)
    file_handler.setFormatter(formatter)
    
    new_logger.addHandler(file_handler)
    
    return new_logger
    

logger = generate_logger()

def initializing_fencepost_begin():
    """Used during initializing phase to notify the
    logger that initializing has begun. Outputs a
    notification to the logger.info that initialization
    has begun.
    """
    logger.info('Beginning Initialization')

def initializing_fencepost_finish():
    """Used during initializing phase to notify the
    logger that the initializing has finished. Outputs
    a notification to the logger.info that initialization
    has completed.
    """
    logger.info('End initialization')

def log_func_data(func):
    """Wrapper function that is wrapped around
    a method.
    
    @param func: func representing the function
    to be wrapped with the interior wrapper function
    when called, and wrapped by this function.
    
    @return: func representing the interior wrapper
    class that will wrap the function.
    """

    function_info = ''
    if 'im_class' in dir(func):
        function_info += func.im_class.__module__ + '.'
        function_info += func.im_class.__name__ + '.'

    function_info += func.__name__ + ' : '

    def log_wrapper(*args, **kwargs):
        """Wrapper sub function that is used to
        wrap the method when it is called.
        
        @param *args: list of parameters that represents
        the standard arguments given to the function.
        
        @param **kwargs: list of keyword parameters that
        represents the standard keyword arguments given to
        the function.
        
        @raise Exception e: Raises exceptions when it encounters
        them from wrapped functions. Prints out to file logger
        object.
        
        @return: func stored in the function that wraps this
        one.
        """
        try:
            if logger.getEffectiveLevel() == logging.DEBUG:
                logger.debug(function_info + 'Entering ' + func.__name__)
                
            try:
                return func(*args, **kwargs)

            except (NoSuchSelectionError, InvalidItemError,
                    InvalidOrderError, InvalidReservationError) as e:
                logger.info('')
                logger.info('NON-FATAL-ERROR: ' + str(type(e)))
                logger.info(e)
                logger.info('')
                raise

            except Exception as e:
                logger.error(e)
                spaces = '   '
                logger.error('')
                logger.error('TRACEBACK')
                logger.error(traceback.format_exc())
                logger.error('')
                logger.error(spaces + 'Parameters: ')
                
                spaces *= 2
                if len(args) > 0 or len(kwargs) > 0:
                    for param_set in (args, kwargs):
                        for arg in param_set:
                            arg_type = str(type(arg))
                            arg_value = str(arg)
                            logger.error(spaces + 'type = ' + arg_type)
                            logger.error(spaces + 'value = ' + arg_value)
                            logger.error('')
                else:
                    logger.error(spaces + 'No Parameters given to function')
                
                raise
        
        finally:
            if logger.getEffectiveLevel() == logging.DEBUG:
                logger.debug(function_info + 'Exiting ' + func.__name__)
        
    for attr in "__module__", "__name__", "__doc__":
        setattr(log_wrapper, attr, getattr(func, attr))
    
    return log_wrapper

def error_logging(cls):
    """Class Decorator.
    
    Used to apply the log_func_data function to all
    methods in the class.
    
    @param cls: cls variable that represents the class
    that is to have its methods modified.
    
    @return: cls representing the class that has been
    modified.
    """
    for name, method in inspect.getmembers(cls, inspect.ismethod):
        setattr(cls, name, log_func_data(method))
        
    return cls