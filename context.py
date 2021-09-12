import ctypes

from .device import Device
from .internal_constants import *
from .constants import *

class Context:
	def __init__(self):
		self._devices = [Device(i) for i in range(INTERCEPTION_MAX_DEVICE)]

	def set_filter(self, predicate, filter):
		for i in range(INTERCEPTION_MAX_DEVICE):
			if (predicate == IS_KEYBOARD and self._devices[i].is_keyboard()) or (predicate == IS_MOUSE and self._devices[i].is_mouse()):
				self._devices[i].set_filter(filter)

	def wait(self, timeout=-1):
		wait_handles = (ctypes.c_void_p * INTERCEPTION_MAX_DEVICE)()
		for i in range(INTERCEPTION_MAX_DEVICE):
			wait_handles[i] = self._devices[i].event

		result = ctypes.windll.kernel32.WaitForMultipleObjects(INTERCEPTION_MAX_DEVICE, wait_handles, False, timeout)
		if result == WAIT_FAILED or result == WAIT_TIMEOUT:
			return None

		return self._devices[result]
