import sys
from rtm import Rtm

def readFile(file):
    dt = file.splitlines()
    n = [dt[0][i] for i in range(len(dt[0])) if dt[0][i] != ' ']
    rtm = Rtm( int(n[0]), int(n[1]), int(n[2]), int(n[3]), dt[1], dt[2], dt[3], dt[4:-1], dt[len(dt) - 1])
    rtm.printValues()

def main (args):
    print("*-- Máquina de Turing Reversível --*\n")

    readFile(sys.stdin.read())

if __name__ == "__main__":sys.exit(main(sys.argv))