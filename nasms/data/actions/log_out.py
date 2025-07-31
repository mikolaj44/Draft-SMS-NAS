from .menu_action import *

from ...managers.router import router_manager

class LogOut(MenuAction):
    def select(self):
        print("\nLogging out, please wait...\n")

        router_manager.log_out()

        print("Logged out successfully.\n")
