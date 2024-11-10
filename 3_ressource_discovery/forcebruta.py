import requests
from threading import Thread
import sys
import getopt


class RequestPerformer(Thread):
    def __init__(self, word, url):
        Thread.__init__(self)
        try:
            self.word = word.strip()
            self.url = url.replace('FUZZ', self.word)
        except Exception as e:
            print(f"Error initializing thread: {e}")

    def run(self):
        global i
        try:
            response = requests.get(self.url)
            print(f"{self.url} - {response.status_code}")
            i[0] -= 1
        except Exception as e:
            print(f"Request failed: {e}")


def banner():
    print("\n**********************************************************************************************")
    print("                             Starting *forceBruta v1.1*    ")
    print("                                                 Writting by Ephraim C Norbert    ")
    print("\n**********************************************************************************************")


def usage():
    print("Usage: script.py -w <url> -f <wordlist_file> -t <threads>")


def start(argv):
    banner()
    if len(argv) < 5:
        usage()
        sys.exit()

    url = ""
    wordlist_file = ""
    threads = 1

    try:
        opts, args = getopt.getopt(argv, "w:f:t:")
    except getopt.GetoptError:
        print("Error in arguments")
        usage()
        sys.exit()

    for opt, arg in opts:
        if opt == '-w':
            url = arg
        elif opt == '-f':
            wordlist_file = arg
        elif opt == '-t':
            threads = int(arg)

    try:
        with open(wordlist_file, "r") as f:
            words = f.readlines()
    except Exception as e:
        print(f"Failed to open file: {wordlist_file}. Error: {e}")
        sys.exit()

    launcher_thread(words, threads, url)


def launcher_thread(words, max_threads, url):
    global i
    i = [0]
    result_list = []

    while words:
        try:
            if i[0] < max_threads:
                word = words.pop(0)
                i[0] += 1
                thread = RequestPerformer(word, url)
                thread.start()
                result_list.append(thread)
        except KeyboardInterrupt:
            print("Forcebruta interrupted by user. Finishing attack...")
            sys.exit()

    for thread in result_list:
        thread.join()


if __name__ == "__main__":
    try:
        start(sys.argv[1:])
    except KeyboardInterrupt:
        print("Forcebruta interrupted by user. Killing all threads...")