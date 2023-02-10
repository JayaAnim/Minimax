import argparse
from board import Board

def main():
    parser = argparse.ArgumentParser(description='ConnectM game')
    parser.add_argument('N', type=int, help='board size (3 <= N <= 10)')
    parser.add_argument('M', type=int, help='number of pieces in a row to win (1 <= M <= N)')
    parser.add_argument('H', type=int, help='starting player (H == 0 or H == 1)')

    args = parser.parse_args()

    N = args.N
    M = args.M
    H = args.H

    board = Board(N, M, H)

if __name__ == '__main__':
    main()