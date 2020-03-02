
#========================================================
#FILE PURPOSE:
#  - The functions contained in this file will directly pertain to the game loop.
#========================================================


#========================================================
#BUG SECTION:
# Selecting "Upgrade into city" functions unexpecetedly
# The game improperly calculates a winner. Gives it out with not enough points.
# need feedback for what kind of dev card you recieve.
# Playing a dev card throws an error.
#========================================================

#========================================================
# Requirements and Exports
#========================================================
import random
import catan_classes
import items
import config
import math
import socket
from _thread import *

#========================================================
# FUNCTION DECLARATIONS
#========================================================

def catan_print(conn, given_str):
    conn.send(given_str.encode('ascii'))
    return

def catan_read(conn, size=1024):
    s = conn.recv(size).decode('ascii').strip()
    return s

def handle_errors(conn, result):
    if result == -1:
        catan_print(conn, "That's an invalid location\n")
    elif result == -2:
        catan_print(conn, "Someone is already on that space!!\n")
    elif result == -3:
        catan_print(conn, "Someone is on an adjacent space!!\n")
    elif result == -4:
        catan_print(conn, "The correct format is tile,corner\n")
        catan_print(conn, "EXAMPLE: 1,2\n")
    elif result == -5:
        catan_print(conn, "Your road must be connected to one of your settlements\n")
    elif result == -6:
        catan_print(conn,"Not enough resources!!\n")
    elif result == -7:
        catan_print(conn,"Already a city!! Cannot upgrade\n")
    elif result == -8:
        catan_print(conn,"Cannot upgrade unsettled location...\n")
    elif result == -99:
        catan_print(conn, "Invalid input... Please try again.\n")
    else:
        catan_print(conn, "That caused some unknown error, please try to not do that again :)\n")
#==========================================================================
# FROM CONFIG
#==========================================================================

# include all the globably needed stuff in here.

def create_nodes():
	nodes = []
	for x in range(1,55):
		nodes.append(catan_classes.Node(x))
	return nodes

def init_dev_cards():
    dev_cards = []
    for i in range(0,25):
        if i<14:
            new_card = catan_classes.Dev_Card("Knight")
            dev_cards.append(new_card)
        elif i<19:
            new_card = catan_classes.Dev_Card("Victory Point")
            dev_cards.append(new_card)
        elif i<21:
            new_card = catan_classes.Dev_Card("Year of Plenty")
            dev_cards.append(new_card)
        elif i<23:
            new_card = catan_classes.Dev_Card("Road Building")
            dev_cards.append(new_card)
        else:
            new_card = catan_classes.Dev_Card("Monopoly")
            dev_cards.append(new_card)
    return dev_cards

def shuffle(a_list):
    new_l = []
    max_i = len(a_list)-1

    for i in range(0, len(a_list)):
        random_index = random.randint(0, max_i)
        new_l.append(a_list.pop(random_index))
        max_i -= 1
        i += 1
    return new_l


def print_dev_cards(cards):
    for c in cards:
        print(c)



def init_nodes():
    x = create_nodes()
    x[0].alias = [(1,6)]
    x[1].alias = [(1,1)]
    x[2].alias = [(1,2),(2,6)]
    x[3].alias = [(2,1)]
    x[4].alias = [(2,2),(3,6)]
    x[5].alias = [(3,1)]
    x[6].alias = [(3,2)]
    x[7].alias = [(4,1),(1,5)]
    x[8].alias = [(1,4),(4,2),(5,6)]
    x[9].alias = [(1,3),(2,5),(5,1)]
    x[10].alias = [(2,4),(5,2),(6,6)]
    x[11].alias = [(2,3),(3,5),(6,1)]
    x[12].alias = [(3,4),(6,2),(7,6)]
    x[13].alias = [(3,3),(7,1)]
    x[14].alias = [(7,2)]
    x[15].alias = [(4,6)]
    x[16].alias = [(4,5),(8,1)]
    x[17].alias = [(4,4),(8,2),(9,6)]
    x[18].alias = [(4,3),(5,5),(9,1)]
    x[19].alias = [(5,4),(9,2),(10,6)]
    x[20].alias = [(5,3),(6,5),(10,1)]
    x[21].alias = [(6,4),(10,2),(11,6)]
    x[22].alias = [(6,3),(7,5),(11,1)]
    x[23].alias = [(7,4),(11,2),(12,6)]
    x[24].alias = [(7,3),(12,1)]
    x[25].alias = [(12,2)]
    x[26].alias = [(8,6)]
    x[27].alias = [(8,5)]
    x[28].alias = [(8,4),(13,6)]
    x[29].alias = [(8,3),(9,5),(13,1)]
    x[30].alias = [(9,4),(13,2),(14,6)]
    x[31].alias = [(9,3),(10,5),(14,1)]
    x[32].alias = [(10,4),(14,2),(15,6)]
    x[33].alias = [(10,3),(11,5),(15,1)]
    x[34].alias = [(11,4),(15,2),(16,6)]
    x[35].alias = [(11,3),(12,5),(16,1)]
    x[36].alias = [(12,4),(16,2)]
    x[37].alias = [(12,3)]
    x[38].alias = [(13,5)]
    x[39].alias = [(13,4),(17,6)]
    x[40].alias = [(13,3),(14,5),(17,1)]
    x[41].alias = [(14,4),(17,2),(18,6)]
    x[42].alias = [(14,3),(15,5),(18,1)]
    x[43].alias = [(15,4),(18,2),(19,6)]
    x[44].alias = [(15,3),(16,5),(19,1)]
    x[45].alias = [(16,4),(19,2)]
    x[46].alias = [(16,3)]
    x[47].alias = [(17,5)]
    x[48].alias = [(17,4)]
    x[49].alias = [(17,3),(18,5)]
    x[50].alias = [(18,4)]
    x[51].alias = [(18,3),(19,5)]
    x[52].alias = [(19,4)]
    x[53].alias = [(19,3)]

    # id by number
    x[0].adj_nodes = [2,8]
    x[1].adj_nodes = [1,3]
    x[2].adj_nodes = [2,4,10]
    x[3].adj_nodes = [3,5]
    x[4].adj_nodes = [4,6,12]
    x[5].adj_nodes = [5,7]
    x[6].adj_nodes = [6,14]
    x[7].adj_nodes = [1,9,16]
    x[8].adj_nodes = [8,10,19]
    x[9].adj_nodes = [3,9,11]
    x[10].adj_nodes = [10,12,21]
    x[11].adj_nodes = [5,11,13]
    x[12].adj_nodes = [12,14,23]
    x[13].adj_nodes = [7,13,15]
    x[14].adj_nodes = [14,25]
    x[15].adj_nodes = [6,17]
    x[16].adj_nodes = [16,18,27]
    x[17].adj_nodes = [17,19,30]
    x[18].adj_nodes = [9,18,20]
    x[19].adj_nodes = [19,21,32]
    x[20].adj_nodes = [11,20,22]
    x[21].adj_nodes = [21,23,34]
    x[22].adj_nodes = [13,22,24]
    x[23].adj_nodes = [23,25,36]
    x[24].adj_nodes = [15,24,26]
    x[25].adj_nodes = [25,38]
    x[26].adj_nodes = [17,28]
    x[27].adj_nodes = [27,29]
    x[28].adj_nodes = [28,30,39]
    x[29].adj_nodes = [18,29,31]
    x[30].adj_nodes = [30,32,41]
    x[31].adj_nodes = [20,31,33]
    x[32].adj_nodes = [32,34,43]
    x[33].adj_nodes = [22,33,35]
    x[34].adj_nodes = [34,36,45]
    x[35].adj_nodes = [24,35,37]
    x[36].adj_nodes = [36,38,47]
    x[37].adj_nodes = [26,37]
    x[38].adj_nodes = [29,40]
    x[39].adj_nodes = [39,41,48]
    x[40].adj_nodes = [31,40,42]
    x[41].adj_nodes = [41,43,50]
    x[42].adj_nodes = [33,42,44]
    x[43].adj_nodes = [43,45,52]
    x[44].adj_nodes = [35,44,46]
    x[45].adj_nodes = [45,47,54]
    x[46].adj_nodes = [37,46]
    x[47].adj_nodes = [40,49]
    x[48].adj_nodes = [48,50]
    x[49].adj_nodes = [42,49,51]
    x[50].adj_nodes = [50,52]
    x[51].adj_nodes = [44,51,53]
    x[52].adj_nodes = [52,54]
    x[53].adj_nodes = [46,53]
    return x


