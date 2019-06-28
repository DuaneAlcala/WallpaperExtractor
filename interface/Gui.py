import tkinter
import threading
import queue
from PIL import Image, ImageTk

class Gui:

    def __init__(self, controller, root, message_queue):
        self._controller = controller
        self._root = root
        self._images_queue = message_queue

        self._width = 1280
        self._height = 720

        self._left_fragment_width = self._width / 4
        self._right_fragment_width = self._width - self._left_fragment_width

        self._subreddits_panel = None
        self._top_frame = None

        self._subreddits_to_panel_dict = {}

        self._images_frame = None

        self.__setup_interface()

        self.row_count = 0
        self.column_count = 0

    def __setup_interface(self):
        self._root.title("Wallpaper Scraper")
        self._root.geometry(str(self._width) + "x" + str(self._height))
        self._root.configure(background="lightblue")
        self._root.resizable(False, False)

        self.__create_subreddits_panel()
        self.__create_right_fragment()

    def __create_subreddits_panel(self):
        self._subreddits_panel = tkinter.Frame(self._root, width=self._left_fragment_width, height=self._height, background="black")
        self._subreddits_panel.place(x=0, y=0)

        self._top_frame = tkinter.Frame(self._subreddits_panel, background="#42f498", width=self._left_fragment_width, height=100)

        add_subreddit_label = tkinter.Label(self._top_frame, text="Add a Subreddit", font="Laksaman", background="#42f498")
        subreddit_text_box = tkinter.Text(self._top_frame, height=1, width=30, wrap='none', bd=0, highlightthickness=0)

        def add_subreddit_callback():
            subreddit_name = subreddit_text_box.get("1.0", 'end-1c').splitlines()
            if len(subreddit_name) != 0 and (not subreddit_name[0].isspace()):
                self.__create_left_fragment(subreddit_name[0])

        add_subreddit_button = tkinter.Button(self._top_frame, text="Add", bg="#fff", activebackground="#fff", highlightthickness=0, bd=0, command=add_subreddit_callback)

        add_subreddit_label.pack()
        subreddit_text_box.pack()
        add_subreddit_button.pack(pady=(10, 0))
        self._subreddits_panel.pack_propagate(False)
        self._top_frame.pack_propagate(False)
        self._top_frame.pack()

    def __create_left_fragment(self, subreddit_name):
        subreddit_panel = tkinter.Frame(self._subreddits_panel, width=self._left_fragment_width, height=self._height/20, background="white")
        subreddit_label = tkinter.Label(subreddit_panel, text="/r/" + subreddit_name).pack()

        subreddit_panel.pack()
        subreddit_panel.pack_propagate(False)

        self._subreddits_to_panel_dict.update({subreddit_name: subreddit_panel})
        self._controller.add_subreddit(subreddit_name)

    def __create_right_fragment(self):
        right_fragment_panel = tkinter.Frame(self._root, width=self._right_fragment_width, height=self._height, background="#121212")
        right_fragment_panel.place(x=self._left_fragment_width, y=0)

        self._images_frame = tkinter.Frame(right_fragment_panel, width=self._right_fragment_width, height=500, background="#121212")

        def start_scrape_callback():
            self._controller.start_scrape()

        settings_panel = tkinter.Frame(right_fragment_panel, width=self._right_fragment_width, height=30, background="#212121")
        download_button = tkinter.Button(settings_panel, text="Scrape", bg="#212121", activebackground="#212121", highlightthickness=0, bd=0, fg="#fff", command=start_scrape_callback)
        settings_button = tkinter.Button(settings_panel, text="Settings", bg="#212121", activebackground="#212121", highlightthickness=0, bd=0, fg="#fff")

        settings_panel.pack_propagate(False)
        settings_panel.pack()

        download_button.pack(side=tkinter.LEFT)
        settings_button.pack(side=tkinter.LEFT)
        self._images_frame.pack()
        self._images_frame.pack_propagate(False)
        right_fragment_panel.pack_propagate(False)

    def refresh_images(self):
        while self._images_queue.qsize():
            try:
                path = self._images_queue.get(0)

                # Add images to the grid
                image = Image.open(path)
                photo = image.resize((50, 50), Image.ANTIALIAS)
                something = ImageTk.PhotoImage(photo)

                label_test = tkinter.Label(self._images_frame, image=something)
                label_test.image = something
                label_test.grid(row=self.row_count, column=self.column_count, padx=5, pady=5)
                self.column_count = self.column_count + 1
                if self.column_count == 5:
                    self.column_count = 0
                    self.row_count = self.row_count + 1
            except queue.Empty:
                pass
