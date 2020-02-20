#========================================================
# FILE PURPOSE: 
#   - This file contains all functions necessary to create a new "physical" item in catan
#========================================================

# POSSIBLE RESOURCES: Ore, Wheat, Brick, Lumber, Sheep

#========================================================
# Requirements and Exports
#========================================================

#========================================================
# FUNCTION DEFINITIONS
#========================================================

# partially implemented
def build_road(a_player):
  have_resources = has_needed_resources("road", a_player)
  if have_resources:
    console.log("building a road")
  
  else:
    console.log("Not enough resources to build a road!!")
  
  # Space is open
  # It's connected to another road or settlement

# partially implemented
# the intial setup will probably not work with this function.

def build_settlement(a_player):
  have_resources = has_needed_resources("settlement", a_player)
  if (have_resources):
    print("building a settlement")
  else:
    print("Not enough resources to build a settlement!!")

  # Space is open
  # no one is on an adjacent territory


# partially implemented
def build_city(a_player):
  have_resources = has_needed_resources("city", a_player)
  if have_resources:
    print("building a city")
  
  else:
    print("Not enough resources to upgrade into a city!!") 
  # Have a settlement
  # It is a settlement, and not anything else


# partially implemented
def build_dev_card(a_player):
  have_resources = has_needed_resources("dev_card", a_player)
  if have_resources:
    print("here's a dev card")
  else:
    print("Not enough resources to get dev card!!")
  




# CHECK FOR RESOURCES TO GET ITEMS
def has_needed_resources(item, a_player):
  if item == "road":
    # Check that they have 1 brick and lumber
    b = 0
    l = 0
    for card in a_player.p_hand:
      if card.resource == "B":
        b+=1
      if card.resource == "L":
        l+=1
      
    if (b > 0 and l > 0):
      return True
    else:
      return False
    
  
  elif (item == "settlement"):
    # Check that they have 1 sheep, wheat, brick, and lumber
    b = 0
    l = 0
    s = 0
    w = 0

    for card in a_player.p_hand:
      if card.resource == "B":
        b+=1
      if card.resource == "L":
        l+=1
      if card.resource == "W":
        w+=1
      if card.resource == "S":
        s+=1
      
    
    if (b > 0 and l > 0 and w > 0 and s > 0):
      return True
    
    else:
      return False


  elif (item == "city"):
    # Check that they have 2 wheat, 3 ore
    o = 0
    w = 0
    for card in a_player.p_hand:
      if card.resource == "O":
        o+=1 
      elif card.resource == "W":
        w+=1    
      
    
    if (o > 2 and w > 1):
      return True
    else:
      return False

  elif (item == "dev_card"):
    # Check they have 1 sheep, ore and wheat
    o = 0
    w = 0
    s = 0
    counter = 0

    for card in a_player.p_hand:
      if card.resource == "O":
        o+=1
      elif card.resource == "W":
        w+=1
      elif card.resource == "S":
        s+=1

    if (o > 0 and w > 0 and s > 0):
      return True
    else:
      return False