def init_roads(list_of_nodes):
	roads = []
	id = 0
	for n in list_of_nodes:
		for thing in n.adj_nodes:
			if n.id < thing:
				new_road = catan_classes.Road(n.id,thing,id)
				roads.append(new_road)
				id+=1
	return roads





# returns string that i'll need to send to the clients.
def show_board(b, node_list, road_list, game_robber):
	to_print = '''
                              >-----<
                             /~~~~~~~\\
                            /~~~~~~~~~\\
                     >-----<~~~~3:1~~~~>-----<
                    /~~~~~~~\~~~~~~~~~/~~~~~~~\\
                   /~~~~~~~~~\*~~~~~*/~~~~~~~~~\\
            >-----<~~~~~~~~~~~{62}.{138}.{138}.{63}~~~~~~~~~~~>-----<
           /~~~~~~~\~~~~~~~~~{136}       {139}~~~~~~~~~/~~~~~~~\\
          /~~~2:1~~~\~~~~~~~{136}    {0}   {139}~~~~~~~/~~~2:1~~~\\
   >-----<~~~wood~~~*{60}.{135}.{135}.{61}    {111}{1}     {70}.{150}.{150}.{71}*~~sheep~~~>-----<
  /~~~~~~~\~~~~~~~~~{133}       {137}    {2}   {148}       {151}~~~~~~~~~/~~~~~~~\\
 /~~~~~~~~~\~~~~~~*{133}    {3}   {137}       {148}    {4}   {151}*~~~~~~/~~~~~~~~~\\
<~~~~~~~~~~~{58}.{132}.{132}.{59}    {112}{5}     {68}.{147}.{147}.{69}    {113}{6}     {81}.{166}.{166}.{82}~~~~~~~~~~~>
 \~~~~~~~~~{130}       {134}    {7}   {145}       {149}    {8}   {164}       {167}~~~~~~~~~/
  \~~~~~~~{130}    {9}   {134}       {145}    {10}   {149}       {164}    {11}   {167}~~~~~~~/
   >-----{57}    {114}{12}     {66}.{144}.{144}.{67}    {115}{13}     {79}.{163}.{163}.{80}    {116}{14}     {94}-----<
  /~~~~~~~{131}    {15}   {142}       {146}    {16}   {161}       {165}    {17}   {182}~~~~~~~\\
 /~~~2:1~~~{131}       {142}    {18}   {146}       {161}    {19}   {165}       {182}~~~2:1~~~\\
<~~~brick~~*{64}.{140}.{140}.{65}    {117}{20}     {77}.{160}.{160}.{78}    {118}{21}     {92}.{181}.{181}.{93}*~~~ore~~~~>
 \~~~~~~~~~{141}       {143}    {22}   {158}       {162}    {23}   {179}       {183}~~~~~~~~~/
  \~~~~~~*{141}    {24}   {143}       {158}    {25}   {162}       {179}    {26}   {183}*~~~~~~/
   >-----{72}    {119}{27}     {75}.{157}.{157}.{76}    {120}{28}     {90}.{178}.{178}.{91}    {121}{29}     {103}-----<
  /~~~~~~~{152}    {30}   {155}       {159}    {31}   {176}       {180}    {32}   {194}~~~~~~~\\
 /~~~~~~~~~{152}       {155}    {33}   {159}       {176}    {34}   {180}       {194}~~~~~~~~~\\
<~~~~~~~~~~~{73}.{153}.{153}.{74}    {122}{35}     {88}.{175}.{175}.{89}    {123}{36}     {101}.{193}.{193}.{102}~~~~~~~~~~~>
 \~~~~~~~~~{154}       {156}    {37}   {173}       {177}    {38}   {191}       {195}~~~~~~~~~/
  \~~~~~~~{154}    {39}   {156}       {173}    {40}   {177}       {191}    {41}   {195}~~~~~~~/
   >-----{83}    {124}{42}     {86}.{172}.{172}.{87}    {125}{43}     {99}.{190}.{190}.{100}    {126}{44}     {110}-----<
  /~~~~~~*{168}    {45}   {170}       {174}    {46}   {188}       {192}    {47}   {201}*~~~~~~\\
 /~~~~~~~~~{168}       {170}    {48}   {174}       {188}    {49}   {192}       {201}~~~~~~~~~\\
<~~~~3:1~~~*{84}.{169}.{169}.{85}    {127}{50}     {97}.{187}.{187}.{98}    {128}{51}     {108}.{200}.{200}.{109}*~~~3:1~~~~>
 \~~~~~~~~~/~~~~~~~{171}    {52}   {185}       {189}    {53}   {199}~~~~~~~\~~~~~~~~~/
  \~~~~~~~/~~~~~~~~~{171}       {185}    {54}   {189}       {199}~~~~~~~~~\~~~~~~~/
   >-----< ~~~~~~~~~~{95}.{184}.{184}.{96}    {129}{55}     {106}.{198}.{198}.{107}~~~~~~~~~~~>-----<
          \~~~~~~~~~/*~~~~~*{186}    {56}   {197}*~~~~~*\~~~~~~~~~/
           \~~~~~~~/~~~~~~~~~{186}       {197}~~~2:1~~~\~~~~~~~/
            >-----<~~~~3:1~~~~{104}.{196}.{196}.{105}~~~grain~~~>-----<
                   \~~~~~~~~~/~~~~~~~\~~~~~~~~~/
                    \~~~~~~~/~~~~~~~~~\~~~~~~~/
                     >-----<~~~~~~~~~~~>-----<
                            \~~~~~~~~~/
                             \~~~~~~~/
                              >-----<

							  '''.format(str(b.tiles[2].number).ljust(2, ' '),str(b.tiles[2].resource),str(b.tiles[2].id).ljust(2, ' '),str(b.tiles[1].number).ljust(2, ' '),
							  str(b.tiles[6].number).ljust(2, ' '),str(b.tiles[1].resource),str(b.tiles[6].resource),str(b.tiles[1].id).ljust(2, ' '), str(b.tiles[6].id).ljust(2, ' ')
							  ,str(b.tiles[0].number).ljust(2, ' '),str(b.tiles[5].number).ljust(2, ' '),str(b.tiles[11].number).ljust(2, ' '), str(b.tiles[0].resource),
							  str(b.tiles[5].resource),str(b.tiles[11].resource),str(b.tiles[0].id).ljust(2, ' '),str(b.tiles[5].id).ljust(2, ' '),str(b.tiles[11].id).ljust(2, ' '),
							  str(b.tiles[4].number).ljust(2, ' '),str(b.tiles[10].number).ljust(2, ' '),str(b.tiles[4].resource),str(b.tiles[10].resource),
							  str(b.tiles[4].id).ljust(2, ' '),str(b.tiles[10].id).ljust(2, ' '),str(b.tiles[3].number).ljust(2, ' '),str(b.tiles[9].number).ljust(2, ' '),str(b.tiles[15].number).ljust(2, ' '),
							  str(b.tiles[3].resource),str(b.tiles[9].resource),str(b.tiles[15].resource),str(b.tiles[3].id).ljust(2, ' '),
							  str(b.tiles[9].id).ljust(2, ' '),str(b.tiles[15].id).ljust(2, ' '),str(b.tiles[8].number).ljust(2, ' '),str(b.tiles[14].number).ljust(2, ' '),str(b.tiles[8].resource)
							  ,str(b.tiles[14].resource),str(b.tiles[8].id).ljust(2, ' '),str(b.tiles[14].id).ljust(2, ' '),str(b.tiles[7].number).ljust(2, ' '),str(b.tiles[13].number).ljust(2, ' ')
							  ,str(b.tiles[18].number).ljust(2, ' '),str(b.tiles[7].resource),str(b.tiles[13].resource),str(b.tiles[18].resource),
							  str(b.tiles[7].id).ljust(2, ' '),str(b.tiles[13].id).ljust(2, ' '),str(b.tiles[18].id).ljust(2, ' '),str(b.tiles[12].number).ljust(2, ' '),str(b.tiles[17].number).ljust(2, ' '),
							  str(b.tiles[12].resource),str(b.tiles[17].resource),str(b.tiles[12].id).ljust(2, ' '),str(b.tiles[17].id).ljust(2, ' '),
							  str(b.tiles[16].number).ljust(2, ' '),str(b.tiles[16].resource),str(b.tiles[16].id).ljust(2, ' '), node_list[0].status(),
							   node_list[1].status(),node_list[2].status(),node_list[3].status(),
							   node_list[4].status(),node_list[5].status(),node_list[6].status(),
							   node_list[7].status(),node_list[8].status(),node_list[9].status(),
							   node_list[10].status(),node_list[11].status(),node_list[12].status(),
							   node_list[13].status(),node_list[14].status(),node_list[15].status(),
							   node_list[16].status(),node_list[17].status(),node_list[18].status(),
							   node_list[19].status(),node_list[20].status(),node_list[21].status(),
							   node_list[22].status(),node_list[23].status(),node_list[24].status(),
							   node_list[25].status(),node_list[26].status(),node_list[27].status(),
							   node_list[28].status(),node_list[29].status(),node_list[30].status(),
							   node_list[31].status(),node_list[32].status(),node_list[33].status(),
							   node_list[34].status(),node_list[35].status(),node_list[36].status(),
							   node_list[37].status(),node_list[38].status(),node_list[39].status(),
							   node_list[40].status(),node_list[41].status(),node_list[42].status(),
							   node_list[43].status(),node_list[44].status(),node_list[45].status(),
							   node_list[46].status(),node_list[47].status(),node_list[48].status(),
							   node_list[49].status(),node_list[50].status(),node_list[51].status(),
							   node_list[52].status(),node_list[53].status(),game_robber.is_on_tile(3)
							   ,game_robber.is_on_tile(2),game_robber.is_on_tile(7),game_robber.is_on_tile(1),game_robber.is_on_tile(6)
							   ,game_robber.is_on_tile(12),game_robber.is_on_tile(5),game_robber.is_on_tile(11),game_robber.is_on_tile(4)
							   ,game_robber.is_on_tile(10),game_robber.is_on_tile(16),game_robber.is_on_tile(9),game_robber.is_on_tile(15)
							   ,game_robber.is_on_tile(8),game_robber.is_on_tile(14),game_robber.is_on_tile(19),game_robber.is_on_tile(13),game_robber.is_on_tile(18)
							   ,game_robber.is_on_tile(17),road_list[0].show_road(),road_list[1].show_road()
							   ,road_list[2].show_road(),road_list[3].show_road(),road_list[4].show_road()
							   ,road_list[5].show_road(),road_list[6].show_road(),road_list[7].show_road()
							   ,road_list[8].show_road(),road_list[9].show_road(),road_list[10].show_road()
							   ,road_list[11].show_road(),road_list[12].show_road(),road_list[13].show_road()
							   ,road_list[14].show_road(),road_list[15].show_road(),road_list[16].show_road()
							   ,road_list[17].show_road(),road_list[18].show_road(),road_list[19].show_road()
							   ,road_list[20].show_road(),road_list[21].show_road(),road_list[22].show_road()
							   ,road_list[23].show_road(),road_list[24].show_road(),road_list[25].show_road()
							   ,road_list[26].show_road(),road_list[27].show_road(),road_list[28].show_road()
							   ,road_list[29].show_road(),road_list[30].show_road(),road_list[31].show_road()
							   ,road_list[32].show_road(),road_list[33].show_road(),road_list[34].show_road()
							   ,road_list[35].show_road(),road_list[36].show_road(),road_list[37].show_road()
							   ,road_list[38].show_road(),road_list[39].show_road(),road_list[40].show_road()
							   ,road_list[41].show_road(),road_list[42].show_road(),road_list[43].show_road()
							   ,road_list[44].show_road(),road_list[45].show_road(),road_list[46].show_road()
							   ,road_list[47].show_road(),road_list[48].show_road(),road_list[49].show_road()
							   ,road_list[50].show_road(),road_list[51].show_road(),road_list[52].show_road()
							   ,road_list[53].show_road(),road_list[54].show_road(),road_list[55].show_road()
							   ,road_list[56].show_road(),road_list[57].show_road(),road_list[58].show_road()
							   ,road_list[59].show_road(),road_list[60].show_road(),road_list[61].show_road()
							   ,road_list[62].show_road(),road_list[63].show_road(),road_list[64].show_road()
							   ,road_list[65].show_road(),road_list[66].show_road(),road_list[67].show_road()
							   ,road_list[68].show_road(),road_list[69].show_road(),road_list[70].show_road()
							   ,road_list[71].show_road())
