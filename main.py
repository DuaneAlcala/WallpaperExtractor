from scraper.Controller import Controller
import tkinter


def main():
    root = tkinter.Tk()
    controller = Controller(root)
    #txt = input("Type something to test this out: ")
    #controller.add_subreddit(txt)
    #controller.test()
    root.mainloop()


if __name__ == '__main__':
    main()
