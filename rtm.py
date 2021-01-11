class Rtm:
    nStates = 0
    nInput = 0
    nTape = 0
    nTransitions = 0
    states = []
    alphaInput = []
    alphaTape = []
    transitions = []
    input = []

    inputTape = []
    historyTape = []
    outputTape = []

    head = 0 # posicao onde se encontra a cabeca na fita 'input'
    headH = 0 # posicao da cabeca da fita de 'history'
    state = 0

    currentTransitionIndex = 0

    def __init__(self, nStates, nInput, nTape, nTransitions, states, alphaInput, alphaTape, transitions, _input):
        self.nStates = nStates
        self.nInput = nInput
        self.nTape = nTape
        self.nTransitions = nTransitions
        self.states = states
        self.alphaInput = alphaInput
        self.alphaTape = alphaTape
        self.transitions = transitions
        self.input = _input

        self.inputTape = [i for i in self.input]
        self.outputTape = ["B" for i in range(len(self.input))]

    def printValues(self):
        print("Número de estados: ", self.nStates)
        print("Estados: ", self.states)
        print("Número de símbolos do alfabeto de entrada: ", self.nInput)
        print("Alfabeto de entrada:", self.alphaInput)
        print("Número de símbolos do alfabeto da fita: ", self.nTape)
        print("Alfabeto da fita: ", self.alphaTape)
        print("Número de transições: ", self.nTransitions)
        print("Transições: ", self.transitions)
        print("Entrada: ", self.input)
        print("Fita 1: ", self.inputTape)
        print("Fita 3: ", self.outputTape)
        print("\nInput check: ", self.checkInput())
        print("State check: ", self.checkStates())
        print("Symbols check: ", self.checkSymbols())
        print("Tape symbols check: ", self.checkTapeSymbols())
        print("Transitions check: ", self.transitionsCheck())

    def initTransitions(self): # remove as virgulas e parenteses
        for i in range(len(self.transitions)):
            self.transitions[i] = self.transitions[i].replace(",", "")
            self.transitions[i] = self.transitions[i].replace("(", "")
            self.transitions[i] = self.transitions[i].replace(")", "")

    def getQuadruples(self):
        newT = []
        for t in self.transitions:
            tr = t[0]
            tr2 = t[3]
            check = t[1]
            symbol = t[4]
            sigma = t[5]
            newT.append(tr + ',' + check + '/B=' + tr + ',' + symbol + sigma + 'B')
            newT.append(tr + ',' + '/B/=' + tr2 + ',' + sigma + sigma + '0')
        return newT

    def execution(self):
        print("Estado inicial:")
        self.printTapes()
        print("Estagio 1:")
        self.Stage_1()
        self.printTapes()
        print("Estagio 2:")
        #self.Stage_2()
        #self.printTapes()
        #self.Stage_3()
        #self.printTapes()

    def setTransitionByStage(self, stage):

        if int(stage) == self.nStates:
            print("\nIt's all over, bro.")
            exit()

        count = -1
        for t in self.transitions: # loop pelas transicoes
            count += 1
            if t[0] == stage:
                print(t[0])
                self.currentTransitionIndex = count
                print("\n ----- Saltou transicao ------ Recebeu o valor: ", stage, " Setando index para: ", count, "\n")
                return
            

    def Stage_1(self):
        self.initTransitions()
        self.transitions = self.getQuadruples()

        print("\nTransitions: ", self.transitions, "\n")

        self.state = self.transitions[0][0]

        self.setTransitionByStage(1) # vai paga a transicao do estagio 1

        while True:

            print("Input: ", self.inputTape)

            transition = self.transitions[self.currentTransitionIndex] # pega a transicao atual
            print("\nTransicao atual: ", transition, " index: ", self.currentTransitionIndex, "\n")
            aux = transition.partition("=")
            left = aux[0]
            right = aux[2]
            curState = left.partition(",")[0]
            check = left.partition(",")[2][0] # se a entrada for quintupla
            stage = left.partition(",")[0]
            move_write = right.partition(",")[2][0]

            print ("Fita: ", self.inputTape, "Head at: ", self.inputTape[self.head])

            print("\nCheck: ", self.inputTape[self.head], "\n")
            print("\nHead: ", self.inputTape[self.head], "\n")

            if check != "/" and self.inputTape[self.head] == check: # se nao é uma barra -> ESCREVE
                self.inputTape[self.head] = move_write # recebe o simbolo do lado direito da transicao
                self.historyTape.append(stage) # numero do estagio
                print("\nEscreveu\n")
                self.currentTransitionIndex += 1 # incrementa o index da transicao
                wrote = True

            elif check == "/": # caso o simbolo seja uma barra -> MOVE

                if move_write == "L": # avancar para a esquerda
                    print("Movendo pra esquerda", self.head)
                    self.head -= 1
                elif move_write == "R": # avancar para a direita
                    self.head += 1
                    print("Movendo pra direita", self.head)
                    # se a cabeça da fita é igual ao tamanho da fita, a fita é aumentada com um "B"
                    if self.head == len(self.inputTape):
                        self.inputTape.append("B")

                if right[0] != curState: # o seguinte eh outro valor de estagio
                    self.setTransitionByStage(right[0]) # envia o valor do estagio para onde tem que saltar

                else:
                    self.currentTransitionIndex -= 1 # volta para a transicao anterior a este deslocamento
                    
                    
                #elif self.inputTape[self.head] != check: # avanca a transicao
                #   if move_write == "R":
                #       self.currentTransitionIndex += 1
                #  elif move_write == "L":
                #     self.currentTransitionIndex -= 1

            elif check != "/":
                self.currentTransitionIndex += 2

            if(self.currentTransitionIndex > len(self.transitions)):
                print("It's over, bro.")
                exit(0)

    def Stage_2(self):
        self.invertTransitions()
        self.outputTape = self.inputTape; # copia a fita 1 para a fita 3

    def Stage_3(self):
        print("Cabeça fita1", self.head)
        for transition in self.transitions: # loop pelas transicoes
            aux = transition.partition("=")
            left = aux[0]
            right = aux[2]
            check = left.partition(",")[2][0] # se a entrada for quintupla
            move_write = right.partition(",")[2][0]
            print("Transicao:", transition)
            if check != "/": # se nao é uma barra -> ESCREVE
                self.inputTape[self.head] = check # recebe o simbolo do lado direito da transicao
                self.historyTape = self.historyTape[:-1] # remove o ultimo estagio
            elif check == "/": # caso o simbolo seja uma barra -> MOVE
                if move_write == "L": # avancar para a esquerda
                    self.head -= 1
                    print("Movendo pra esquerda", self.head)
                elif move_write == "R": # avancar para a direita
                    self.head += 1
                    # se a cabeça da fita é igual ao tamanho da fita, a fita é aumentada com um "B"
                    if self.head == len(self.inputTape):
                        self.inputTape.append("B")
                        print("Movendo pra direita", self.head)
            print("Fita 1:", self.inputTape)

    def invertTransitions(self): # Stage 2
        for index in range(0, len(self.transitions)): # inverte as letras direcionais
            if "R" in self.transitions[index]:
                self.transitions[index] = self.transitions[index].replace("R", "L")
            elif "L" in self.transitions[index]:
                self.transitions[index] = self.transitions[index].replace("L", "R")
            part = self.transitions[index].partition("=") # inverte a ordem
            auxLeft = part[0]
            auxRight = part[2]
            l = auxLeft.partition(",")
            r = auxRight.partition(",")
            newL = r[0] + "," + l[2][0] + r[2][1] + l[2][2]
            newR = l[0] + "," + r[2][0] + l[2][1] + r[2][2]
            self.transitions[index] = newL + "=" + newR
        self.transitions.reverse()

    def checkInput(self):
        for val in self.input:
            if val not in self.alphaInput:
                return False
        return True

    def checkStates(self):
        size = len(self.states.replace(" ", ""))
        return size == self.nStates

    def checkSymbols(self):
        size = len(self.alphaInput.replace(" ", ""))
        return size == self.nInput

    def checkTapeSymbols(self):
        size = len(self.alphaTape.replace(" ", ""))
        return size == self.nTape

    def transitionsCheck(self):
        return self.nTransitions == len(self.transitions)

    def printTapes(self):
        print("inputTape:", self.inputTape)
        print("historyTape:", self.historyTape)
        print("OutputTape:", self.outputTape, "\n")