#.ljust(5, ' ') should work for padding. but it only applies to strings, so we have to turn them into strings first. Robber not accounted for
# 5, and 6 i took out 6 instead of 6
# all of the b.tile stuff now needs the padding, i took the spaces out of the template.  The resource ones need 6.
# should always be three spaces in the format, and 2 characters of padding for all the numbers (id and number)
# 1 space for resource character, and 5 spaces in format template
	return to_print

def roll_dice():
    x = random.randint(1, 6)
    y = random.randint(1, 6)
    return x + y


def random_tile(id):
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
    rand_tile = catan_classes.Tile(tile_r, tile_n, id)
    return rand_tile


def init_board():
	b = catan_classes.Board()
	for i in range(1,20):
		b.tiles.append(random_tile(i))
	return b


def init_robber(tile_id):
	r = catan_classes.Robber(tile_id)
	return r

#======================================================


def catan_client(conn):

    start_game = False
    while not start_game:
        msg = display_main_menu()
        catan_print(conn, msg)
        selection = catan_read(conn)
        selection = int(selection)
        if selection == 1:
            start_game = True
        elif selection == 2:
            explain_rules(conn)
            continue
        elif selection == 3:
            display_credits(conn)
            continue
        else:
            catan_print(conn, "Please enter an appropriate value")

    # Do initial setup
    player_list = get_player_info(conn)
    dev_cards = shuffle(init_dev_cards())
    b = init_board()
    game_robber = init_robber(random.randint(1, 20))
    node_list = init_nodes()
    road_list = init_roads(node_list)

    # establish points to win
    points_to_win = declare_pts_to_win(conn)
    print(str(points_to_win))
    robber = init_robber(random.randint(1, 20))

    # show_board returns the board as a string
    catan_print(conn, show_board(b, node_list, road_list, game_robber)) #show_board(b, node_list, road_list, robber)
    curr_player_turn = 0
    place_initial(conn, player_list, b, node_list, road_list, game_robber)
    catan_print(conn, items.give_resources(0, game_robber, b, player_list, node_list, True))



    winner = False
    while winner != True:
        winner = player_turn(conn, player_list[curr_player_turn], points_to_win, player_list, b, node_list, road_list, game_robber, dev_cards) #player_turn(conn, player, points_to_win, robber, player_list, b, node_list, road_list, robber)
        if winner:
            break
        curr_player_turn = increment_player_turn(curr_player_turn, len(player_list))

    catan_print(conn, "\nWINNER: " + player_list[curr_player_turn].p_name + "\n")

    conn.close()
    print("Gracefully closed connection to client")





