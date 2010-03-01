from django.conf import settings
import time


DELAY = 1


def force_delay(method):
    
    debug = getattr(settings, 'DEBUG', False)
    
    def wrapped(*args, **kwargs):
        if debug:
            time.sleep(DELAY)
        return method(*args, **kwargs)
        
    return wrapped
        