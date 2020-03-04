import random

class Board:
    def __init__(self):
        with open("board.txt",'r') as fp:
            self.board_format = fp.read()

    def __str__(self):
        boardstr = ""
        boardstr += self.board_format
        boardstr=boardstr.replace("%n()%",'.')
        boardstr=boardstr.replace("%r()%",'.')
        for i in range(1,20):
            boardstr=boardstr.replace("%t("+str(i)+")num%",str(int(random.random()*8)))
            boardstr=boardstr.replace("%t("+str(i)+")res%",'B')
        return boardstr


if __name__=='__main__':
    b = Board()
    print(b)