import copy #Utilizado para copiar listas e matrizes
import sys  #Utilizado para implementar infinito computacional 

class infinity:
    
    def __init__(self, color):
        self.color = color
        #Inicializa o numero de jogadas ja realizadas
        global njogadas
        njogadas = 0

#############################################################################################
####################### HEURISTICAS DE JOGO #################################################

    def amadoscantos(self, board): #Quem domina os cantos tem maior chance de vitoria : [1][1],[1][8],[8][1],[8][8]
        resultado = 0
        cantos = (1,8)
        for i in cantos:
            for j in cantos:
                if board.board[i][j] == self.color:
                    resultado += sys.maxint
                elif ((board.board[i][j] != self.color) and (board.board[i][j] != board.EMPTY)):
                    resultado -= sys.maxint
        return resultado

    def contardominio(self, board): #Quantas casas estao sobre meu dominio
        minhascasas = 0.0
        for i in range(1, 9):
            for j in range(1, 9):
                if board.board[i][j] == self.color:
                    minhascasas += 1.0
        return minhascasas

    def meusmovimentosdisponiveis(self, board):
        return len(board.valid_moves(self.color))

    def movimentosdisponiveisinimigo(self, board):
        if (self.color == board.WHITE):
            return len(board.valid_moves(board.BLACK))
        else:
            return len(board.valid_moves(board.WHITE))
    

#############################################################################################
####################### HEURISTICA RESULTANTE ###############################################

    def heuristic(self, board):
            return self.meusmovimentosdisponiveis(board) + self.amadoscantos(board) - self.movimentosdisponiveisinimigo(board) + (
            self.contardominio(board) / 100)     

#############################################################################################
################## ALGORITMO MINMAX COM CORTE ALPHABETA #####################################

    def minmaxcortealphabeta(self, board, depth, alpha, beta, tipo):
        global jogada
        global auxiliar
       
        #FIM DE JOGO
        if (depth == 0) or (self.meusmovimentosdisponiveis(board) == 0):
            return self.heuristic(board)

        #Define as cores do inimigo
        enemyColor = board.BLACK
        if (self.color == board.BLACK):
            enemyColor = board.WHITE
        
        
        if (tipo == False): # Se tipo for false roda min
            #Arvore MIN
            moves = board.valid_moves(enemyColor)
            #Inicializa o no como +infinito
            no = sys.maxint
            #Para cada jogada possivel
            for move in moves:
                newboard = copy.deepcopy(board)
                newboard.play(move, enemyColor)
                no = min(
                    no,
                    self.minmaxcortealphabeta(
                        newboard,
                        depth - 1,
                        alpha,
                        beta,
                        True))
                beta = min(beta, no)
                #Corte na Arvore
                if (beta <= alpha):
                    break
            return no
        #Arvore MAX
        else:
            moves = board.valid_moves(self.color)
            #Inicializa o no como -infinito
            no = -sys.maxint
            for move in moves:
                newboard = copy.deepcopy(board)
                newboard.play(move, self.color)
                no = max(
                    no,
                    self.minmaxcortealphabeta(
                        newboard,
                        depth - 1,
                        alpha,
                        beta,
                        False))
                alpha = max(alpha, no)
                if (depth == profundidade) and (no > auxiliar):
                    auxiliar = no
                    jogada = copy.copy(move)
                #Corte na Arvore
                if (beta <= alpha):
                    break
            return no

#############################################################################################
####################### JOGANDO #############################################################

    def play(self, board):
        moves = board.valid_moves(self.color)
        global profundidade
        global auxiliar
        global njogadas 
        #Um numero menor de profundidade reduz o tempo de jogada quando ha muitas jogadas possiveis
        profundidade = 2
        #Se ja ocorreram 21 jogadas, entao aumentamos a profundidade da arvore
        if (njogadas>21):
            profundidade = 5
        #Auxiliar para comparacao do no
        auxiliar = -sys.maxint
        #chama o algoritmo minmax
        self.minmaxcortealphabeta(board, profundidade, -sys.maxint, sys.maxint, True)
        global jogada
        #Mais uma jogada foi feita, entao soma 1 na quantidade de jogadas
        #Esse metodo melhora o tempo de execucao em comparacao a outros codigos que buscam as casas livres a cada jogada
        njogadas+=1
        return jogada

#############################################################################################
#############################################################################################