def move_robber(conn, game_robber):
    knight_placed = False
    while knight_placed == False:
        catan_print(conn, "Which tile will you place the robber on?\n> ")
        t = int(catan_read(conn))
        if t == game_robber.on_tile: # can i get the board this way or does it have to be an argument? Maybe just put it in config?
            catan_print(conn, "You must put the robber on a new tile.")
            continue
        else:
            # maybe the tile that the robber is on should be an attribute of the robber, because im going to have to iterate over all the times to "undo" the old robber.
            game_robber.on_tile = t
            knight_placed = True


def play_dev_card(conn, a_player, dev_card, player_list, node_list, road_list, game_robber):
    # Partially Implemented
    if dev_card.card_type == "Knight":
        catan_print(conn, a_player.p_name + " played a development card: ")
        catan_print(conn, dev_card.card_type) # this might break, need to pass a string
        move_robber(conn, game_robber)
        # steal a card from a player.

    #DONE
    elif dev_card.card_type == "Road Building":
        catan_print(conn, a_player.p_name + " played a development card: ")
        catan_print(conn, dev_card.card_type)
        a_player.p_hand.append("B")
        a_player.p_hand.append("L")
        a_player.p_hand.append("B")
        a_player.p_hand.append("L")

        # this should force the player to build two roads
        roads_placed = 0
        while roads_placed != 2:
            # have to check they built a valid road. function can return None.
            # going to have to ask for user input here and read the result first.
            catan_print(conn, "Where do you want to start your road?\n> ")
            n1 = catan_read(conn)
            catan_print(conn, "Where do you want to end your road?\n> ")
            n2 = catan_read(conn)
            if items.build_road(a_player, n1, n2, node_list, road_list) == None: #build_road(a_player, n1, n2, node_list, road_list, initializing = False)
                continue
            else:
                roads_placed += 1

    #DONE
    elif dev_card.card_type == "Year of Plenty":
        catan_print(conn, a_player.p_name + " played a development card: ")
        catan_print(conn, dev_card.card_type)

        added_cards = 0
        while added_cards != 2: # even if this loo
            catan_print(conn, "What resource would you like? Resource (" + str(added_cards+1) + "/2)")
            wanted_card = catan_read(conn)
            if wanted_card.upper() in "BLSWO":
                    a_player.p_hand.append(wanted_card.upper())
                    added_cards += 1
            else:
                catan_print(conn, wanted_card + " is not a valid resource")

    #DONE
    elif dev_card.card_type == "Monopoly":
        catan_print(conn, a_player.p_name + " played a development card: ")
        catan_print(conn, dev_card.card_type)
        got_resources = False
        while got_resources == False:
            catan_print(conn, "What resource would you like?\n> ")
            wanted_card = catan_read(conn)
            if wanted_card.upper() in "BLSWO":
                num_taken = 0
                for p in player_list: # wait, this actually takes cards from the player using it too, since they're in player list. I guess that's okay if i add them back?
                    for resource in p.p_hand:
                        if resource == wanted_card.upper():
                            p.p_hand.remove(resource)
                            num_taken += 1

                for num in range(0, num_taken):
                    a_player.p_hand.append(wanted_card.upper())

                catan_print(conn, a_player.p_name + " took all everyone's " + wanted_card.upper())
                got_resources = True

            else:
                catan_print(conn, wanted_card + " is not a valid resource")


    #DONE
    elif dev_card.card_type == "Victory Point":
        catan_print(conn, "Victory point card played!!\n") # make sure this is only adding a victory point once, not now and when they get it.
        a_player.p_victory_pts += 1 # I don't want to tell anyone else that this was played.

    else:
        catan_print(conn, "Not a known development card type")



