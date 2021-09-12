import ctypes

from .internal_constants import *
from .constants import *
from .key_stroke import KeyStroke, KeyboardInputData
from .mouse_stroke import MouseStroke, MouseInputData

class Device:
	def __init__(self, index):
		self.index = index

		file_name = "\\\\.\\interception{:02d}".format(self.index).encode("UTF-8")
		self.handle = ctypes.windll.kernel32.CreateFileA(file_name, GENERIC_READ, 0, None, OPEN_EXISTING, 0, None)
		if self.handle == INVALID_HANDLE_VALUE:
			# Clean up
			return

		self.event = ctypes.windll.kernel32.CreateEventA(None, True, False, None)
		if self.event == 0:
			# Clean up
			return

		self.set_event(self.event)

	def __del__(self):
		if self.handle != INVALID_HANDLE_VALUE:
			ctypes.windll.kernel32.CloseHandle(self.handle)

		if self.event != 0:
			ctypes.windll.kernel32.CloseHandle(self.event)

	def is_keyboard(self):
		return self.index >= 1 and self.index <= INTERCEPTION_MAX_KEYBOARD

	def is_mouse(self):
		return self.index >= INTERCEPTION_MAX_KEYBOARD + 1 and self.index <= INTERCEPTION_MAX_KEYBOARD + INTERCEPTION_MAX_MOUSE

	def set_precedence(self, precedence):
		value = ctypes.c_int(precedence)
		ctypes.windll.kernel32.DeviceIoControl(self.handle, IOCTL_SET_PRECEDENCE, ctypes.byref(value), ctypes.sizeof(value), None, 0, None, None)

	def get_precedence(self):
		value = ctypes.c_int(0)
		ctypes.windll.kernel32.DeviceIoControl(self.handle, IOCTL_GET_PRECEDENCE, None, 0, ctypes.cast(ctypes.byref(value), ctypes.c_void_p), ctypes.sizeof(value), None, None)
		return value.value

	def set_filter(self, filter_value):
		value = ctypes.c_ushort(filter_value)
		ctypes.windll.kernel32.DeviceIoControl(self.handle, IOCTL_SET_FILTER, ctypes.byref(value), ctypes.sizeof(value), None, 0, None, None)

	def get_filter(self):
		value = ctypes.c_ushort(0)
		ctypes.windll.kernel32.DeviceIoControl(self.handle, IOCTL_GET_FILTER, None, 0, ctypes.byref(value), ctypes.sizeof(value), None, None)
		return value.value

	def set_event(self, event):
		zero_padded_handle = (ctypes.c_int * 2)()
		zero_padded_handle[0] = event
		ctypes.windll.kernel32.DeviceIoControl(self.handle, IOCTL_SET_EVENT, zero_padded_handle, ctypes.sizeof(zero_padded_handle), None, 0, None, None)

	def send(self, stroke):
		if self.is_keyboard():
			raw_stroke = KeyboardInputData.from_key_stroke(stroke)
		else:
			raw_stroke = MouseInputData.from_mouse_stroke(stroke)

		ctypes.windll.kernel32.DeviceIoControl(self.handle, IOCTL_WRITE, ctypes.byref(raw_stroke), ctypes.sizeof(raw_stroke), None, 0, None, None)

	def receive(self):
		if self.is_keyboard():
			raw_stroke = KeyboardInputData()
			result = ctypes.windll.kernel32.DeviceIoControl(self.handle, IOCTL_READ, None, 0, ctypes.byref(raw_stroke), ctypes.sizeof(raw_stroke), None, None)
			return KeyStroke.from_keyboard_input_data(raw_stroke)
		else:
			raw_stroke = MouseInputData()
			result = ctypes.windll.kernel32.DeviceIoControl(self.handle, IOCTL_READ, None, 0, ctypes.byref(raw_stroke), ctypes.sizeof(raw_stroke), None, None)
			return MouseStroke.from_mouse_input_data(raw_stroke)

	def get_hardware_id(self):
		out_buf = (ctypes.c_char * 256)()
		bytes_returned = ctypes.c_ulong()
		result = ctypes.windll.kernel32.DeviceIoControl(self.handle, IOCTL_GET_HARDWARE_ID, None, 0, ctypes.byref(out_buf), ctypes.sizeof(out_buf), ctypes.byref(bytes_returned), None)

		return out_buf.value
