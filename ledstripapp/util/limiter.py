import time


def limit_rate(delay=1.0):
    """
    produces a decorator that will call a function only once per `delay` 
    see https://stackoverflow.com/questions/3232748/i-want-to-limit-how-often-a-tkinter-callback-is-run
    """
    def wrapper(func):  # the actual decorator
        cache = dict(next=0)  # cache the result and time

        def limited(*args, **kwargs):
            if time.time() > cache['next']:  # is it time to call again
                cache['result'] = func(*args, **kwargs)  # do the function
                # dont call before this time
                cache['next'] = time.time() + delay
            return cache['result']
        return limited
    return wrapper
