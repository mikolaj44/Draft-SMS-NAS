from .menu_action import *
from ...utils.colors import *

import magic
from tkinter import Tk
from tkinter.filedialog import askopenfilename

from ...managers.router import file_manager

class StoreFile(MenuAction):
    def select(self):
        Tk().withdraw()
        
        file_path = askopenfilename()
        
        name = ""

        while True:
            print("\nPlease provide a file name, max 4 characters and only letters and numbers: ", end="")

            name = input()

            if(not file_manager.file_name_is_valid(name)):
                print(RED + "\nTry again." + RESET)
            elif(file_manager.store_file(name=name, file_path=file_path)):
                return