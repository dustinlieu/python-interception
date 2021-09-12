import ctypes

class MouseStroke:
	def __init__(self, state, flags, rolling, x, y, information):
		self.state = state
		self.flags = flags
		self.rolling = rolling
		self.x = x
		self.y = y
		self.information = information

	@classmethod
	def from_mouse_input_data(cls, raw_stroke):
		return cls(raw_stroke.flags, raw_stroke.button_flags, raw_stroke.button_data, raw_stroke.last_x, raw_stroke.last_y, raw_stroke.extra_information)

class MouseInputData(ctypes.Structure):
	_fields_ = [
		("unit_id", ctypes.c_ushort),
		("flags", ctypes.c_ushort),
		("button_flags", ctypes.c_ushort),
		("button_data", ctypes.c_ushort),
		("raw_buttons", ctypes.c_ulong),
		("last_x", ctypes.c_long),
		("last_y", ctypes.c_long),
		("extra_information", ctypes.c_ulong)
	]

	@classmethod
	def from_mouse_stroke(cls, stroke):
		raw_stroke = cls()
		raw_stroke.unit_id = 0
		raw_stroke.flags = stroke.flags
		raw_stroke.button_flags = stroke.state
		raw_stroke.button_data = stroke.rolling
		raw_stroke.raw_buttons = 0
		raw_stroke.last_x = stroke.x
		raw_stroke.last_y = stroke.y
		raw_stroke.extra_information = stroke.information

		return raw_stroke