def player_choose_color(conn, color_options):
        catan_print(conn, "Which color will you be?\n")
        i = 1
        for c in color_options:
            color_format = "\t" + str(i) + ". " + c + "\n"
            catan_print(conn, color_format)
            i += 1
        try:
            catan_print(conn, "Chose the number of the color you'd like.\n> ")
            choice = int(catan_read(conn))
            return choice

        except ValueError:
            catan_print(conn, "You must enter an integer.") # this exception handling might not work...
            choice = player_choose_color(conn, color_options) # I don't want to call this recursively, but im hacking it together.
            return choice

#def valid_discard(a_string, player_hand):

def robber(conn, player_list, game_robber):
    catan_print(conn, "ROBBER HAS BEEN ROLLED\n")

    # Loop checks to see if any players have 7 or more cards
    for i in player_list:
        if len(i.p_hand) >= 7:
            num_to_discard = math.ceil(len(i.p_hand)/2)
            discard = ""
            has_cards = False
            while len(discard) != num_to_discard or has_cards == False:
                catan_print(conn, i.p_name + " this is your current hand: ")
                i.show_hand()
                catan_print(conn, i.p_name + " Please discard " + str(num_to_discard) + " cards\n> ")
                discard = catan_read(conn)
                if len(discard) > num_to_discard:
                    catan_print(conn, "You have discarded more cards than necessary.")

                elif len(discard) < num_to_discard:
                    catan_print(conn, "You didn't discard enough cards... try again.")

                if i.p_hand.count("O") >= list(discard).count("O") and i.p_hand.count("B") >= list(discard).count("B") and i.p_hand.count("S") >= list(discard).count("S") and i.p_hand.count("W") >= list(discard).count("W") and i.p_hand.count("L") >= list(discard).count("L"):
                    has_cards = True

                else:
                    has_cards = False
                    catan_print(conn, "You do not have those cards")
            for card in discard:
                i.p_hand.remove(card)
            catan_print(conn, "\n" + i.p_name + " this is your new hand: \n")
            i.show_hand()

    move_robber(conn, game_robber)

