import os
import sys
import time
import multiprocessing
import tty
import termios
import signal

def checkFile () -> None:
    tofile = os.path.join(os.path.expanduser("~") + "/.configotta")
    if os.path.isfile(tofile):
        return

    print("The program will create a file called '.configotta' at '~/'.")
    print("Do not remove since all your progress information will be losed.")
    with open(tofile, "w") as file:
        file.close()
    print(tofile + ": Was created!")

def usage () -> None:
    print("U: This program needs arguments to be able to work!")
    print("    * -T <task>: Task you'll be working on.")
    print("    * -M <mins>: How many mintues you'll be working on.")
    print("    * -s: Activities summary.")
    exit(0)

class Work:
    def __init__ (self, task: str, mins: str):
        if not mins.isdigit(): self.__mins = 20
        else: self.__mins = int(mins)
        self.__task = task
        self.__seconds = 0
        self.__secs    = 0
        self.__mins    = 0
        self.__hous    = 0
        self.__countDown()

    def __countDown (self) -> None:
        for sec in range(10, -1, -1):
            print(f"Getting started :: {sec} seconds left!", end = '\r')
            time.sleep(1)
        os.system("clear")

    def __working (self) -> None:
        while self.__seconds <= self.__mins * 60:
            if self.__secs == 60:
                self.__mins += 1
                self.__secs = 0
            if mins == 60:
                self.__mins = 0
                self.__hours += 1

            print(f"{self.__hous}:{self.__mins}:{self.__secs} \t Working on '{self.__task}' : STAY HARD!", end = '\r')
            self.__secs += 1
            self.__seconds += 1
            time.sleep(1)


def main () -> None:
    checkFile()
    if len(sys.argv) == 1:
        usage()

    args = ["-/-", "-/-", False]
    for idx in range(len(sys.argv)):
        if sys.argv[idx] == "-s":
            args[2] = True
            break

        if (idx + 1) < len(sys.argv):
            if sys.argv[idx] == "-T": args[0] = sys.argv[idx + 1]; idx += 1
            if sys.argv[idx] == "-M": args[1] = sys.argv[idx + 1]; idx += 1

    if args[-1]: pass
    Work(args[0], args[1])

if __name__ == '__main__':
    main()
