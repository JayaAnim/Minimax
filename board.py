from copy import deepcopy
from collections import deque
import math
from gaussian import genGaussianBoard

class Board:
    gauss_assigned = None
    gaussian_board = None

    def __init__(self, N, M, H):
        #N is number of cols/rows in n x n grid
        #M is number of disks to connect contiguously 
        #H is who makes the next move (1 = computer, 0 = human)
        #board_cols is a list of next available board space + 1, if value is 0 no spaces are left
        self.N = N
        self.M = M
        self.H = H
        self.board_cols = [self.N] * self.N
        self.winner = -1

        if not Board.gauss_assigned:
            Board.gauss_assigned = True
            Board.gaussian_board = genGaussianBoard(self.N)
        

    #creates new empty board
    def createNewBoard(self):
        self.board = [[' ' for j in range(self.N)] for i in range(self.N)]

    #creates deepcopy of existing board
    def createCopyBoard(self, board):
        self.board = deepcopy(board)

    #prints board to console
    def printBoard(self):
        for i in self.board:
            print('+' + '---+' * self.N)
            index = 1
            for j in i:
                print('|' + ' ' + j, end = ' ')
                if index == self.N:
                    print('|')
                else:
                    index += 1
        print('+' + '---+' * self.N)

    #returns true if move is a valid move, False if invalid
    def validateMove(self, move):
        if move <= 0 or move > self.N:
            return False
        elif self.board[0][move - 1] == ' ':
            return True
        else:
            return False
    
    #places move on board and flips next move (self.H)
    def placeMove(self, move) -> bool:
        if self.H == 1:
            self.board[self.board_cols[move - 1] - 1][move - 1] = 'O'
        elif self.H == 0:
            self.board[self.board_cols[move - 1] - 1][move - 1] = 'X'
        
        if self.checkWin(move):
            self.board_cols[move - 1] -= 1
            if self.winner == -1:
                self.winner = self.H
            self.H = self.H ^ 1
            self.enumBoard()
            return True
        else:
            self.board_cols[move - 1] -= 1
            self.H = self.H ^ 1
            self.enumBoard()
            return False

    def checkWin(self, move) -> bool:
        col = move - 1
        row = self.board_cols[move - 1] - 1
        if self.checkRow(col, row):
            return True
        elif self.checkCol(col, row):
            return True
        elif self.checkDiag(col, row):
            return True
        else:
            return False

    def checkDiag(self, col, row) -> bool:
        player_piece = ' '
        if self.H == 1:
            player_piece = 'O'
        elif self.H == 0:
            player_piece = 'X'
        col_counter = col
        row_counter = row
        counter = 1
        #counts bottom left of move
        while col_counter > 0 and row_counter < self.N - 1:
            col_counter -= 1
            row_counter += 1
            if player_piece == self.board[row_counter][col_counter]:
                counter += 1
            else:
                break
        col_counter = col
        row_counter = row
        #counts top right of move
        while col_counter < self.N - 1 and row_counter > 0:
            col_counter += 1
            row_counter -= 1
            if player_piece == self.board[row_counter][col_counter]:
                counter += 1
            else:
                break
        col_counter = col
        row_counter = row
        #checks if win condition met, if not met start search on opposite diagonals
        if self.M <= counter:
            return True
        else:
            col_counter = col
            row_counter = row
            counter = 1
        #checks top left of move
        while col_counter > 0 and row_counter > 0:
            col_counter -= 1
            row_counter -= 1
            if player_piece == self.board[row_counter][col_counter]:
                counter += 1
            else:
                break
        col_counter = col
        row_counter = row
        #checks bottom right of move
        while col_counter < self.N - 1 and row_counter < self.N - 1:
            col_counter += 1
            row_counter += 1
            if player_piece == self.board[row_counter][col_counter]:
                counter += 1
            else:
                break
        if self.M <= counter:
            return True
        else:
            return False

    def checkRow(self, col, row) -> bool:
        player_piece = ' '
        if self.H == 1:
            player_piece = 'O'
        elif self.H == 0:
            player_piece = 'X'
        col_counter = col
        counter = 1
        #check left of move
        while col_counter > 0:
            col_counter -= 1
            if player_piece == self.board[row][col_counter]:
                counter += 1
            else:
                break
        col_counter = col
        #check right of move
        while col_counter < self.N - 1:
            col_counter += 1
            if player_piece == self.board[row][col_counter]:
                counter += 1
            else:
                break
        if self.M <= counter:
            return True
        else:
            return False

    def checkCol(self, col, row) -> bool:
        player_piece = ' '
        if self.H == 1:
            player_piece = 'O'
        elif self.H == 0:
            player_piece = 'X'
        row_counter = row
        counter = 1
        #check below piece
        while row_counter < self.N - 1:
            row_counter += 1
            if player_piece == self.board[row_counter][col]:
                counter += 1
            else:
                break
        if self.M <= counter:
            return True
        else:
            return False

    def enumBoard(self):
        rows_adv = self.enumRows()
        self.enumDiags(rows_adv[4])

    #returns player row advantage, computer row advantage, number of threats each has in the rows, and depth of placed pieces
    #player and computer advantage are calculated using the number of pieces in a row, the number of pieces available to make a win and spatial analysis
    def enumRows(self) -> tuple:
        # computer advantage
        comp_adv = 0
        # counts number of player threats
        player_threats = 0
        # counts number of player pieces in a row
        player_pieces = 0
        # player advantage
        player_adv = 0
        # keeps track of if row is empty
        encountered = False
        # highest row with pieces
        depth = self.N

        for i in range(self.N - 1, -1, -1):
            row = self.board[i]
            # counts number of consecutive pieces and pushes it onto queue when consecutive pieces stops
            row_list = deque()
            # counts spatial analysis of pieces
            gauss_list = deque()
            # counts computer gauss analysis
            comp_gauss = 0
            # counts player gauss analysis
            player_gauss = 0
            # counts number of computer threats
            computer_threats = 0
            # counts number of computer pieces in a row
            computer_pieces = 0

            # form row_list
            for j in range(self.N):
                value = row[j]
                if value == 'X':
                    encountered = True
                    if computer_pieces != 0:
                        row_list.append(computer_pieces)
                        computer_pieces = 0
                        player_pieces -= 1
                        gauss_list.append(comp_gauss)
                        comp_gauss = 0
                        player_gauss -= Board.gaussian_board[i][j]
                    else:
                        player_pieces -= 1
                        player_gauss -= Board.gaussian_board[i][j]
                elif value == 'O':
                    encountered = True
                    if player_pieces != 0:
                        row_list.append(player_pieces)
                        player_pieces = 0
                        computer_pieces += 1
                        gauss_list.append(player_gauss)
                        player_gauss = 0
                        comp_gauss += Board.gaussian_board[i][j]
                    else:
                        computer_pieces += 1
                        comp_gauss += Board.gaussian_board[i][j]
                elif value == ' ':
                    if player_pieces != 0:
                        row_list.append(player_pieces)
                        player_pieces = 0
                        gauss_list.append(player_gauss)
                        player_gauss = 0
                    if computer_pieces != 0:
                        row_list.append(computer_pieces)
                        computer_pieces = 0
                        gauss_list.append(comp_gauss)
                        comp_gauss = 0
                    row_list.append(0)
                    gauss_list.append(0)

            # if no pieces encountered break
            if not encountered:
                break
            else:
                depth -= 1
                encountered = False

            # ensure pieces at end of board are in deque
            if player_pieces != 0:
                row_list.append(player_pieces)
                player_pieces = 0
                gauss_list.append(player_gauss)
                player_gauss = 0
            if computer_pieces != 0:
                row_list.append(computer_pieces)
                computer_pieces = 0
                gauss_list.append(comp_gauss)
                comp_gauss = 0

            # check for threats
            for k in range(len(row_list)):
                # if last index do nothing
                if k == len(row_list) - 1:
                    pass
                # if second to last index
                elif k == len(row_list) - 2:
                    if row_list[k + 1] == 0:
                        if row_list[k] > 0 and row_list[k] + 1 == self.M:
                            computer_threats += 1
                        elif row_list[k] < 0 and abs(row_list[k] - 1) == self.M:
                            player_threats += 1
                    #check later
                    elif row_list[k] == 0:
                        if row_list[k + 1] > 0 and row_list[k + 1] + 1 >= self.M:
                            computer_threats += 1
                        elif row_list[k + 1] < 0 and abs(row_list[k + 1] - 1) >= self.M:
                            player_threats += 1
                # if not second to last or last index
                else:
                    if row_list[k + 1] == 0 and abs(row_list[k] + row_list[k + 2]) >= self.M:
                        if row_list[k] > 0:
                            computer_threats += 1
                        else:
                            player_threats += 1

            # get row enumeration val
            row_enum = self.enumRowHelper(row_list, gauss_list)
            comp_adv += row_enum[0]
            player_adv += row_enum[1]

        return (comp_adv, computer_threats, player_adv, player_threats, depth)


    def enumRowHelper(self, row_list, gauss_list) -> tuple:
        #temporary variable to store number of pieces found
        pieces = 0
        #temporary variable to store consecutive advantage
        adv = 0
        #temporary variable to store consecutive zeros
        zeros = 0
        #overall computer advantage
        computer_pieces = 0
        #overallplayer advantage
        player_pieces = 0
        #count computer advantage
        for i in range(len(row_list)):
            if row_list[i] == 0:
                zeros += 1
            elif row_list[i] > 0:
                pieces += row_list[i]
                adv += self.signedPower20(row_list[i]) * (1 + abs(gauss_list[i]))
            else:
                if pieces > 0:
                    if pieces + zeros >= self.M: 
                        computer_pieces += adv + (zeros * .2)
                pieces = 0
                adv = 0
                zeros = 0
            if i == len(row_list) - 1:
                if pieces > 0:
                    if pieces + zeros >= self.M: 
                        computer_pieces += adv + (zeros * .2)
                pieces = 0
                adv = 0
                zeros = 0

        # count player advantage
        for i in range(len(row_list)):
            if row_list[i] == 0:
                zeros += 1
            elif row_list[i] < 0:
                pieces += row_list[i]
                adv += self.signedPower20(row_list[i]) * (1 + abs(gauss_list[i]))
            else: 
                if pieces < 0:
                    if abs(pieces - zeros) >= self.M: 
                        player_pieces += adv - (zeros * .2)
                pieces = 0
                adv = 0
                zeros = 0
            if i == len(row_list) - 1:
                if pieces < 0:
                    if abs(pieces - zeros) >= self.M:
                        player_pieces += adv - (zeros * .2)
                pieces = 0
                adv = 0
                zeros = 0

        return (computer_pieces, player_pieces)

    def signedPower20(self, n):
        sign = math.copysign(1, n)
        return sign * (abs(n) ** 2)

    def enumCols(self) -> tuple:
        #keeps track of overall computer adv for all rows
        comp_adv = 0
        #keeps track of overall player adv for all rows
        player_adv = 0
        #keeps track of computer threats
        comp_threats = 0
        #keeps track of player threats 
        player_threats = 0
        #keeps track of spacial weights for consecutive pieces
        gaussian_weight = 0
        for col in range(self.N):
            #index for iterating through rows
            row_index = self.board_cols[col]
            #available spaces above piece
            spaces = row_index
            #counter used for each column
            col_counter = 0
            if row_index < self.N:
                if self.board[row_index][col] == 'X':
                    col_counter = -1
                    gaussian_weight += Board.gaussian_board[row_index][col]
                elif self.board[row_index][col] == 'O':
                    col_counter = 1
                    gaussian_weight += Board.gaussian_board[row_index][col]
                row_index += 1

            while row_index < self.N:
                if self.board[row_index][col] == 'X':
                    #if player pieces ontop
                    if col_counter < 0:
                        col_counter -= 1
                        gaussian_weight += Board.gaussian_board[row_index][col]
                    #if computer pieces ontop
                    elif col_counter > 0:
                        break
                elif self.board[row_index][col] == 'O':
                    #if player pieces ontop
                    if col_counter < 0:
                        break
                    #if computer pieces ontop
                    if col_counter > 0:
                        col_counter += 1
                        gaussian_weight += Board.gaussian_board[row_index][col]
                row_index += 1
            
            #check for threats and add advantages if possibility of winning in column
            if col_counter < 0:
                if abs(col_counter) + 1 >= self.M:
                    player_threats += 1
                if abs(col_counter) + spaces >= self.M:
                    player_adv += self.signedPower20(col_counter) * (1 + gaussian_weight)
            elif col_counter > 0:
                if col_counter + 1 >= self.M:
                    comp_threats += 1
                if col_counter + spaces >= self.M:
                    comp_adv += self.signedPower20(col_counter) * (1 + gaussian_weight)
            
            gaussian_weight = 0
            col_counter = 0
        return (comp_adv, comp_threats, player_adv, player_threats)

    def enumDiags(self, depth) -> tuple:
        print(self.enumDiagRight(0, 6))
        return (0, 0)
    
    def enumDiagRight(self, col, row) -> tuple:
        col_index = col
        row_index = row
        diag_list = deque()
        gauss_list = deque()
        counter = 0
        gauss_counter = 0
        while col_index < self.N and row_index >= 0:
            #if spot is empty
            if self.board[row_index][col_index] == ' ':
                #if player or computer pieces have been counted
                if counter != 0:
                    diag_list.append(counter)
                    gauss_list.append(gauss_counter)
                diag_list.append(0)
                gauss_list.append(0)
                counter = 0
                gauss_counter = 0
            #if spot is player
            elif self.board[row_index][col_index] == 'X':
                #if computer pieces below
                if counter > 0:
                    diag_list.append(counter)
                    gauss_list.append(gauss_counter)
                    counter = -1
                    gauss_counter = -1 * Board.gaussian_board[row_index][col_index]
                else:
                    counter -= 1
                    gauss_counter -= Board.gaussian_board[row_index][col_index]
            elif self.board[row_index][col_index] == 'O':
                #if player pieces below
                if counter < 0:
                    diag_list.append(counter)
                    gauss_list.append(gauss_counter)
                    counter = 1
                    gauss_counter = Board.gaussian_board[row_index][col_index]
                else:
                    counter += 1
                    gauss_counter += Board.gaussian_board[row_index][col_index]
            col_index += 1
            row_index -= 1

        if counter != 0:
            diag_list.append(counter)
            gauss_list.append(gauss_counter)
        return self.enumDiagHelper(diag_list, gauss_list)

    #col_index -= 1 row_index -= 1 col_index >= 0 and row_index >= depth

    def enumDiagLeft(self, col, row) -> tuple:
        col_index = col
        row_index = row
        diag_list = deque()
        gauss_list = deque()
        counter = 0
        gauss_counter = 0
        while col_index < self.N and row_index >= 0:
            #if spot is empty
            if self.board[row_index][col_index] == ' ':
                #if player or computer pieces have been counted
                if counter != 0:
                    diag_list.append(counter)
                    gauss_list.append(gauss_counter)
                diag_list.append(0)
                gauss_list.append(0)
                counter = 0
                gauss_counter = 0
            #if spot is player
            elif self.board[row_index][col_index] == 'X':
                #if computer pieces below
                if counter > 0:
                    diag_list.append(counter)
                    gauss_list.append(gauss_counter)
                    counter = -1
                    gauss_counter = -1 * Board.gaussian_board[row_index][col_index]
                else:
                    counter -= 1
                    gauss_counter -= Board.gaussian_board[row_index][col_index]
            elif self.board[row_index][col_index] == 'O':
                #if player pieces below
                if counter < 0:
                    diag_list.append(counter)
                    gauss_list.append(gauss_counter)
                    counter = 1
                    gauss_counter = Board.gaussian_board[row_index][col_index]
                else:
                    counter += 1
                    gauss_counter += Board.gaussian_board[row_index][col_index]
            col_index += 1
            row_index -= 1

        if counter != 0:
            diag_list.append(counter)
            gauss_list.append(gauss_counter)
        return self.enumDiagHelper(diag_list, gauss_list)
 
    def enumDiagHelper(self, diag_list, gauss_list) -> tuple:
        print(diag_list)
        print(gauss_list)
        comp_adv = 0
        player_adv = 0
        comp_threats = 0
        player_threats = 0
        zeros = 0
        counter = 0
        adv = 0
        #count player and computer threats
        for k in range(len(diag_list)):
            # if last index do nothing
            if k == len(diag_list) - 1:
                pass
            # if second to last index
            elif k == len(diag_list) - 2:
                if diag_list[k + 1] == 0:
                    if diag_list[k] > 0 and diag_list[k] + 1 >= self.M:
                        comp_threats += 1
                    elif diag_list[k] < 0 and abs(diag_list[k] - 1) >= self.M:
                        player_threats += 1
                elif diag_list[k] == 0:
                    if diag_list[k + 1] > 0 and diag_list[k + 1] + 1 >= self.M:
                        comp_threats += 1
                    elif diag_list[k + 1] < 0 and abs(diag_list[k + 1] - 1) >= self.M:
                        player_threats += 1
            # if not second to last or last index
            else:
                if diag_list[k + 1] == 0 and abs(diag_list[k] + diag_list[k + 2]) >= self.M:
                    if diag_list[k] > 0:
                        comp_threats += 1
                    else:
                        player_threats += 1

        #check player adv
        for i in range(len(diag_list)):
            #if row of player pieces
            if diag_list[i] < 0:
                counter += diag_list[i]
                adv += self.signedPower20(diag_list[i]) * (1 + abs(gauss_list[i]))
            #if row of computer pieces
            elif diag_list[i] > 0:
                #if row of player pieces below
                if counter < 0:
                    if abs(counter) + zeros >= self.M:
                        player_adv += adv
                counter = 0
                zeros = 0
                adv = 0
            #if a zero
            elif diag_list[i] == 0:
                zeros += 1
        if counter < 0:
            if abs(counter) + zeros >= self.M:
                player_adv += adv
        counter = 0
        zeros = 0
        adv = 0
        for i in range(len(diag_list)):
            #if row of computer pieces
            if diag_list[i] > 0:
                counter += diag_list[i]
                adv += self.signedPower20(diag_list[i]) * (1 + gauss_list[i])
            #if row of player pieces
            elif diag_list[i] < 0:
                #if row of computer pieces below
                if counter > 0:
                    if counter + zeros >= self.M:
                        comp_adv += adv
                    counter = 0
                    zeros = 0
                    adv = 0
            #if a zero
            elif diag_list[i] == 0:
                zeros += 1
        if counter > 0:
            if counter + zeros >= self.M:
                comp_adv += adv
        counter = 0
        zeros = 0
        adv = 0


        return (comp_adv, comp_threats, player_adv, player_threats)

    def numDiagsRight(self, row, col):
        min(row, self.N - col - 1)
    
    def numDiagsLeft(self, row, col):
        min(row, col)


            
        
        
                            

            

                
                    

    

     
        
    
            


            

        

        
    
   