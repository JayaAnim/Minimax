class Board:
    def __init__(self, N, M, H):
        #N is number of cols/rows in n x n grid
        #M is number of disks to connect contiguously 
        #H is who makes the first move (1 = computer, 0 = human)
        print(N, M, H)

        self.N = N
        while self.N < 3 or self.N > 10:
            print('Error: invalid board size')
            print('Parameters (3 <= N <= 10)')
            self.N = int(input('Please enter a new board size: '))

        self.M = M
        while self.M <= 1 or self.M > N:
            print('Error: invalid disks value')
            print('Parameters (1 < M <= N)')
            self.M = int(input('Please enter a new disk value: '))
        
        self.H = H
        while self.H != 0 and self.H != 1:
            print('Error: invalid starting player')
            print('Parameters (H == 1 or H == 0)')
            self.H = int(input('Please enter a new starting player: '))

        self.createBoards()
        self.startGame()

    def createBoards(self):
        self.board = [[' ' for j in range(self.N)] for i in range(self.N)]
        self.value_board = [[0 for j in range(self.N)] for i in range(self.N)]
        self.board_eval = 0
        self.game_over = False
    
    def printBoard(self):
        print(self.board)
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

    def startGame(self):
        while not self.game_over:
            self.printEvaluation()
            #Users turn
            if self.H == 0:
                self.printBoard()
                self.turn = int(input('Please enter the column (int) for your move: '))
                self.check_move()
                self.place_move()
            #Computers turn
            elif self.H == 1:
                print('hi')
            #error
            else:
                print('User variable H error: ending game')
                self.game_over = True
                return

    def check_move(self):
        while self.turn < 1 or self.turn > self.N or self.board[0][self.turn - 1] != ' ':
            self.turn = int(input('That is an invalid column please try again: '))
    
    def place_move(self):
        #testing if it work, Tri Pham
        print("place move")

    #make value board
    def boardEvalutation(self):
        #produce board for evaluation
        mid = self.N//2
        for i in range(self.N):
            for j in range(self.N):
                self.value_board[i][j] = (self.M - abs(i-mid)) + (self.M - abs(j-mid))
        
    #print value board
    def printEvaluation(self):
        self.boardEvalutation()
        print("Value board")
        for i in self.value_board:
            for g in i:
                print("{:>3}".format(g), end="")
            print()            
        
    
            


            

        

        
    
   