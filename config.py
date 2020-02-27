import random
import catan_classes


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






def show_board():
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
							   node_list[52].status(),node_list[53].status(),robber.is_on_tile(3)
							   ,robber.is_on_tile(2),robber.is_on_tile(7),robber.is_on_tile(1),robber.is_on_tile(6)
							   ,robber.is_on_tile(12),robber.is_on_tile(5),robber.is_on_tile(11),robber.is_on_tile(4)
							   ,robber.is_on_tile(10),robber.is_on_tile(16),robber.is_on_tile(9),robber.is_on_tile(15)
							   ,robber.is_on_tile(8),robber.is_on_tile(14),robber.is_on_tile(19),robber.is_on_tile(13),robber.is_on_tile(18)
							   ,robber.is_on_tile(17),road_list[0].show_road(),road_list[1].show_road()
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
	print(to_print)

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

def init_ports():
	ports = []
	ports.append(catan_classes.Port("W", (node_list[49],node_list[50])))
	ports.append(catan_classes.Port("O", (node_list[36],node_list[46])))
	ports.append(catan_classes.Port("S", (node_list[14],node_list[24])))
	ports.append(catan_classes.Port("L", (node_list[2],node_list[3])))
	ports.append(catan_classes.Port("B", (node_list[7],node_list[15])))
	ports.append(catan_classes.Port("3", (node_list[5],node_list[6])))
	ports.append(catan_classes.Port("3", (node_list[26],node_list[27])))
	ports.append(catan_classes.Port("3", (node_list[39],node_list[38])))
	ports.append(catan_classes.Port("3", (node_list[52],node_list[53])))
	return ports


# GLOBALLY ACCESSIBLE VARIABLES
dev_cards = shuffle(init_dev_cards())
b = init_board()
robber = init_robber(random.randint(1, 20))
node_list = init_nodes()
road_list = init_roads(node_list)
port_list = init_ports()
player_list = []
