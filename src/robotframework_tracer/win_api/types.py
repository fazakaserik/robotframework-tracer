from ctypes import POINTER, Structure, byref, c_long, c_ulong, wintypes


class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]


class MSLLHOOKSTRUCT(Structure):
    _fields_ = [
        ("pt", POINT),
        ("mouseData", wintypes.DWORD),
        ("flags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", POINTER(c_ulong)),
    ]
