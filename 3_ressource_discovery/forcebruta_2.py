import requests
from threading import Thread
import sys
import time
import getopt
from termcolor import colored
import re 
class RequestPerformer(Thread):
    def __init__(self, word, url, hidecode):
        Thread.__init__(self)
        try:
            self.word = word.strip()
            self.url = url.replace("FUZZ", self.word)
            self.hidecode = hidecode
        except Exception as e:
            print(e)

    def run(self):
        try:
            r = requests.get(self.url)
            lines = str(r.text.count("\n"))  
            chars = str(len(r.text))
            words = str(len(re.findall(r"\s+", r.text)))
            code = str(r.status_code)

            if self.hidecode != code:
                if '200' <= code < '300':
                    print(colored(code, 'green') + "   \t\t" + chars + " \t\t" + words + " \t\t " + lines + "\t" + self.url + "\t\t  ")
                elif '400' <= code < '500':
                    print(colored(code, 'red') + "   \t\t" + chars + " \t\t" + words + " \t\t " + lines + "\t" + self.url + "\t\t  ")
                elif '300' <= code < '400':
                    print(colored(code, "yellow") + " \t\t" + chars + " \t\t" + words + " \t\t " + lines + "\t" + self.url + "\t\t ")

            i[0] -= 1
        except Exception as e:
            print(e)

def banner():
    print("    Starting the brute force    ")

def usage():
    print("Usage: script.py -w <url> -f <wordlist_file> -t <threads> -c <hidecode>")

def start(argv):
    banner()
    if len(sys.argv) < 5:
        usage()
        sys.exit()
    try:
        opts, args = getopt.getopt(argv, "w:f:t:c:")
    except getopt.GetoptError:
        print("Error in argument")
        sys.exit()
    hidecode = "000"
    for opt, arg in opts:
        if opt == "-w":
            url = arg
        elif opt == "-f":
            dict_file = arg
        elif opt == "-t":
            threads = int(arg)  # Convert threads to integer here
        elif opt == "-c":
            hidecode = arg
    try:
        with open(dict_file, "r") as f:
            words = f.readlines()
    except Exception as e:
        print(f"Failed opening file: {dict_file}\n", e)
        sys.exit()
    launcher_thread(words, threads, url, hidecode)

def launcher_thread(names, th, url, hidecode):
    global i
    i = []
    i.append(0)
    print("________________________________________________________________________________________________")
    print("Code" + "\t\tchars\t\twords\t\tlines\t\tURL")
    print("_________________________________________________________________________________________________")
    threads = []
    while len(names):
        try:
            if i[0] < th:
                n = names.pop(0)
                i[0] += 1
                thread = RequestPerformer(n, url, hidecode)
                thread.start()
                threads.append(thread)
        except KeyboardInterrupt:
            print("ForceBruta 2 interrupted by user. Finishing attack...")
            sys.exit()

   
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    try:
        start(sys.argv[1:])
    except KeyboardInterrupt:
        print("Forcebruta 2 interrupted by user, killing all threads....")
