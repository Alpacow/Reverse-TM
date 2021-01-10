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

    inputTape = ["B","B"]
    historyTape = ["B","B"]
    outputTape = ["B","B"]

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

    def execution(self):

        self.initTransitions()

        print("\n")

        index = 1 # posicao onde se encontra a cabeca na transicao
        head = 0 # posicao onde se encontra a cabeca na fita
        offset = 5 # deslocamento ate o outro lado
        for transition in self.transitions: # loop pelas transicoes

            print("Transition: ", transition) # debug
            print("Head: ", transition[index]) # debug

            if transition[index] == self.input[head]: # input bate com a condicao da transicao
                self.inputTape[head] = transition[index + offset] # recebe o simbolo do lado direito da transicao
                self.historyTape[head] = transition[0] # numero do estagio

            elif transition[index] == "/": # caso o simbolo seja uma barra
                if transition[index + offset] == "L": # avancar para a direita
                    print("Left shift") # debug
                    head -= 1
                elif transition[index + offset] == "R": # avancar para a esquerda
                    print("Right shift") # debug
                    head += 1

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