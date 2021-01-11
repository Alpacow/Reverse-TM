import sys
from rtm import Rtm

def readFile(file):
    dt = file.splitlines()
    n = dt[0].split()
    rtm = Rtm( int(n[0]), int(n[1]), int(n[2]), int(n[3]), dt[1], dt[2], dt[3], dt[4:-1], dt[len(dt) - 1])
    rtm.execution()
    #for t in rtm.transitions:
    #   print(t)

def main (args):
    print("*-- Máquina de Turing Reversível --*\n")
    readFile(sys.stdin.read())
    #TODO: tratar quando nao passa nada pro stdin ler (ta entrando em loop do jeito que ta)


if __name__ == "__main__":sys.exit(main(sys.argv))