def increment_player_turn(current_player_turn, num_players):
    return (current_player_turn + 1) % num_players


def player_menu(conn):
    catan_print(conn,
'''
        1. View your hand
        2. Buy a road
        3. Buy a settlement
        4. Upgrade a settlement to a city
        5. Buy a development card
        6. Trade with a player
        7. Trade with the bank (4 for 1)
        8. Trade using a port
        9. Display Board
        10. View Development cards
        11. Play Development Card
        12. Show current victory points
        0. End Turn
'''
    )

def trade_resources(player, trade_to, want, offer):
    for r in offer:
        player.p_hand.remove(r)
        trade_to.p_hand.append(r)

    for r in want:
        player.p_hand.append(r)
        trade_to.p_hand.remove(r)

def trade_accepted(conn, player, trade_to, want, offer):
    catan_print(conn, trade_to.p_name + ", " + player.p_name + " has offered you: " )
    catan_print(conn, offer + "\n")
    catan_print(conn, "In exchange for: ")
    catan_print(conn, want + "\n")
    choice = ""
    while choice == "":
        catan_print(conn, "Do you want to accept this trade? (y/n)\n> ")
        choice = catan_read(conn)
        if choice not in "yn":
            catan_print(conn, "You must enter 'y' or 'n'")
            choice = ""
            continue

    if choice == "y":
        return True
    elif choice == "n":
        return False

def player_turn(conn, player, points_to_win, player_list, b, node_list, road_list, game_robber, dev_cards): #player_turn(conn, player, points_to_win, robber, player_list, b, node_list, road_list, robber)
    catan_print(conn, "\n" + player.p_name + " it is your turn\n")

    catan_print(conn, "Press Enter to Roll Die")
    user_input = catan_read(conn)

    roll = roll_dice()
    catan_print(conn, "\n" + str(roll) + " has been rolled\n")
    catan_print(conn, items.give_resources(roll, game_robber, b, player_list, node_list)) #give_resources(roll_num, robber, b, player_list, initial = False)


    #Check to see if robber() should be called
    if roll == 7:
        robber(conn, player_list, game_robber)

  #Player Selects an Option
    selection = -1
    while selection != 0:
        player_menu(conn)
        try:
            catan_print(conn, "Please Select One\n"+ player.p_name + "> ")
            selection = int(catan_read(conn))
        except ValueError:
            catan_print(conn, "You must enter a number corresponding to an option")
            selection = -1

        if selection == 1:
            catan_print(conn, player.show_hand())

        elif selection == 2:
            server_build_item(conn, player, "road", node_list, road_list)


        elif selection == 3:
            server_build_item(conn, player, "settlement", node_list,road_list)

        elif selection == 4:
            server_build_item(conn, player, "city", node_list) #build_city(a_player,location,node_list)

        elif selection == 5:
            result = items.build_dev_card(player, dev_cards) #build_dev_card(a_player, dev_cards)
            if isinstance(result, str):
                catan_print(conn, result)
            elif isinstance(result, int):
                handle_errors(conn, result)


        elif selection == 6:
            catan_print(conn, "Players:\n")
            counter  = 1
            for p in player_list:
                catan_print(conn, "\t" + str(counter) + ". " + p.p_name + "\n")
                counter += 1
            catan_print(conn, "\t" + str(counter) + ". Offer trade to everyone\n")
            catan_print(conn, "Who do you want to trade with?\n> ")

            option = int(catan_read(conn)) # gonna have to do error checking on this too...
            trade_to = player_list[option-1]
            catan_print(conn, "What resource(s) do you want?")
            want = catan_read(conn)
            catan_print(conn, "What resource(s) are you offering in exchange?\n> ")
            offer = catan_read(conn)


            if option <= len(player_list):
                if player.has_resources(offer):
                    want_to_trade = trade_accepted(conn, player, trade_to, want, offer)
                    they_have_resources = trade_to.has_resources(want)
                    if want_to_trade and they_have_resources:
                        trade_resources(player, trade_to, want, offer)
                else:
                    catan_print(conn, "You don't have those resources to offer...")
            elif trade_to == len(player_list) + 1:
                catan_print(conn, "Trade to all players is coming soon")
            else:
                catan_print(conn, "Invalid option")





        elif selection == 7:
            catan_print(conn, "What resource would you like?\n> ")
            want = catan_read(conn)
            catan_print(conn, "What resource will you be trading 4 of?\n> ")
            give = catan_read(conn)
            if player.has_resources(give*4):
                player.p_hand.remove(give)
                player.p_hand.remove(give)
                player.p_hand.remove(give)
                player.p_hand.remove(give)
                player.p_hand.append(want)
                catan_print(conn, "You traded with the bank!")

            else:
                catan_print(conn, "You don't have enough of that resource to trade...")

        elif selection == 8:
            catan_print(conn, "Trade using a port")

        elif selection == 9:
            catan_print(conn, show_board(b, node_list, road_list, game_robber))

        elif selection == 10:
            catan_print(conn, player.show_dev_cards())


        elif selection == 11:
            if player.p_dev_cards == []:
                catan_print(conn, "You have no development cards!!")
                continue
            catan_print(conn, "Please select a dev_card: \n")
            msg_to_client = player.show_dev_cards()
            catan_print(conn, msg_to_client)
            num = int(catan_read(conn)) # this will break if they give something other than an int.
            play_dev_card(conn, player, player.p_dev_cards[num-1], player_list, node_list, road_list, game_robber) #play_dev_card(conn, a_player, dev_card, player_list, node_list, road_list, robber)

        elif selection == 12:
            catan_print(conn, player.show_victory_pts())

        elif selection == 0:
            pass


        # I don't know if this check actually works.

        if int(player.show_victory_pts()) >= points_to_win:
            return True



    return False

