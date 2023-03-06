# A thread (or at least so far [guided by what we know])
# won't modify the variable for the whole program, so
# if one thread do "x += 1", 'x' is gonna be modfy
# just for that thread, not for the other ones.
# TASK: Learn too much about, we love this SHIT!!!!!!!!!!!!!
import os
import sys
import time
import tty
import termios
import subprocess
import multiprocessing

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
        if not mins.isdigit(): self.__total = 1200
        else: self.__total = int(mins) * 60

        self.__task = task
        self.__passedby = 0
        self.__secs     = 0
        self.__mins     = 0
        self.__hours    = 0
        self.__prssdkey = 0

        # Just settings...
        stts = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin)

        workingT = multiprocessing.Process(target = self.__working)
        workingT.start()

        workstoped = False
        while True:
            if not workingT.is_alive():
                break

            self.__prssdkey = sys.stdin.read(1)[0]
            if self.__prssdkey == chr(27):
                workingT.terminate()
                print("The program was stoped since ESC key was pressed.")
                print(f"You did {self.__hours}:{self.__mins}:{self.__secs}!")
                break

        print("PROGRAM ENDED.")

    def __countDown (self) -> None:
        for sec in range(2, -1, -1):
            print(f"Getting started :: {sec} seconds left!", end = '\r')
            time.sleep(1)
        os.system("clear")

    def __working (self) -> None:
        while (self.__passedby <= self.__total):
            if self.__secs == 60:
                self.__mins += 1
                self.__secs = 0

            if self.__mins == 60:
                self.__mins = 0
                self.__hours += 1

            print(f"{self.__hours}:{self.__mins}:{self.__secs} :: Working on '{self.__task}' :: STAY HARD!", end = '\r')
            self.__secs += 1
            self.__passedby += 1
            time.sleep(000.1)

        print("")
        print("WELL DONE!")
        print("PRESS ANY KEY TO SAVE THE PROGRESS INFORMATION.")

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
