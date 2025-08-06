from .menu_action import *

from ..managers import console_handler

class LogOut(MenuAction):
    def select(self):
        print("\nLogging out, please wait...\n")

        console_handler.safe_exit()