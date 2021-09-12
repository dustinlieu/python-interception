def _CTL_CODE(device_type, function, method, access):
	return (device_type << 16) | (access << 14) | (function << 2) | method

FILE_DEVICE_UNKNOWN = 0x00000022

METHOD_BUFFERED = 0

FILE_ANY_ACCESS = 0

IOCTL_SET_PRECEDENCE = _CTL_CODE(FILE_DEVICE_UNKNOWN, 0x801, METHOD_BUFFERED, FILE_ANY_ACCESS)
IOCTL_GET_PRECEDENCE = _CTL_CODE(FILE_DEVICE_UNKNOWN, 0x802, METHOD_BUFFERED, FILE_ANY_ACCESS)
IOCTL_SET_FILTER = _CTL_CODE(FILE_DEVICE_UNKNOWN, 0x804, METHOD_BUFFERED, FILE_ANY_ACCESS)
IOCTL_GET_FILTER = _CTL_CODE(FILE_DEVICE_UNKNOWN, 0x808, METHOD_BUFFERED, FILE_ANY_ACCESS)
IOCTL_SET_EVENT = _CTL_CODE(FILE_DEVICE_UNKNOWN, 0x810, METHOD_BUFFERED, FILE_ANY_ACCESS)
IOCTL_WRITE = _CTL_CODE(FILE_DEVICE_UNKNOWN, 0x820, METHOD_BUFFERED, FILE_ANY_ACCESS)
IOCTL_READ = _CTL_CODE(FILE_DEVICE_UNKNOWN, 0x840, METHOD_BUFFERED, FILE_ANY_ACCESS)
IOCTL_GET_HARDWARE_ID = _CTL_CODE(FILE_DEVICE_UNKNOWN, 0x880, METHOD_BUFFERED, FILE_ANY_ACCESS)

GENERIC_READ = 0x80000000
OPEN_EXISTING = 3
INVALID_HANDLE_VALUE = -1

WAIT_TIMEOUT = 0x00000102
WAIT_FAILED = 0xFFFFFFFF

INTERCEPTION_MAX_KEYBOARD = 10
INTERCEPTION_MAX_MOUSE = 10
INTERCEPTION_MAX_DEVICE = INTERCEPTION_MAX_KEYBOARD + INTERCEPTION_MAX_MOUSE