#========================================================
# START OF GAME
#========================================================




def server_build_item(conn, a_player, item, node_list, road_list, init = False):

    # There's a way to get this down into one thing. More DRY, but i can't figure it out rn.
    # PARTIALLY IMPLEMENTED
    if item == "city":
        catan_print(conn, "Where would you like to upgrade into a city?\n> ")
        location = catan_read(conn)
        result = items.build_city(a_player, location, node_list)
        if isinstance(result, int):
            handle_errors(conn, result)
        elif isinstance(result, str):
            catan_print(conn, result)



    # There's a way to get this down into one thing. More DRY, but i can't figure it out rn.
    # PARTIALLY IMPLEMENTED
    elif item == "settlement":
        if init:
            settled = False
            while settled == False:
                catan_print(conn, "Where do you want to place your settlement?\n" + a_player.p_name.strip() + "> ")
                location = catan_read(conn)
                result = items.build_settlement(a_player, location, node_list, True)
                if isinstance(result, int):
                    handle_errors(conn, result)
                elif isinstance(result, str):
                    catan_print(conn, result)
                    settled = True


        else:
            catan_print(conn, "Where do you want to place your settlement?\n> ")
            location = catan_read(conn)
            result = items.build_settlement(a_player, location, node_list)
            if isinstance(result, int):
                handle_errors(conn, result)
            elif isinstance(result, str):
                catan_print(conn, result)

    #server_build_item(conn, p, "road", node_list, init=True)
    elif item == "road": # not yet written for anything other than initial setup
        if init:
            first_road = False
            while first_road == False:
                catan_print(conn, "Where do you want to start your road?\n> ")
                n1 = catan_read(conn)
                catan_print(conn, "Where do you want to end your road?\n> ")
                n2 = catan_read(conn)
                result = items.build_road(a_player, n1, n2, node_list, road_list, True)
                if isinstance(result, int):
                    handle_errors(conn, result)
                elif isinstance(result, str):
                    catan_print(conn, result)
                    first_road = True
        else:
            catan_print(conn, "Where do you want to start your road?\n> ")
            n1 = catan_read(conn)
            catan_print(conn, "Where do you want to end your road?\n> ")
            n2 = catan_read(conn)
            result = items.build_road(a_player, n1, n2, node_list, road_list)
            if isinstance(result, int):
                handle_errors(conn, result)
            elif isinstance(result, str):
                catan_print(conn, result)

    elif item == "dev card":
        catan_print(conn, "Where do you want to start your road?\n> ")
        n1 = catan_read(conn)
        catan_print(conn, "Where do you want to end your road?\n> ")
        n2 = catan_read(conn)
        result = items.build_dev_card(a_player)
        if isinstance(result, int):
            handle_errors(conn, result)
        elif isinstance(result, str):
            catan_print(conn, result)


def place_initial(conn, player_list, b, node_list, road_list, game_robber):
    for p in player_list:
        catan_print(conn, "\n" + p.p_name.strip() + " is placing their first settlement\n")

        # FIRST SETTLEMENT
        server_build_item(conn, p, "settlement", node_list, road_list, init=True)
        catan_print(conn, show_board(b, node_list, road_list, game_robber))
        p.p_victory_pts += 1


        # FIRST ROAD
        catan_print(conn, "\n" + p.p_name.strip() + " is placing their first road\n")
        server_build_item(conn, p, "road", node_list, road_list, init=True)
        catan_print(conn, show_board(b, node_list, road_list, game_robber))


    for p in reversed(player_list):

        # SECOND SETTLEMENT
        catan_print(conn, "\n" + p.p_name + " is placing their second settlement\n")
        server_build_item(conn, p, "settlement", node_list, road_list, init=True)
        catan_print(conn, show_board(b, node_list, road_list, game_robber))
        p.p_victory_pts += 1

        # SECOND ROAD
        catan_print(conn, "\n" + p.p_name.strip() + " is placing their second road\n")
        server_build_item(conn, p, "road", node_list, road_list, init=True)
        catan_print(conn, show_board(b, node_list, road_list, game_robber))



def display_main_menu():
    template = '''
        CCCCCCCCCCCCC               AAA         TTTTTTTTTTTTTTTTTTTTTTT         AAA               NNNNNNNN        NNNNNNNN
     CCC::::::::::::C              A:::A        T:::::::::::::::::::::T        A:::A              N:::::::N       N::::::N
   CC:::::::::::::::C             A:::::A       T:::::::::::::::::::::T       A:::::A             N::::::::N      N::::::N
  C:::::CCCCCCCC::::C            A:::::::A      T:::::TT:::::::TT:::::T      A:::::::A            N:::::::::N     N::::::N
 C:::::C       CCCCCC           A:::::::::A     TTTTTT  T:::::T  TTTTTT     A:::::::::A           N::::::::::N    N::::::N
C:::::C                        A:::::A:::::A            T:::::T            A:::::A:::::A          N:::::::::::N   N::::::N
C:::::C                       A:::::A A:::::A           T:::::T           A:::::A A:::::A         N:::::::N::::N  N::::::N
C:::::C                      A:::::A   A:::::A          T:::::T          A:::::A   A:::::A        N::::::N N::::N N::::::N
C:::::C                     A:::::A     A:::::A         T:::::T         A:::::A     A:::::A       N::::::N  N::::N:::::::N
C:::::C                    A:::::AAAAAAAAA:::::A        T:::::T        A:::::AAAAAAAAA:::::A      N::::::N   N:::::::::::N
C:::::C                   A:::::::::::::::::::::A       T:::::T       A:::::::::::::::::::::A     N::::::N    N::::::::::N
 C:::::C       CCCCCC    A:::::AAAAAAAAAAAAA:::::A      T:::::T      A:::::AAAAAAAAAAAAA:::::A    N::::::N     N:::::::::N
  C:::::CCCCCCCC::::C   A:::::A             A:::::A   TT:::::::TT   A:::::A             A:::::A   N::::::N      N::::::::N
   CC:::::::::::::::C  A:::::A               A:::::A  T:::::::::T  A:::::A               A:::::A  N::::::N       N:::::::N
     CCC::::::::::::C A:::::A                 A:::::A T:::::::::T A:::::A                 A:::::A N::::::N        N::::::N
        CCCCCCCCCCCCCAAAAAAA                   AAAAAAATTTTTTTTTTTAAAAAAA                   AAAAAAANNNNNNNN         NNNNNNN


            MAIN MENU: Please Select and Option

        1. Play Catan
        2. Explain Rules
        3. Credits
> '''
    return template

