import os
import sys
import time
import tty
import multiprocessing
import termios
from datetime import datetime

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
        # If the -M argument wasn't given or was given
        # in a wrong way the total of minutes will be
        # 20, and 20 * 60 = 1200..
        if not mins.isdigit(): self.__total = 1200
        else:                  self.__total = int(mins) * 60

        # 'self.__info': Information about the time.
        # idx 0: How many seconds have passed by.
        # idx 1: hours counter.
        # idx 2: minutes counter
        # idx 3: seconds counter.
        # This gotta be like this since parent and child threads
        # doesn't share same memory location, since if one value
        # changes in the parent thread, it'll not be affected on
        # child one.
        self.__info     = multiprocessing.Manager().list([0, 0, 0, 0])
        self.__prssdkey = 0
        self.__task     = task
        self.__since    = datetime.today().strftime("%H:%M:%S")

        self.__stts = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin);
        self.__countDown()

        # This variable is an exception since it's shared by both threads.
        self.__paused = multiprocessing.Event()
        self.__twork  = multiprocessing.Process(target = self.__working)
        self.__twork.start()

        while self.__twork.is_alive():
            self.__prssdkey = sys.stdin.read(1)[0]
            if self.__prssdkey == chr(27):
                self.__twork.terminate()
                print("The program was stoped since ESC key was pressed.")
                break

            if self.__prssdkey == chr(32):
                if not self.__paused.is_set():
                    print("")
                    print("** PAUSED **", end = '\r')
                    self.__paused.set()
                else:
                    self.__countDown()
                    self.__paused.clear()

        print(f"You've worked {self.__info[1]}:{self.__info[2]}:{self.__info[3]} on '{self.__task}'. Congrats!")
        print("PROGRAM ENDED.")
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.__stts)
        self.__saveInfo()

    def __countDown (self) -> None:
        for sec in range(10, -1, -1):
            print(f"Getting started :: {sec} seconds left!", end = '\r')
            time.sleep(0.01)
        os.system("clear")

    def __working (self) -> None:
        while (self.__info[0] <= self.__total):
            if self.__paused.is_set():
                continue

            if self.__info[3] == 60:
                self.__info[2] += 1
                self.__info[3] = 0

            if self.__info[2] == 60:
                self.__info[2] = 0
                self.__info[1] += 1

            print(f"{self.__info[1]}:{self.__info[2]}:{self.__info[3]} :: Working on '{self.__task}' :: STAY HARD!", end = '\r')
            self.__info[3] += 1
            self.__info[0] += 1
            time.sleep(0.01)

        print("")
        print("WELL DONE!")
        print("PRESS ANY KEY TO KILL THE STOPWATCH :).")

    def __saveInfo (self):
        filepath = os.path.join(os.path.expanduser("~") + "/.configotta")
        file = open(filepath, 'a')

        file.seek(0, 2)
        file.writelines([
            '\n' + self.__task + '\n',
            "Since " + self.__since + " until " + datetime.today().strftime("%H:%M:%S") +  " of " + datetime.today().strftime("%Y-%m-%d") + '\n',
            str(int(self.__total / 60)) + " mins.\n"
        ])
        file.close()

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
