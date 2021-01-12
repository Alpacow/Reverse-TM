import sys
import select
from rtm import Rtm

def readFile(file):
    dt = file.splitlines()
    n = dt[0].split()
    rtm = Rtm( int(n[0]), int(n[1]), int(n[2]), int(n[3]), dt[1], dt[2], dt[3], dt[4:-1], dt[len(dt) - 1])
    rtm.execution()

def main (args):
    print("*-- Máquina de Turing Reversível --*\n")
    if not select.select([sys.stdin,],[],[],0.0)[0]:
        print("Entrada do programa deve ser 'python3 simulador.py < nome_arquivo.txt'")
        exit(-2)
    readFile(sys.stdin.read())


if __name__ == "__main__":sys.exit(main(sys.argv))