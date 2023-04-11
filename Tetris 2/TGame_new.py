import copy
import random
import rotate_matrix

class Tetris(object):
    Figures = [
        [[1,1,1,1],[0,1,2,3],4],#I  0
        [[0,0,1,1],[0,1,0,1],2],#o  1
        [[0,0,1,2],[0,1,1,1],3],#l  2
        [[0,1,2,2],[1,1,1,0],3],#rl 3
        [[0,1,1,2],[0,0,1,1],3],#s  4
        [[0,1,1,2],[1,1,0,0],3],#rs 5
        [[0,1,1,1],[1,0,1,2],3] #t   6
        ]

    figposx = 0
    figposy = 4

    def __init__(self, _height, _width, _score = 0):
        self.height = _height
        self.width = _width
        self.state = "Start"
        self.score = _score
        self.field_empty = []
        self.field = []
        self.score = _score

        for i in range(_height):
            new_line = []
            for j in range(_width):
                new_line.append(0)
            self.field_empty.append(new_line)
        self.wipe()

    def wipe(self):
        self.field = copy.deepcopy(self.field_empty)
        self.create_block()
        self.score = 0

    def get_view(self):
        tmp =  copy.deepcopy(self.field)
        r = 0
        for row in self.figure:
            col=0
            for value in row:
                if value != 0:
                    tmp[r+self.figposx][col+self.figposy]=value
                col= col + 1
            r=r+1
        return tmp

    def add_figure(self):
        r = 0
        for row in self.figure:
            col=0
            for value in row:
                if value != 0:
                    self.field[r+self.figposx][col+self.figposy]=value
                col= col + 1
            r=r+1

    def create_block(self):
        self.figposx = 0
        self.figposy = 4
        self.figure = []
        self.dings = random.randint(0,len(self.Figures)-1)
        fig_tmp = self.Figures[self.dings]
        self.lenght = fig_tmp[2]
        for i in range(self.lenght):
            new_line = []
            for j in range(self.lenght):
                new_line.append(0)
            self.figure.append(new_line)
        for i in range(4):
            x = fig_tmp[0][i]
            y = fig_tmp[1][i]
            self.figure[x][y] = self.dings+1

    def Collision(self):
        r = 0
        for row in self.figure:
            col=0
            for value in row:
                if value != 0:
                    if col+self.figposy >= self.width:
                        self.shift_left()
                        self.Collision()
                    if col+self.figposy < 0:
                        self.shift_right()
                        self.Collision()
                    if r+self.figposx >= self.height:
                        return True
                    if self.field[r+self.figposx][col+self.figposy] != 0:
                        return True
                col= col + 1
            r=r+1  
        return False

    def turn_block(self):
        self.figure = rotate_matrix.clockwise(self.figure)
        self.Collision()

    def shift_left(self):
        self.figposy -= 1
        if self.Collision():
            self.figposy +=1

    def shift_right(self):
        self.figposy += 1
        if self.Collision():
            self.figposy -=1

    def shift_down(self):
        self.figposx += 1
        while self.Collision():
            self.figposx -= 1

    def shift_up(self):
        self.figposx -= 1

    def check_rows(self):
        del_line = 0       
        for i in range(self.height-1,0,-1):
            blockcount = 0
            i=i+del_line
            if del_line != 0:
                if i-del_line>=0:
                    self.field[i]=self.field[i-del_line].copy()
                else:
                     for count in range(self.width):
                         self.field[i][count]=0
            for j in range(self.width):
                if self.field[i][j]!=0:
                    blockcount+=1
                if blockcount == self.width:
                    del_line += 1
        self.score += del_line * self.width
        if del_line == 4:
            self.score += self.width
        return del_line

    def game_step(self):
        self.figposx += 1
        if self.Collision():
            self.figposx -= 1
            self.add_figure()
            self.check_rows()
            if self.figposx <= 0:
                return True
            self.create_block()
        return False

    def AI_step(self, action):
        if action == [1,0,0,0]:
            self.shift_left()
        if action == [0,1,0,0]:
            self.turn_block()
        if action == [0,0,1,0]:
            self.shift_right()
        reward = 0
        done = self.game_step()
        score = self.score
        return reward, done, score
   


         

