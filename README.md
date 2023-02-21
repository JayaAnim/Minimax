# Quadratic connect 4

# Introduction

connectM.py creates quadratic connect 4 game, in which user will play against the program/computer. The board size, number of pieces needed
to be connected, and the starting player are all configurable. The computer uses spacial analysis, board analysis, and threat analysis to create a static
evaluation for board states, then it utilizes a minimax function with alpha-beta pruning to return the best possible move it can make.

This program has been tested against human players and an online connect 4 AI, and has not yet lost with the latest iteration.

# Installation

To install the necessary dependencies for this project, you can use pip with the included requirements.txt file:

First, ensure that you have Python 3 installed on your system. If you do not have Python 3 installed, you can download it from the official website: https://www.python.org/downloads/

Next, create a new virtual environment using the venv module that comes with Python 3:
    python3 -m venv env

Activate the virtual environment:
    On macOS and Linux:
        source env/bin/activate
    On Windows:
        .\env\Scripts\activate

Install the dependencies using the following command:
    pip install -r requirements.txt

This will install all the required packages specified in the requirements.txt file.

Note: If you are using a different package manager like Anaconda or Miniconda, the commands may be slightly different.

# Usage

To start the program:
    python3 connectM.py N M H

1) N will be a number that is greater than or equal to 3 and less than or equal to 10. 
   N is the board size (Example: 10 will be a 10x10 board)

2) M will be a number greater than or equal to 2 and less than or equal to N
   M is the number of disks to get in a row to win (Example: 3 means getting 3 disks in a row results in a win)

3) H will be 0 or 1
   H is the starting player (1 means the computer will make the first move, 0 means the player will make the first move)

To play the terminal will ask you for your move. Moves will be a integer that corresponds to a column. For example, if you want to place a piece in column 2, simply type 2 and then enter when asked. Moves will need to be valid (moves >= 0 and moves <= N) and an integer (For example, a move cannot be "three" it must be 3).

The computer may take longer than expected to return a move on larger boards, however, moves will be returned in no more than 2 minutes on larger boards. Please be patient.

Once the computer or player has won, or a tie has occurred and no more valid moves are left, a prompt anouncing the winner will appear and the program will quit. The program must be restarted to play again.

# Example

![Example run](https://drive.google.com/file/d/1jigU0HzaLGKQtSVVX0CJf4vb4-522EeV/view?usp=share_link)


