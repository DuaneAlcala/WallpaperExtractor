from controller import Controller


def main():
    controller = Controller()
    txt = input("Type something to test this out: ")
    controller.add_subreddit(txt)
    controller.test()


if __name__ == '__main__':
    main()
