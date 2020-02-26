#
#FILE PURPOSE:
#  1. This file contains all class definitions and functions that instantiate one of
#  the created classes.

#BUG SECTION:
#  1. showing a tile needs to have a point at the top, not an edge
# */

#/* Requirements and Exports */

# need to give players an id, use first letter of not conflicting colors (NOT BLWSO)
# Red, Yellow, Purple, Green, Cyan, Tan
class Player:
    def __init__(self, name, color):
        self.p_name = name
        self.p_hand = [] # should be a list of characters
        self.p_color = color # Red, Yellow, Purple, Green, Cyan, Tan
        self.p_victory_pts = 0
        self.p_dev_cards = []

    def present(self):
        print(self.p_name)

    def show_hand(self):
        print(''.join(self.p_hand))

    #def add_card(self, new_card):
    #    self.p_hand += new_card

	#returns how many victory points a player has
    def show_victory_pts(self):
        return self.p_victory_pts

    def calculate_victory_pts(self):
<<<<<<< HEAD
        pass # needs to be implemented
=======
        pass
>>>>>>> 3da4862f5003a3ea50e18762cb9730b18a19ae1d

#Partial implementation

class Board:
    def __init__(self):
        self.tiles = [] #Is a list of tiles

<<<<<<< HEAD
=======
    def create_board(self):
        for i in range(1,20):
            randomize = random_tile()
            self.tiles.append(Tile(randomize[0], randomize[1], i))

    def show_board(self):
        to_print = '''
                                  >-----<
                                 /~~~~~~~\\
                                /~~~~~~~~~\\
                         >-----<~~~~3:1~~~~>-----<
                        /~~~~~~~\~~~~~~~~~/~~~~~~~\\
                       /~~~~~~~~~\*~~~~~*/~~~~~~~~~\\
                >-----<~~~~~~~~~~~{57}-----<~~~~~~~~~~~>-----<
               /~~~~~~~\~~~~~~~~~/       \~~~~~~~~~/~~~~~~~\\
              /~~~2:1~~~\~~~~~~~/    {0}    \~~~~~~~/~~~2:1~~~\\
       >-----<~~~wood~~~*>-----<     {1}     >-----<*~~sheep~~~>-----<
      /~~~~~~~\~~~~~~~~~/       \    {2}    /       \~~~~~~~~~/~~~~~~~\\
     /~~~~~~~~~\~~~~~~*/    {3}    \       /    {4}    \*~~~~~~/~~~~~~~~~\\
    <~~~~~~~~~~~>-----<     {5}     >-----<     {6}     >-----<~~~~~~~~~~~>
     \~~~~~~~~~/       \    {7}    /       \    {8}    /       \~~~~~~~~~/
      \~~~~~~~/    {9}    \       /    {10}    \       /    {11}    \~~~~~~~/
       >-----<     {12}     >-----<     {13}     >-----<     {14}     >-----<
      /~~~~~~~\    {15}    /       \    {16}    /       \    {17}    /~~~~~~~\\
     /~~~2:1~~~\       /    {18}    \       /    {19}    \       /~~~2:1~~~\\
    <~~~brick~~*>-----<     {20}     >-----<     {21}     >-----<*~~~ore~~~~>
     \~~~~~~~~~/       \    {22}    /       \    {23}    /       \~~~~~~~~~/
      \~~~~~~*/    {24}    \       /    {25}    \       /    {26}    \*~~~~~~/
       >-----<     {27}     >-----<     {28}     >-----<     {29}     >-----<
      /~~~~~~~\    {30}    /       \    {31}    /       \    {32}    /~~~~~~~\\
     /~~~~~~~~~\       /    {33}    \       /    {34}    \       /~~~~~~~~~\\
    <~~~~~~~~~~~>-----<     {35}     >-----<     {36}     >-----<~~~~~~~~~~~>
     \~~~~~~~~~/       \    {37}    /       \    {38}    /       \~~~~~~~~~/
      \~~~~~~~/    {39}    \       /    {40}    \       /    {41}    \~~~~~~~/
       >-----<     {42}     >-----<     {43}     >-----<     {44}     >-----<
      /~~~~~~*\    {45}    /       \    {46}    /       \    {47}    /*~~~~~~\\
     /~~~~~~~~~\       /    {48}    \       /    {49}    \       /~~~~~~~~~\\
    <~~~~3:1~~~*>-----<     {50}     >-----<     {51}     >-----<*~~~3:1~~~~>
     \~~~~~~~~~/~~~~~~~\    {52}    /       \    {53}    /~~~~~~~\~~~~~~~~~/
      \~~~~~~~/~~~~~~~~~\       /    {54}    \       /~~~~~~~~~\~~~~~~~/
       >-----< ~~~~~~~~~~>-----<     {55}     >-----<~~~~~~~~~~~>-----<
              \~~~~~~~~~/*~~~~~*\    {56}    /*~~~~~*\~~~~~~~~~/
               \~~~~~~~/~~~~~~~~~\       /~~~2:1~~~\~~~~~~~/
                >-----<~~~~3:1~~~~>-----<~~~grain~~~>-----<
                       \~~~~~~~~~/~~~~~~~\~~~~~~~~~/
                        \~~~~~~~/~~~~~~~~~\~~~~~~~/
                         >-----<~~~~~~~~~~~>-----<
                                \~~~~~~~~~/
                                 \~~~~~~~/
                                  >-----<

                                  '''.format(self.tiles[2].number,self.tiles[2].resource,self.tiles[2].id,self.tiles[1].number,
                                  self.tiles[6].number,self.tiles[1].resource,self.tiles[6].resource,self.tiles[1].id, self.tiles[6].id
                                  ,self.tiles[0].number,self.tiles[5].number,self.tiles[11].number, self.tiles[0].resource,
                                  self.tiles[5].resource,self.tiles[11].resource,self.tiles[0].id,self.tiles[5].id,self.tiles[11].id,
                                  self.tiles[4].number,self.tiles[10].number,self.tiles[4].resource,self.tiles[10].resource,
                                  self.tiles[4].id,self.tiles[10].id,self.tiles[3].number,self.tiles[9].number,self.tiles[15].number,
                                  self.tiles[3].resource,self.tiles[9].resource,self.tiles[15].resource,self.tiles[3].id,
                                  self.tiles[9].id,self.tiles[15].id,self.tiles[8].number,self.tiles[14].number,self.tiles[8].resource
                                  ,self.tiles[14].resource,self.tiles[8].id,self.tiles[14].id,self.tiles[7].number,self.tiles[13].number
                                  ,self.tiles[18].number,self.tiles[7].resource,self.tiles[13].resource,self.tiles[18].resource,
                                  self.tiles[7].id,self.tiles[13].id,self.tiles[18].id,self.tiles[12].number,self.tiles[17].number,
                                  self.tiles[12].resource,self.tiles[17].resource,self.tiles[12].id,self.tiles[17].id,
                                  self.tiles[16].number,self.tiles[16].resource,self.tiles[16].id,config.node_list[5].owns_node)

        print(to_print)

>>>>>>> 2cdae5502c90522f56d127b83f310371c3465c7d
class Tile:

    def __init__(self, resource, number, id):
        self.resource = resource
        self.number = number
        self.id = id

class Robber:

    def __init__(self, first_tile):
        self.on_tile = first_tile

#Need to finish present method in tile class
#print(rand_tile.present());

#print_roads(roads)
