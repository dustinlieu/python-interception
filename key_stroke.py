import ctypes

class KeyStroke:
	def __init__(self, code, state, information):
		self.code = code
		self.state = state
		self.information = information

	@classmethod
	def from_keyboard_input_data(cls, raw_stroke):
		return cls(raw_stroke.make_code, raw_stroke.flags, raw_stroke.extra_information)

class KeyboardInputData(ctypes.Structure):
	_fields_ = [
		("unit_id", ctypes.c_ushort),
		("make_code", ctypes.c_ushort),
		("flags", ctypes.c_ushort),
		("reserved", ctypes.c_ushort),
		("extra_information", ctypes.c_ulong)
	]

	@classmethod
	def from_key_stroke(cls, stroke):
		raw_stroke = cls()
		raw_stroke.unit_id = 0
		raw_stroke.make_code = stroke.code
		raw_stroke.flags = stroke.state
		raw_stroke.reserved = 0
		raw_stroke.extra_information = stroke.information

		return raw_stroke
