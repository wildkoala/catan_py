#
#FILE PURPOSE: 
#  1. This file contains all class definitions and functions that instantiate one of
#  the created classes.

#BUG SECTION: 
#  1. showing a tile needs to have a point at the top, not an edge
# */

#/* Requirements and Exports */
#Fuck this shit
#var game = require('./catan_js.js');
import catan_py
import random;

class Player:

  def __init__(self, name):
    self.p_name = name
    self.p_hand = [] # this is a list of cards
    self.p_color = ""
    self.p_victory_pts = 0
    self.p_dev_cards = []

  def present(self):
    print("My name is " + self.p_name)

  def show_hand(self):
    for i in range(0, len(self.p_hand)):
      print("Resource: " + self.p_hand[i].resource)

  def add_card(self, new_card):
    self.p_hand.insert(len(self.p_hand), new_card)
  
	#returns how many victory points a player has
  def show_victory_pts(self):
    return self.p_victory_pts


class Card:
  def __init__(self, resource):
    self.resource = resource

  def present(self):
    print("Resource: " + self.resource)




#Partial implementation
class Board:
  def __init__(self, size):
    self.size = size

  def present(self):
    print("This board is " + self.size + " tiles large")
 


class Tile:
  def __init__(self, resource, number):
    self.resource = resource;
    self.number = number;

#Need to look up proper syntax to create this format in python
  '''def present(self):
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
  x = random.randint(1, 6)  #gives random number between 1 and 5
  if (x == 1):
    tile_r = "O"
  if (x == 2):
    tile_r = "W"
  if (x == 3):
    tile_r = "B"
  if (x == 4):
    tile_r = "L"
  if (x == 5):
    tile_r = "S"

  #Determine the number, 7's not allowed
  tile_n = game.roll_dice()
  while(tile_n == 7):
    tile_n = game.roll_dice()
  rand_tile = Tile(tile_r, tile_n)
  return rand_tile;
  #Need to finish present method in tile class
  #print(rand_tile.present());

