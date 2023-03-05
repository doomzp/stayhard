package main

import (
    "fmt"
    "os"
)

func checkFile () {
    homepath, _ := os.UserHomeDir();
    var pathfile string = homepath + "/.configotta";
    _, E := os.Stat(pathfile);

    if E != nil {
        var username string;
        fmt.Print("Welcome, your name is: ");
        fmt.Scanln(&username);

        fmt.Println("Ok, " + username + ", the program will create a file called '.configotta' at '~/'.");
        fmt.Println("Please do not remove it since all information's gonna be save there ;).");

        file, _ := os.Create(pathfile);

        defer file.Close();
        fmt.Println("Operation done, run the program again. STAY HARD!");
        os.Exit(0);
    }
}

func main () {
    checkFile();
    if len(os.Args) == 1 {
        fmt.Println("U: This programs needs arguments to be able to work!");
        fmt.Println("    * -T <task>: Task which you'll be working on.");
        fmt.Println("    * -m <mins>: How many minutes you'll study (20 by default).")
        fmt.Println("    * -s: See the activities sumary.");
        os.Exit(0);
    }
}
