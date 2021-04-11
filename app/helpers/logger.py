from datetime import datetime
import logging


class LoggerHelper(object):
    def __init__(self, scope, ret=None):
        self.scope = scope
        self.ret = ret

    def __call__(self, original_function):
        def inner_func(*args, **kwargs): 
            try:
                logging.warning(f"{self.scope} - {original_function.__name__} start excuting at {datetime.utcnow().strftime('%m/%d/%Y, %H:%M:%S')}")
                return original_function(*args, **kwargs)
            except Exception as e:
                logging.error(f"{self.scope} - {original_function.__name__} fails: {str(e)} at {datetime.utcnow().strftime('%m/%d/%Y, %H:%M:%S')}")
                return self.ret

        return inner_func