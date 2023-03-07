import multiprocessing

class X:
    def __init__ (self):
        self.__values = multiprocessing.Manager().list([0, 0, 0])
        self.__procss = multiprocessing.Process(target = self.__do)
        self.__procss.start()

        while True:
            inp = input(":")
            if inp == 's':
                break
        print(self.__values)

    def __do (self):
        self.__values[0] = 1
        self.__values[1] = 2
        self.__values[2] = 3


X()
