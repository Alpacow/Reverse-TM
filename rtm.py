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
        print("\nInput check: ", self.checkInput())
        print("State check: ", self.checkStates())
        print("Symbols check: ", self.checkSymbols())
        print("Tape symbols check: ", self.checkTapeSymbols())
        print("Transitions check: ", self.transitionsCheck(), "\n")

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
        self.transitions = newT
        self.nTransitions = count

    def execution(self):
        print("ESTADO INICIAL")
        self.printValues()
        if not self.checkTmValues():
            print("Valores iniciais da MT são inválidos")
            exit(-1)
        self.printTapes()
        self.initTransitions()
        self.getQuadruples() # transicoes ficam em writeT e moveT
        print("ESTAGIO 1: realiza os passos de uma MT")
        self.Stage_1()
        self.printTapes()
        print("ESTAGIO 2: inverte as transições e copia Fita 1 para Fita 3")
        self.Stage_2()
        self.printTapes()
        print("ESTAGIO 3: realiza os passos da MT para reverter a Fita 1")
        self.Stage_3()
        self.printTapes()

    def setNextTransitionByState(self, state, wm):
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
            _, _, move = self.getValues(tMove)
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
        self.currentTransitionIndex = 0

    def Stage_2(self):
        self.invertTransitions()
        self.separateTransitions()
        self.outputTape = self.inputTape.copy(); # copia a fita 1 para a fita 3

    def Stage_3(self):
        nextState = self.historyTape[-1] # pega o ultimo estado realizado
        self.setNextTransitionByState(nextState, "M") # seta a transicao do ultimo estado feito
        i = 0
        while True:
            tMove = self.moveT[self.currentTransitionIndex] # pega a transicao de movimento atual
            stateM, _, move = self.getValues(tMove)
            tWrite = self.writeT[self.currentTransitionIndex] # pega a transicao de escrita atual
            _, checkW, write = self.getValues(tWrite)
            nextStateOfTransition = tWrite.partition("=")[2][0] # pega o proximo estado da transicao de escrita atual
            # se o estado é o esperado, a cabeca da fita corresponde ao simbolo da transicao de move e o prox estado eh oq esta em 'history'
            if stateM == nextState and self.isSymbolValid(checkW, move)  and int(nextStateOfTransition) == int(self.historyTape[-1]):
                if move == "L": # avanca cabeca da fita 1 para a esquerda
                    self.head -= 1
                elif move == "R": # avanca cabeca da fita 1 para a direita
                    self.head += 1
                # apos mover, realiza a escrita correspondente
                self.inputTape[self.head] = write # recebe o simbolo do lado direito da transicao
                nextState = self.historyTape.pop() # retira o numero do estado
                self.setNextTransitionByState(nextState, "M") # envia o valor do estagio para onde tem que saltar
            else:
                self.setNextTransitionByState(nextState, "M") # envia o valor do estagio para onde tem que saltar
            i += 1
            if(self.head >= len(self.inputTape) or self.head < 0 or len(self.historyTape) == 0):
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
            if (index % 2 == 0): # transicoes de movimento = mantem apenas o simbolo
                newL = r[0] + "," + r[2][0] + l[2][1] + r[2][2]
                newR = l[0] + "," + l[2][0] + r[2][1] + l[2][2]
            else: # transicoes de escrita = troca o simbolo do meio e os estados
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
        print("Fita 1 -> Entrada:", self.inputTape)
        print("Fita 2 -> Histórico:", self.historyTape)
        print("Fita 3 -> Saída:", self.outputTape, "\n")

    def getValues(self, transition): # retorna apenas os valores significativos de cada quadrupla
        aux = transition.partition("=")
        left = aux[0]
        right = aux[2]
        state = left.partition(",")[0]
        check = left.partition(",")[2][0]
        move_write = right.partition(",")[2][0]
        return state, check, move_write

    def separateTransitions(self): # separa as transicoes invertidas em duas listas
        self.moveT = []
        self.writeT = []
        for t in self.transitions:
            tr = t[2]
            if tr == '/': # se for movimento
                self.moveT.append(t)
            else:         # se for escrita
                self.writeT.append(t)

     # verifica se simbolo da transicao de escrita e valido apos movimentar cabeca da fita 1
    def isSymbolValid(self, checkW, move):
        aux = -1
        if move == "L":   # avanca cabeca da fita 1 para a esquerda
            aux = self.head - 1
        elif move == "R": # avanca cabeca da fita 1 para a direita
            aux = self.head + 1
        return self.inputTape[aux] == checkW
    
    def checkTmValues(self):
        return self.checkInput() and self.checkSymbols() and self.checkTapeSymbols() and self.transitionsCheck()