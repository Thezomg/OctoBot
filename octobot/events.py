from functools import wraps
import sys
from asyncio import Queue, coroutine, iscoroutine, async, Future, gather
import logging
import inspect

logger = logging.getLogger('octobot:EventManager')

class RegistrationException: pass

class _EventManager(object):

    def __init__(self):
        providers = {}
        self.__registration = {}
        self.__module_functions = {}
        self.__events = Queue()

    @coroutine
    def handleEvents(self):
        while True:
            event, args, future = yield from self.__events.get()
            logger.debug("Handling event {}".format(event))
            for fn, expects in self.__registration[event[0]]:
                fire = True
                if len(event) - 1 != len(expects):
                    continue
                for i in range(len(event)-1):
                    ev = event[i+1].lower()
                    ex = expects[i]
                    if isinstance(ex, list):
                        if not any(ev == val.lower() for val in ex):
                            logger.error("Won't fire")
                            fire = False
                            break
                    else:
                        if ev.lower() != ex.lower():
                            fire = False
                            break
                if fire:
                    logger.debug("Firing event function: {} with {}".format(fn.__name__, args))
                    ret = fn(event=event, **args)
                    future.set_result(ret)

    @coroutine
    def handle_event(self, event, args):
        logger.debug('Handling event {}'.format(event))
        to_call = []
        results = []
        for fn, expects in self.__registration[event[0]]:
            fire = True
            if len(event) -1 != len(expects):
                continue
            for i in range(len(event)-1):
                ev = event[i+1].lower()
                ex = expects[i]
                if isinstance(ex, list):
                    if not any(ev == val.lower() for val in ex):
                        logger.error("Won't fire")
                        fire = False
                        break
                else:
                    if ev.lower() != ex.lower():
                        fire = False
                        break
            if fire:
                to_call.append(fn(event=event, **args))

        if len(to_call) > 0:
            results = yield from gather(*to_call)

        return results

    def register_class(self, cls):
        methods = inspect.getmembers(cls, predicate=inspect.ismethod)
        for _, f in methods:
            fn = f
            event = getattr(fn, '__event__', None)
            if event is not None:
                logger.debug('Registering {} for {}'.format(fn.__name__, event))
                self.register_function(event, fn)

    def register_function(self, event, func):
        primary = event[0]
        expects = []
        if len(event) > 1:
            expects = event[1:]
        if not primary in self.__registration:
            self.__registration[primary] = []
        self.__registration[primary].append([func, expects])

        mod = sys.modules[func.__module__]
        if not mod in self.__module_functions:
            self.__module_functions[mod] = []

        self.__module_functions[mod].append(func)

    @coroutine
    def fire_event(self, *event, **kwargs):
        results = yield from self.handle_event(event, kwargs)

        return results

    def unregisterModuleFunctions(self, mod):
        if not mod in self.__module_functions:
            return True

        for r in __registration:
            self.__registration[r][:] = [i for i,_ in self.__registration[r] if i not in self.__module_functions[mod]]

        del self.__module_functions[mod]

EventManager = _EventManager()

def BindEvent(*event):
    def decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        if len(event) > 0:
            EventManager.registerFunction(event, func)
        return func_wrapper
    return decorator

def bind_event(*event):
    def decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            fn = func
            if not iscoroutine(fn):
                fn = coroutine(fn)

            return fn(*args, **kwargs)

        if len(event) > 0:
            func_wrapper.__event__ = event

        return func_wrapper
    return decorator

@coroutine
def fire_event(*event, **kwargs):
    logger.debug("Firing event {} with {}".format(event, kwargs))
    f = yield from EventManager.fire_event(*event, **kwargs)
    return f
