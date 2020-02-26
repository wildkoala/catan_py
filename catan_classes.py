#
#FILE PURPOSE:
#  1. This file contains all class definitions and functions that instantiate one of
#  the created classes.

#BUG SECTION:
#  1. showing a tile needs to have a point at the top, not an edge
# */

#/* Requirements and Exports */
import random


def roll_dice():
    x = random.randint(1, 6)
    y = random.randint(1, 6)
    return x + y

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

    def remove_cards(self, cards):
        pass





#Partial implementation
class Board:

    def __init__(self):
        self.tiles = [] #Is a list of tiles

    def create_board(self):
        for i in range(1,20):
            randomize = random_tile()
            self.tiles.append(Tile(randomize[0], randomize[1], i))

    def show_board(self):
        print('''
                                  >-----<
                                 /~~~~~~~\\
                                /~~~~~~~~~\\
                         >-----<~~~~3:1~~~~>-----<
                        /~~~~~~~\~~~~~~~~~/~~~~~~~\\
                       /~~~~~~~~~\*~~~~~*/~~~~~~~~~\\
                >-----<~~~~~~~~~~~>-----<~~~~~~~~~~~>-----<
               /~~~~~~~\~~~~~~~~~/       \~~~~~~~~~/~~~~~~~\\
              /~~~2:1~~~\~~~~~~~/    {}    \~~~~~~~/~~~2:1~~~\\
       >-----<~~~wood~~~*>-----<     {}     >-----<*~~sheep~~~>-----<
      /~~~~~~~\~~~~~~~~~/       \    {}    /       \~~~~~~~~~/~~~~~~~\\
     /~~~~~~~~~\~~~~~~*/    {}    \       /    {}    \*~~~~~~/~~~~~~~~~\\
    <~~~~~~~~~~~>-----<     {}     >-----<     {}     >-----<~~~~~~~~~~~>
     \~~~~~~~~~/       \    {}    /       \    {}    /       \~~~~~~~~~/
      \~~~~~~~/    {}    \       /    {}    \       /    {}    \~~~~~~~/
       >-----<     {}     >-----<     {}     >-----<     {}     >-----<
      /~~~~~~~\    {}    /       \    {}    /       \    {}    /~~~~~~~\\
     /~~~2:1~~~\       /    {}    \       /    {}    \       /~~~2:1~~~\\
    <~~~brick~~*>-----<     {}     >-----<     {}     >-----<*~~~ore~~~~>
     \~~~~~~~~~/       \    {}    /       \    {}    /       \~~~~~~~~~/
      \~~~~~~*/    {}    \       /    {}    \       /    {}    \*~~~~~~/
       >-----<     {}     >-----<     {}     >-----<     {}     >-----<
      /~~~~~~~\    {}    /       \    {}    /       \    {}    /~~~~~~~\\
     /~~~~~~~~~\       /    {}    \       /    {}    \       /~~~~~~~~~\\
    <~~~~~~~~~~~>-----<     {}     >-----<     {}     >-----<~~~~~~~~~~~>
     \~~~~~~~~~/       \    {}    /       \    {}    /       \~~~~~~~~~/
      \~~~~~~~/    {}    \       /    {}    \       /    {}    \~~~~~~~/
       >-----<     {}     >-----<     {}     >-----<     {}     >-----<
      /~~~~~~*\    {}    /       \    {}    /       \    {}    /*~~~~~~\\
     /~~~~~~~~~\       /    {}    \       /    {}    \       /~~~~~~~~~\\
    <~~~~3:1~~~*>-----<     {}     >-----<     {}     >-----<*~~~3:1~~~~>
     \~~~~~~~~~/~~~~~~~\    {}    /       \    {}    /~~~~~~~\~~~~~~~~~/
      \~~~~~~~/~~~~~~~~~\       /    {}    \       /~~~~~~~~~\~~~~~~~/
       >-----< ~~~~~~~~~~>-----<     {}     >-----<~~~~~~~~~~~>-----<
              \~~~~~~~~~/*~~~~~*\    {}    /*~~~~~*\~~~~~~~~~/
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
                                  self.tiles[16].number,self.tiles[16].resource,self.tiles[16].id))


class Tile:

    def __init__(self, resource, number, id):
        self.resource = resource
        self.number = number
        self.id = id
        self.has_robber = False

#Need to look up proper syntax to create this format in python
'''
  def present(self):
    const format = `   _____
  /     \\
 /       \\
(    ` + this.resource + `    )
 \\   ` + this.number + `   /
  \\_____/`

    return format;
'''
def random_tile():
    tile_r = ""
    tile_n = -1

    #Determine the resource
    x = random.randint(1, 5)  #gives random number between 1 and 5
    if (x == 1):
        tile_r = "O"
    elif (x == 2):
        tile_r = "W"
    elif (x == 3):
        tile_r = "B"
    elif (x == 4):
        tile_r = "L"
    elif (x == 5):
        tile_r = "S"

#Determine the number, 7's not allowed
    tile_n = roll_dice()
    while(tile_n == 7):
        tile_n = roll_dice()
        rand_tile = [tile_r, tile_n]
    rand_tile = [tile_r, tile_n]
    return rand_tile
#Need to finish present method in tile class
#print(rand_tile.present());


class Road:
    def __init__(self, start_n, end_n):
        self.owns_road = ""
        self.start_n = start_n # id of starting node
        self.end_n = end_n # id of ending node

    def is_owned(self):
        if self.owns_node == "":
            return False
        else:
            return True

    def __str__(self):
        return "Road: " + str(str(self.start_n) + " " +  str(self.end_n))

class Node:
    def __init__(self, id): # Just gonna have every node have an id.
        self.id = id
        self.owns_node = "" # color of player with a settlement or city on this node
        self.alias = [] # this is a list of tuples, where the first vvalue is the tile it's on, and the second is the corner that it is.
        self.can_place = False # basically, this is only true in limited circumstances
        self.adj_nodes = [] # list of id's for connected nodes

    def is_empty(self):
        if self.owns_node == "":
            return True
        else:
            return False

    def add_adj(self, id):
        self.adj_nodes.append(id)

    def is_settlement(self):
        if self.owns_node.islower():
            return True
        else:
            return False

    def is_city(self):
        if self.owns_node.isupper():
            return True
        else:
            return False

    def __str__(self):
        return "Node: " + str(self.id)


def print_nodes(node_list):
	for n in node_list:
		print(n)


def print_roads(road_list):
    for r in road_list:
        print(r)


#print_roads(roads)
