from functools import wraps
import sys
from asyncio import Queue, coroutine, iscoroutine, async
import logging

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
			event, args = yield from self.__events.get()
			for fn, expects in self.__registration[event[0]]:
				fire = True
				if len(event) - 1 != len(expects):
					continue
				for i in range(len(event)-1):
					ev = event[i+1].lower()
					ex = expects[i]
					if isinstance(ex, list):
						if not any(ev == val.lower() for val in ex):
							fire = False
							break
					else:
						if ev.lower() != ex.lower():
							fire = False
							break
				if fire:
					fn(event=event, **args)

	def registerFunction(self, event, func):
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
	def fireEvent(self, *event, **kwargs):
		if event[0] in self.__registration:
			yield from self.__events.put([event, kwargs])

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

def fireEvent(*event, **kwargs):
	logger.debug("Firing event {} with {}".format(event, kwargs))
	async(EventManager.fireEvent(*event, **kwargs))