def welcome():
    template = '''
        CCCCCCCCCCCCC               AAA         TTTTTTTTTTTTTTTTTTTTTTT         AAA               NNNNNNNN        NNNNNNNN
     CCC::::::::::::C              A:::A        T:::::::::::::::::::::T        A:::A              N:::::::N       N::::::N
   CC:::::::::::::::C             A:::::A       T:::::::::::::::::::::T       A:::::A             N::::::::N      N::::::N
  C:::::CCCCCCCC::::C            A:::::::A      T:::::TT:::::::TT:::::T      A:::::::A            N:::::::::N     N::::::N
 C:::::C       CCCCCC           A:::::::::A     TTTTTT  T:::::T  TTTTTT     A:::::::::A           N::::::::::N    N::::::N
C:::::C                        A:::::A:::::A            T:::::T            A:::::A:::::A          N:::::::::::N   N::::::N
C:::::C                       A:::::A A:::::A           T:::::T           A:::::A A:::::A         N:::::::N::::N  N::::::N
C:::::C                      A:::::A   A:::::A          T:::::T          A:::::A   A:::::A        N::::::N N::::N N::::::N
C:::::C                     A:::::A     A:::::A         T:::::T         A:::::A     A:::::A       N::::::N  N::::N:::::::N
C:::::C                    A:::::AAAAAAAAA:::::A        T:::::T        A:::::AAAAAAAAA:::::A      N::::::N   N:::::::::::N
C:::::C                   A:::::::::::::::::::::A       T:::::T       A:::::::::::::::::::::A     N::::::N    N::::::::::N
 C:::::C       CCCCCC    A:::::AAAAAAAAAAAAA:::::A      T:::::T      A:::::AAAAAAAAAAAAA:::::A    N::::::N     N:::::::::N
  C:::::CCCCCCCC::::C   A:::::A             A:::::A   TT:::::::TT   A:::::A             A:::::A   N::::::N      N::::::::N
   CC:::::::::::::::C  A:::::A               A:::::A  T:::::::::T  A:::::A               A:::::A  N::::::N       N:::::::N
     CCC::::::::::::C A:::::A                 A:::::A T:::::::::T A:::::A                 A:::::A N::::::N        N::::::N
        CCCCCCCCCCCCCAAAAAAA                   AAAAAAATTTTTTTTTTTAAAAAAA                   AAAAAAANNNNNNNN         NNNNNNN


                                    WELCOME TO CATAN!! WAITING FOR OTHER PLAYERS...
                                      GAME WILL BEGIN WHEN THERE ARE 2 PLAYERS
'''
    return template


def explain_rules(conn):
    catan_print(conn,'''
    Here are the rules for Catan:


    Please press Enter to go back to the main menu

    ''')
    reply = catan_read(conn)
    return reply


def display_credits(conn):
    catan_print(conn,'''
    Game Created by:
        Grayson "Twiggy" Gordon
        Anthony Walton

    Graphics:
        Grayson "Twiggy" Gordon
        Anthony Walton

    All Rights are owned by the creators of this game
    IF YOU STEAL THIS I WILL GET HANGRY


Please press Enter to go back to the main menu
    ''')
    reply = catan_read(conn)
    return reply

# Returns list of player objects
def get_player_info(conn):
    try:
        player_list = []
        catan_print(conn, "Please enter the number of players\n> ")

        num_players = int(catan_read(conn))
        i = 0
        color_options = ["Red", "Yellow", "Purple", "Green", "Cyan", "Tan"]

        while i < num_players:
            template = "Please Enter Player " + str((i + 1)) + "'s name\n> "
            catan_print(conn, template)
            name = catan_read(conn)

            p_color =  color_options.pop(player_choose_color(conn, color_options)-1)
            catan_print(conn, "You selected: " + p_color + "\n")
            color = p_color[0].lower()
            player_list.append(catan_classes.Player(name.strip(),color))
            i+=1

        return player_list

    except ValueError:
        catan_print(conn, "You must enter an integer")
        return

    except IndexError:
        catan_print(conn, "You must enter one of the provided options")
        return

def declare_pts_to_win(conn):
    try:
        catan_print(conn, "Enter the Amount of Points Required to Win\n> ")
        pts_to_win = int(catan_read(conn))
        return pts_to_win
    except ValueError:
        catan_print(conn, "You must provide an integer")


if __name__ == "__main__":
    connections = [] # list of connected clients

    # create a socket object
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 4445


    # bind to the port
    serversocket.bind(('', port))

    # Only take 1 connection for now until multi-threading works
    serversocket.listen(1)
    print("CATAN SERVER STARTED\nWaiting for connctions...")
    while True:
        # establish a connection

        client_conn,addr = serversocket.accept()

        print("Got a connection from %s" % str(addr))
        thread_id = start_new_thread(catan_client, (client_conn,))
        connections.append((client_conn, addr))

    serversocket.close()


'''
UNIVERSAL ERROR CODES:

-1 : Invalid location. Location does not exist on the map
-2: Occupied space. Another player is located here
-3: Adjacent Player. A player is on an adjacent object.
'''
