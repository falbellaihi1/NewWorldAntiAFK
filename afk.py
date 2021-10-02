import pydirectinput
import threading
from random import randrange

import sys, time, threading, abc
from optparse import OptionParser


def parse_options():
    parser = OptionParser()
    parser.add_option("-t", action="store", type="int", dest="threadNum", default=1,
                      help="thread count [1]")
    (options, args) = parser.parse_args()
    return options


class thread_main(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.kill_received = False

    def run(self):
        time_to_wait = input("Type in seconds every when the character should move back and forth : ")
        while not self.kill_received:
            send_keys()
            print(self.name, "is active")
            for i in range(int(time_to_wait),0,-1):
                print(f"{i} remaining for next action ", end="\r", flush=True)
                time.sleep(1)


def has_live_threads(threads):
    return True in [t.isAlive() for t in threads]


def main():
    options = parse_options()
    threads = []
    print('PRESS CTR-C TO KILL THREADS')

    for i in range(options.threadNum):
        thread = thread_main("thread#" + str(i))
        thread.start()
        threads.append(thread)

    while has_live_threads(threads):
        try:
            # synchronization timeout of threads kill
            [t.join(1) for t in threads
             if t is not None and t.isAlive()]
        except KeyboardInterrupt:
            # Ctrl-C handling and send kill to threads
            print("Sending kill to threads... \nthread is still alive as long as application did not exist please wait\n THREAD WILL CANCEL IN THE NEXT EXECUSTION")
            for t in threads:
                t.kill_received = True

    print("Exited")


def send_keys():  # randomly walk fbrl
    keys = ['w', 's', 'a', 'd']
    # randomValue = randrange
    pydirectinput.keyDown(keys[randrange(start=0, stop=4)])


def get_random():
    return randrange(start=0, stop=4)


if __name__ == "__main__":
    # execute only if run as a script
    main()
