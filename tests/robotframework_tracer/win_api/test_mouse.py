from threading import Thread
import unittest
from unittest.mock import patch, MagicMock
from robotframework_tracer.win_api.mouse import Mouse

class TestMouse(unittest.TestCase):

    @patch('ctypes.WinDLL')
    def setUp(self, MockWinDLL: MagicMock):
        self.mock_user32 = MagicMock()
        MockWinDLL.return_value = self.mock_user32
        self.mouse = Mouse()

    def test_subscribe_and_unsubscribe_on_mouse_left_button_down(self):
        callback = MagicMock()
        self.mouse.subscribe_on_mouse_left_button_down(callback)
        self.assertIn(callback, self.mouse._on_mouse_left_button_down_callbacks)

        self.mouse.unsubscribe_on_mouse_left_button_down(callback)
        self.assertNotIn(callback, self.mouse._on_mouse_left_button_down_callbacks)

    def test_subscribe_and_unsubscribe_on_mouse_left_button_up(self):
        callback = MagicMock()
        self.mouse.subscribe_on_mouse_left_button_up(callback)
        self.assertIn(callback, self.mouse._on_mouse_left_button_up_callbacks)

        self.mouse.unsubscribe_on_mouse_left_button_up(callback)
        self.assertNotIn(callback, self.mouse._on_mouse_left_button_up_callbacks)


if __name__ == '__main__':
    unittest.main()
