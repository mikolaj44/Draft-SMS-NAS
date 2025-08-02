from .menu_action import *

from ...managers.router import file_manager

class ListFiles(MenuAction):
    def select(self):
        listStr = file_manager.get_file_list()
        numFiles = listStr.count(";") - 1

        print("=================================")
        print(f"{numFiles} files saved, list:")
        print(listStr)
        print("=================================")