from board import Board
from copy import deepcopy

class Node:
    def __init__(self, possible_moves: list, current_moves: list, depth, init_board: Board):
        #initial board state for bottom of tree
        self.init_board = None
        #child nodes
        self.child_nodes = []
        #keeps track of if node ends before end of depth
        self.final_node = False
        #current move
        self.moves = 0


        #if node is at bottom of tree
        if depth == 0 or sum(possible_moves) == 0:
            self.final_node = True
            self.init_board = init_board
            self.moves = current_moves
        #if node is not at bottom of the tree
        else:
            #generate child nodes
            for i in range(len(possible_moves)):
                #checks whether move is possible
                if possible_moves[i] != 0:
                    #if possible, create a deep copy of current moves and possible moves, then modify each to reflect move
                    new_current_moves = deepcopy(current_moves)
                    new_current_moves.append(i + 1)
                    new_possible_moves = deepcopy(possible_moves)
                    new_possible_moves[i] -= 1
                    #append child nodes list with new node of new changes
                    self.child_nodes.append(Node(new_possible_moves, new_current_moves, depth - 1, init_board))

    def getUtilityAndMove(self) -> tuple:
            #keeps track of number of moves made to get to win, to incentivize early wins
            numMoves = 0
            #create a deepcopy of current state of the board
            board = Board(self.init_board.N, self.init_board.M, self.init_board.H)
            board.createCopyBoard(self.init_board.board, self.init_board.board_cols)
            #place moves onto new board
            for move in self.moves:
                numMoves += 1
                #if a move results in a win, evaluate the board and return
                if not board.validateMove(move):
                    print('critical error')
                if board.placeMove(move):
                    utility = board.enumBoard()
                    if numMoves != 0:
                        return (utility / numMoves, self.moves[0])
                    else:
                        return (utility, self.moves[0])
            #if no moves resulted in a win, evaluate the board and return
            utility = board.enumBoard()
            if numMoves != 0:
                return (utility / numMoves, self.moves[0])
            else:
                return (utility, self.moves[0])


def generateMove(init_board: Board) -> int:
    depth = init_board.getDepthToSearch()
    head_node = Node(init_board.board_cols, [], depth, init_board)
    utility, move = minimax(head_node, depth, float('-inf'), float('inf'), True)
    return move

def minimax(node: Node, depth, alpha, beta, maximizingComputer):
    if depth == 0 or node.final_node:
        utility, move = node.getUtilityAndMove()
        return utility, move

    if maximizingComputer:
        maxEval = float('-inf')
        maxMove = None
        for child_node in node.child_nodes:
            eval, move = minimax(child_node, depth - 1, alpha, beta, False)
            if eval > maxEval:
                maxEval = eval
                maxMove = move
            if eval > alpha:
                alpha = eval
            if beta <= alpha:
                break
        return maxEval, maxMove
    
    else:
        minEval = float('inf')
        minMove = None
        for child_node in node.child_nodes:
            eval, move = minimax(child_node, depth - 1, alpha, beta, True)
            if eval < minEval:
                minEval = eval
                minMove = move
            if eval < beta:
                beta = eval
            if beta <= alpha:
                break
        return minEval, minMove




            