class Rtm:
    nStates = 0
    nInput = 0
    nTape = 0
    nTransitions = 0
    states = []
    alphaInput = []
    alphaTape = []
    transitions = []
    moveT = [] # guarda apenas transições de escrita
    writeT = []
    input = []

    inputTape = []
    historyTape = []
    outputTape = []

    head = 0 # posicao onde se encontra a cabeca na fita 'input'
    headH = 0 # posicao da cabeca da fita de 'history'
    state = 0

    currentTransitionIndex = -1
    nextTransitionIndex = 0

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
        count = 0
        for t in self.transitions:
            tr = t[0]
            tr2 = t[3]
            check = t[1]
            symbol = t[4]
            sigma = t[5]
            self.writeT.append(tr + ',' + check + '/B=' + tr + ',' + symbol + sigma + 'B')
            self.moveT.append(tr + ',' + '/B/=' + tr2 + ',' + sigma + tr + '0')
            count += 2
        self.nTransitions = count

    def execution(self):
        print("Estado inicial:")
        self.printTapes()
        self.initTransitions()
        self.getQuadruples() # transicoes estao em writeT e moveT
        print("Estagio 1:")
        self.Stage_1()
        self.printTapes()
        """
        print("Estagio 2:")
        self.Stage_2()
        self.printTapes()
        print("Estagio 3:")
        self.Stage_3()
        self.printTapes()
        """

    def setNextWriteTransitionByState(self, state):
        #print("--Procurando estado", state) # debug
        self.currentTransitionIndex += 1
        if self.currentTransitionIndex >= len(self.writeT):
            #print("Passou, atualizando index transicao", self.currentTransitionIndex)  # debug
            self.currentTransitionIndex = 0
        for i in range(self.currentTransitionIndex, len(self.writeT)): # loop pelas transicoes
            if int(self.writeT[i][0]) == int(state):
                self.currentTransitionIndex = i
                self.nextTransitionIndex = i
                return

    def Stage_1(self):
        self.setNextWriteTransitionByState(1) # vai pega a transicao do estagio 1
        nextState = self.writeT[self.currentTransitionIndex][0] # pega o primeiro estado valido
        print(self.writeT[self.currentTransitionIndex], nextState)
        i = 0
        while True:
            print("*-- INPUT --*: ", self.inputTape, "Cabeca: ", self.head, self.inputTape[self.head])
            tWrite = self.writeT[self.currentTransitionIndex] # pega a transicao de escrita atual
            stateW, checkW, write = self.getValues(tWrite)
            print("Transicao de escrita:", tWrite)

            tMove = self.moveT[self.currentTransitionIndex] # pega a transicao de movimento atual
            stateM, checkM, move = self.getValues(tMove)
            print("Transicao de movimento:", tMove)
            if stateW == nextState and self.inputTape[self.head] == checkW: # se a cabeca da fita corresponde ao simbolo da transicao de write
                nextState = tMove.partition("=")[2][0]
                print("Proximo estado e", nextState)
                self.inputTape[self.head] = write # recebe o simbolo do lado direito da transicao
                self.historyTape.append(stateW) # numero do estado
                # apos escrever, realiza o movimento correspondente
                if move == "L": # avanca cabeca da fita 1 para a esquerda
                    self.head -= 1
                    print("Escreveu", write, "Moveu pra esquerda",self.head)
                elif move == "R": # avanca cabeca da fita 1 para a direita
                    self.head += 1
                    print("Escreveu", write, "Moveu pra direita",self.head)
                self.setNextWriteTransitionByState(nextState) # envia o valor do estagio para onde tem que saltar
            else:
                self.setNextWriteTransitionByState(nextState) # envia o valor do estagio para onde tem que saltar
            i += 1
            if(self.currentTransitionIndex >=  len(self.writeT) or self.head >= len(self.inputTape) or self.head < 0):
                break
        print("cabeca parou em = ", self.head)

    def Stage_2(self):
        self.invertTransitions()
        self.outputTape = self.inputTape.copy(); # copia a fita 1 para a fita 3

    def Stage_3(self):
        self.setNextWriteTransitionByState(1) # vai pega a transicao do estagio 1
        nextState = self.writeT[self.currentTransitionIndex][0] # pega o primeiro estado valido
        print(self.writeT[self.currentTransitionIndex], nextState)
        i = 0
        while True:
            print("*-- INPUT --*: ", self.inputTape, "Cabeca: ", self.head, self.inputTape[self.head])
            tWrite = self.writeT[self.currentTransitionIndex] # pega a transicao de escrita atual
            stateW, checkW, write = self.getValues(tWrite)
            print("Transicao de escrita:", tWrite)

            tMove = self.moveT[self.currentTransitionIndex] # pega a transicao de movimento atual
            stateM, checkM, move = self.getValues(tMove)
            print("Transicao de movimento:", tMove)
            if stateW == nextState and self.inputTape[self.head] == checkW: # se a cabeca da fita corresponde ao simbolo da transicao de write
                nextState = tMove.partition("=")[2][0]
                print("Proximo estado e", nextState)
                self.inputTape[self.head] = write # recebe o simbolo do lado direito da transicao
                self.historyTape.append(stateW) # numero do estado
                # apos escrever, realiza o movimento correspondente
                if move == "L": # avanca cabeca da fita 1 para a esquerda
                    self.head -= 1
                    print("Escreveu", write, "Moveu pra esquerda",self.head)
                elif move == "R": # avanca cabeca da fita 1 para a direita
                    self.head += 1
                    print("Escreveu", write, "Moveu pra direita",self.head)
                self.setNextWriteTransitionByState(nextState) # envia o valor do estagio para onde tem que saltar
            else:
                self.setNextWriteTransitionByState(nextState) # envia o valor do estagio para onde tem que saltar
            i += 1
            if(self.currentTransitionIndex >=  len(self.writeT) or self.head >= len(self.inputTape) or self.head < 0):
                break
        print("cabeca parou em = ", self.head)

    def invertTransitions(self): # Stage 2
        for index in range(0, len(self.transitions)): # inverte as letras direcionais
            if "R" in self.transitions[index]:
                self.transitions[index] = self.transitions[index].replace("R", "L")
            elif "L" in self.transitions[index]:
                self.transitions[index] = self.transitions[index].replace("L", "R")
            part = self.transitions[index].partition("=")
            auxLeft = part[0]
            auxRight = part[2]
            l = auxLeft.partition(",")
            r = auxRight.partition(",")
            if (index % 2 == 0):
                newL = r[0] + "," + r[2][0] + l[2][1] + r[2][2]
                newR = l[0] + "," + l[2][0] + r[2][1] + l[2][2]
            else:
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

    def getValues(self, transition):
        aux = transition.partition("=")
        left = aux[0]
        right = aux[2]
        state = left.partition(",")[0]
        check = left.partition(",")[2][0]
        move_write = right.partition(",")[2][0]
        return state, check, move_write