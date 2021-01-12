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
        newT = []
        for t in self.transitions:
            tr = t[0]
            tr2 = t[3]
            check = t[1]
            symbol = t[4]
            sigma = t[5]
            self.writeT.append(tr + ',' + check + '/B=' + tr + ',' + symbol + sigma + 'B')
            self.moveT.append(tr + ',' + '/B/=' + tr2 + ',' + sigma + tr + '0')
            newT.append(tr + ',' + check + '/B=' + tr + ',' + symbol + sigma + 'B')
            newT.append(tr + ',' + '/B/=' + tr2 + ',' + sigma + tr + '0')
            count += 2
        self.transitions = newT.copy()
        self.nTransitions = count

    def execution(self):
        print("Estado inicial:")
        self.printTapes()
        self.initTransitions()
        self.getQuadruples() # transicoes estao em writeT e moveT
        print("Estagio 1:")
        self.Stage_1()
        self.printTapes()
        print("Estagio 2:")
        self.Stage_2()
        self.printTapes()
        print("Estagio 3:")
        self.Stage_3()
        self.printTapes()

    def setNextTransitionByState(self, state, wm):
        print("--Procurando estado", state) # debug
        if wm == "W":
            tr = self.writeT
        elif wm == "M": # se M deve usar as transicoes de movimento
            if len(self.historyTape) == 0: # se a fita de history ficou vazia nao precisa mais procurar
                return
            tr = self.moveT
        self.currentTransitionIndex += 1
        find = False
        if self.currentTransitionIndex >= len(tr):
            self.currentTransitionIndex = 0
        for i in range(self.currentTransitionIndex, len(tr)): # loop pelas transicoes
            if int(tr[i][0]) == int(state):
                self.currentTransitionIndex = i
                self.nextTransitionIndex = i
                find = True
                break
        if not find:
            self.setNextTransitionByState(state, wm)

    def Stage_1(self):
        self.setNextTransitionByState(1, "W") # vai pega a transicao do estagio 1
        nextState = self.writeT[self.currentTransitionIndex][0] # pega o primeiro estado valido
        while True:
            tWrite = self.writeT[self.currentTransitionIndex] # pega a transicao de escrita atual
            stateW, checkW, write = self.getValues(tWrite)
            tMove = self.moveT[self.currentTransitionIndex] # pega a transicao de movimento atual
            stateM, checkM, move = self.getValues(tMove)
            if stateW == nextState and self.inputTape[self.head] == checkW: # se a cabeca da fita corresponde ao simbolo da transicao de write
                nextState = tMove.partition("=")[2][0]
                self.inputTape[self.head] = write # recebe o simbolo do lado direito da transicao
                self.historyTape.append(stateW) # numero do estado
                # apos escrever, realiza o movimento correspondente
                if move == "L": # avanca cabeca da fita 1 para a esquerda
                    self.head -= 1
                elif move == "R": # avanca cabeca da fita 1 para a direita
                    self.head += 1
                self.setNextTransitionByState(nextState, "W") # envia o valor do estagio para onde tem que saltar
            else:
                self.setNextTransitionByState(nextState, "W") # envia o valor do estagio para onde tem que saltar
            if(self.currentTransitionIndex >=  len(self.writeT) or self.head >= len(self.inputTape) or self.head < 0):
                break
        print("Cabeca da fita 1 parou em = ", self.head)
        self.currentTransitionIndex = 0

    def Stage_2(self):
        self.invertTransitions()
        self.separateTransitions()
        self.outputTape = self.inputTape.copy(); # copia a fita 1 para a fita 3

    def Stage_3(self):
        nextState = self.historyTape[-1] # pega o ultimo estado realizado
        self.setNextTransitionByState(nextState, "M") # seta a transicao do ultimo estado feito
        i = 0
        while i < 30:
            print("\n*-- INPUT --*: ", self.inputTape, "Cabeca: ", self.head)
            print("History Tape: ", self.historyTape)
            tMove = self.moveT[self.currentTransitionIndex] # pega a transicao de movimento atual
            stateM, checkM, move = self.getValues(tMove)
            print("Transicao de movimento:", tMove)

            tWrite = self.writeT[self.currentTransitionIndex] # pega a transicao de escrita atual
            stateW, checkW, write = self.getValues(tWrite)
            print("Transicao de escrita:", tWrite)

            nextStateOfTransition = tWrite.partition("=")[2][0] # pega o proximo estado da transicao de escrita atual
            print(nextState, " eh o ATUAL ", tWrite.partition("=")[2], "do", nextState, "para", nextStateOfTransition, "Esperado eh: ", self.historyTape[-1])
            # se o estado é o esperado, a cabeca da fita corresponde ao simbolo da transicao de move e o prox estado eh oq esta em 'history'
            if stateM == nextState and self.isSymbolValid(checkW, move)  and int(nextStateOfTransition) == int(self.historyTape[-1]):
                if move == "L": # avanca cabeca da fita 1 para a esquerda
                    self.head -= 1
                    print("Moveu pra esquerda",self.head, "Escreveu", write)
                elif move == "R": # avanca cabeca da fita 1 para a direita
                    self.head += 1
                    print("Moveu pra direita",self.head, "Escreveu", write)
                # apos mover, realiza a escrita correspondente
                self.inputTape[self.head] = write # recebe o simbolo do lado direito da transicao
                nextState = self.historyTape.pop() # retira o numero do estado
                print("Proximo estado e", nextState, self.historyTape,len(self.historyTape) == 0)
                self.setNextTransitionByState(nextState, "M") # envia o valor do estagio para onde tem que saltar
            else:
                self.setNextTransitionByState(nextState, "M") # envia o valor do estagio para onde tem que saltar
            i += 1
            if(self.head >= len(self.inputTape) or self.head < 0 or len(self.historyTape) == 0):
                print("Finalizado")
                return

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

    def separateTransitions(self):
        self.moveT = []
        self.writeT = []
        for t in self.transitions:
            tr = t[2]
            if tr == '/': # se for movimento
                self.moveT.append(t)
            else:
                self.writeT.append(t)

    def isSymbolValid(self, checkW, move):
        aux = -1
        if move == "L": # avanca cabeca da fita 1 para a esquerda
            aux = self.head - 1
        elif move == "R": # avanca cabeca da fita 1 para a direita
            aux = self.head + 1
        return self.inputTape[aux] == checkW