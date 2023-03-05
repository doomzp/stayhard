import os
import sys
import time
import tty

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

def summary () -> None:
    pass

def countDown () -> None:
    for s in range(1, -1, -1):
        print(f"You'll start in {s}", end="\r")
        time.sleep(1)
    os.system("clear")

def work (task: str, mins: str) -> None:
    if not mins.isdigit():
        mins = "20"
    countDown()

    second = 0
    Sec, Min, Hour = 0, 0, 0
    while second <= int(mins) * 60:
        if Sec == 60:
            Min += 1
            Sec = 0
        if Min == 60:
            Hour += 1
            Min = 0

        time.sleep(1)
        print(f"{Hour}:{Min}:{Sec} Working on '{task}'. STAY HARD!", end="\n")
        Sec += 1
        second += 1

def main () -> None:
    checkFile()
    if len(sys.argv) == 1:
        pass

    args = ["unknown", "-/-", False]
    for idx in range(len(sys.argv)):
        if sys.argv[idx] == "-s":
            args[2] = True
            break

        if (idx + 1) < len(sys.argv):
            if sys.argv[idx] == "-T": args[0] = sys.argv[idx + 1]; idx += 1
            if sys.argv[idx] == "-M": args[1] = sys.argv[idx + 1]; idx += 1

    if args[-1]: summary()
    work(args[0], args[1])

if __name__ == '__main__':
    main()
