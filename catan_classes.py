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
