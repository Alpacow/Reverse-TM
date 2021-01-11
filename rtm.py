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
        index = 1
        for t in self.transitions:
            check = t[1]
            sigma = t[4]
            move = t[5]
            _next = index + 1
            newT.append(str(index) + ',' + check + 'BB=' + str(_next) + ',' + sigma + '0B')
            next2 = _next + 1
            newT.append(str(_next) + ',' + '//B=' + str(next2) + ',' + move + move + 'B')
            index += 2
            self.nTransitions = next2
        return newT

    def execution(self):
        self.initTransitions()
        self.transitions = self.getQuadruples()
        print("\n")
        head = 0 # posicao onde se encontra a cabeca na fita
        for transition in self.transitions: # loop pelas transicoes
            aux = transition.partition("=")
            left = aux[0]
            right = aux[2]
            check = left.partition(",")[2][0]
            stage = left.partition(",")[0]
            move_write = right.partition(",")[2][0]

            print("Transition: ", transition) # debug
            print("Head: ", check, " Move or Write: ", move_write) # debug
            #if check == self.input[head]: # input bate com a condicao da transicao
            if check != "/":
                self.inputTape[head] = move_write # recebe o simbolo do lado direito da transicao
                self.historyTape.append(stage) # numero do estagio

            elif check == "/": # caso o simbolo seja uma barra
                if move_write == "L": # avancar para a direita
                    print("Left shift") # debug
                    # se a cabeça da fita é igual ao tamanho da fita -1, ou o cabeça da fita for símbolo branco, diminui a fita
                    if head == len(self.inputTape)-1 or self.inputTape[head] == "B":
                        print("Diminuindo tamanho da fita:", head,len(self.inputTape)-1, self.inputTape[head])
                        self.inputTape = self.inputTape[:head-1]
                        self.inputTape.append("B")
                    head -= 1
                elif move_write == "R": # avancar para a esquerda
                    print("Right shift") # debug
                    head += 1
                    # se a cabeça da fita é igual ao tamanho da fita, a fita é aumentada com um "B"
                    if head == len(self.inputTape):
                        self.inputTape.append("B")
            print(self.inputTape)

        print("\n")
        print("inputTape: ", self.inputTape)
        print("historyTape: ", self.historyTape)

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