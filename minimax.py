from board import Board
from copy import deepcopy

class Node:
    def __init__(self, possible_moves: list, current_moves: list, depth, init_board: Board):
        #static evaluation of board
        self.utility = 0
        #child nodes
        self.child_nodes = []
        #keeps track of if node ends before end of depth
        self.final_node = False


        #if node is at bottom of tree
        if depth == 0 or sum(possible_moves) == 0:
            self.final_node = True
            #create a deepcopy of current state of the board
            board = Board(init_board.N, init_board.M, init_board.H)
            board.createCopyBoard(init_board.board, init_board.board_cols)
            #place moves onto new board
            for move in current_moves:
                #if a move results in a win, evaluate the board and return
                if board.placeMove(move):
                    self.utility = board.enumBoard()
                    return
            #if no moves resulted in a win, evaluate the board and return
            self.utility = board.enumBoard()
            return
        #if node is not at bottom of the tree
        else:
            #generate child nodes
            for i in range(len(possible_moves)):
                #checks whether move is possible
                if possible_moves[i] != 0:
                    #if possible, create a deep copy of current moves and possible moves, then modify each to reflect move
                    new_current_moves = deepcopy(current_moves)
                    new_current_moves.append(possible_moves[i])
                    new_possible_moves = deepcopy(possible_moves)
                    new_possible_moves[i] -= 1
                    #append child nodes list with new node of new changes
                    self.child_nodes.append(Node(new_possible_moves, new_current_moves, depth - 1, init_board))

def generateMove(init_board: Board) -> int:
    head_node = Node(init_board.board_cols, [], 3, init_board)
    result = minimax(head_node, 3, True)
    return result

#maximizingComputer means it is computer's (H == 1) turn
def minimax(node: Node, depth, maximizingComputer):
    if depth == 0 or node.final_node:
        return node.utility

    if maximizingComputer:
        maxEval = float('-inf')
        for child_node in node.child_nodes:
            eval = minimax(child_node, depth - 1, False)
            maxEval = max(maxEval, eval)
        return maxEval
    
    else:
        minEval = float('inf')
        for child_node in node.child_nodes:
            eval = minimax(child_node, depth - 1, True)
            minEval = min(minEval, eval)
        return minEval
    
board = Board(3, 3, 1)
board.createNewBoard()
generateMove(board)



            