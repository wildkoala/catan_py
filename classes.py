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

#import catan_py.py

class Player:

  def __init__(self, name):
    self.p_name = name
    self.p_hand = []
    self.p_color = ""
    self.p_victory_pts = 0
    self.p_dev_cards = []

  def present(self):
    print("My name is " + self.p_name)

  def show_hand(self):
    for i in range(0, len(self.p_hand)):
      self.p_hand[i].present()

  def add_card(self, new_card):
    self.p_hand.push(new_card)
  
	#returns how many victory points a player has
  def show_victory_pts(self):
    return self.p_victory_pts

'''

class Card {
  constructor(resource) {
    this.resource = resource;
  }
  present() {
    console.log("Resource: " + this.resource);
  }
}

// Partial implementation
class Board {
  constructor(size) {
    this.size = size;
  }
  present() {
    console.log("This board is " + this.size + " tiles large");
  }
}

class Tile {
  constructor(resource, number) {
    this.resource = resource;
    this.number = number;
  }
  present() {
    const format = `   _____
  /     \\ 
 /       \\ 
(    ` + this.resource + `    )
 \\   ` + this.number + `   /
  \\_____/`;
    return format;
  }
}

function random_tile(){
  var tile_r;
  var tile_n;

  // Determine the resource
  var x = Math.floor((Math.random() * 5) + 1); // gives random number between 1 and 5
  if (x == 1){
    tile_r = "O";
  }
  if (x == 2){
    tile_r = "W";
  }
  if (x == 3){
    tile_r = "B";
  }
  if (x == 4){
    tile_r = "L";
  }
  if (x == 5){
    tile_r = "S";
  }

  // Determine the number, 7's not allowed
  tile_n = game.roll_dice(); 
  while(tile_n == 7){
    tile_n = game.roll_dice();
  }
  rand_tile = new Tile(tile_r, tile_n);
  //return rand_tile;
  console.log(rand_tile.present());
}
'''
