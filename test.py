def main():
    file = open('txt', 'r')
    conts = file.readlines()

    for idx in range(len(conts)):
        if conts[idx].split(',')[0] == "hola":
            conts[idx] = "hola, " + "newinfo________________\n"

    file.close()

    file = open('txt', 'w')
    file.writelines(conts)
    file.close()

if __name__ == '__main__':
    main()
