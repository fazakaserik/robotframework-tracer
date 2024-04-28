import ctypes
import time
import tkinter as tk
from ast import arg
from collections import deque
from ctypes import POINTER, byref, wintypes
from queue import Queue
from threading import Thread
from typing import Callable, List, Literal, Tuple, Union

from robotframework_tracer.win_api.types import MSLLHOOKSTRUCT, POINT


class MouseEvents:
    HC_ACTION = 0
    WM_LBUTTONDOWN = 513
    WM_LBUTTONUP = 514


class Mouse:
    def __init__(self):
        self._on_mouse_left_button_down_callbacks: List[
            Callable[[float, float], None]
        ] = []
        self._on_mouse_left_button_up_callbacks: List[
            Callable[[float, float], None]
        ] = []

        self._event_queue = Queue()

        self._user32 = ctypes.WinDLL("user32", use_last_error=True)
        self._LowLevelMouseProc = ctypes.WINFUNCTYPE(
            wintypes.LPARAM,
            wintypes.INT,
            wintypes.WPARAM,
            POINTER(MSLLHOOKSTRUCT),
        )
        self._hook_proc_instance = self._LowLevelMouseProc(self._py_mouse_proc)
        self._hook_id = self._user32.SetWindowsHookExA(
            14, self._hook_proc_instance, None, 0
        )
        if not self._hook_id:
            raise ctypes.WinError(ctypes.get_last_error())

        Thread(target=self._process_event_queue, daemon=True).start()
        Thread(target=self._run_message_loop, daemon=True).start()

    def _call_callbacks(self, callback_list: List[Callable], *args) -> None:
        """Calls each callback in the list with the provided keyword arguments.

        Args:
            callback_list: A list of callable objects.
            **kwargs: Keyword arguments to pass to each callback.
        """
        for callback in callback_list:
            callback(*args)

    def subscribe_on_mouse_left_button_down(
        self, callback_fn: Callable[[float, float], None]
    ) -> None:
        self._on_mouse_left_button_down_callbacks.append(callback_fn)

    def unsubscribe_on_mouse_left_button_down(
        self, callback_fn: Callable[[float, float], None]
    ) -> None:
        self._on_mouse_left_button_down_callbacks.remove(callback_fn)

    def subscribe_on_mouse_left_button_up(
        self, callback_fn: Callable[[float, float], None]
    ) -> None:
        self._on_mouse_left_button_up_callbacks.append(callback_fn)

    def unsubscribe_on_mouse_left_button_up(
        self, callback_fn: Callable[[float, float], None]
    ) -> None:
        self._on_mouse_left_button_up_callbacks.remove(callback_fn)

    def _run_message_loop(self):
        msg = wintypes.MSG()
        while self._user32.GetMessageA(byref(msg), None, 0, 0) != 0:
            self._user32.TranslateMessage(byref(msg))
            self._user32.DispatchMessageA(byref(msg))
        self._user32.UnhookWindowsHookEx(self._hook_id)

    def _py_mouse_proc(self, nCode, wParam, lParam):
        if nCode >= MouseEvents.HC_ACTION:
            self._event_queue.put((nCode, wParam, lParam))
        return self._user32.CallNextHookEx(None, nCode, wParam, lParam)

    def _process_event_queue(self):
        while True:
            nCode, wParam, lParam = self._event_queue.get()
            mouse_struct = ctypes.cast(lParam, POINTER(MSLLHOOKSTRUCT)).contents
            # TODO: solve this offset
            Y_OFFSET = -40
            x = mouse_struct.pt.x
            y = mouse_struct.pt.y + Y_OFFSET

            if wParam == MouseEvents.WM_LBUTTONDOWN:
                self._call_callbacks(
                    self._on_mouse_left_button_down_callbacks, x, y
                )
            elif wParam == MouseEvents.WM_LBUTTONUP:
                self._call_callbacks(
                    self._on_mouse_left_button_up_callbacks, x, y
                )
