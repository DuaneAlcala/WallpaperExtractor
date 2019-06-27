import tkinter

class Gui:

    def __init__(self, controller, root):
        self._controller = controller
        self._root = root

    def setup_interface(self):
        print("Setup")
