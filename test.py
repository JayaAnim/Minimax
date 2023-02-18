import argparse
from board import Board

def main():
    parser = argparse.ArgumentParser(description='ConnectM game')
    parser.add_argument('N', type=int, help='board size (3 <= N <= 10)')
    parser.add_argument('M', type=int, help='number of pieces in a row to win (1 <= M <= N)')
    parser.add_argument('H', type=int, help='starting player (H == 0 or H == 1)')

    args = parser.parse_args()

    params = handleParameters(args.N, args.M, args.H)
    board = Board(params[0], params[1], params[2])
    board.createNewBoard()

    
    while True:
        if board.H == 0:
            board.printBoard()
            print(board.enumBoard())
            move = int(input('Please enter the column (integer) to make your move: '))
            if handleMove(board, move):
                board.printBoard()
                handleWin(board.winner)
        elif board.H == 1:
            board.printBoard()
            print(board.enumBoard())
            move = int(input('Please enter the column (integer) to make your move: '))
            if handleMove(board, move):
                board.printBoard()
                handleWin(board.winner)
    
    

#Handles players making invalid moves
def handleMove(board, move) -> bool:
    while not board.validateMove(move):
        move = int(input('That move is invalid please enter another move: '))
    return board.placeMove(move)

#Handles players inserting invalid parameters
def handleParameters(N, M, H) -> tuple:
    while N < 3 or N > 10:
        print('Error: invalid board size')
        print('Parameters (3 <= N <= 10)')
        N = int(input('Please enter a new board size: '))

    while M <= 1 or M > N:
        print('Error: invalid disks value')
        print('Parameters (1 < M <= N)')
        M = int(input('Please enter a new disk value: '))
    
    while H != 0 and H != 1:
        print('Error: invalid starting player')
        print('Parameters (H == 1 or H == 0)')
        H = int(input('Please enter a new starting player: '))
    
    return (N, M, H)

#Handles player or computer winning
def handleWin(H):
    if H == 1:
        print("╔════════════════════════╗")
        print("║  The computer has won! ║")
        print("╚════════════════════════╝")
        quit()
    elif H == 0:
        print("╔══════════════════════╗")
        print("║  The player has won! ║")
        print("╚══════════════════════╝")
        quit()
    else:
        print('Critical error: Invalid winner')
        print('Program will now close')
        quit()

if __name__ == '__main__':
    main()