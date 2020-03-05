#===============================================
#FILE PURPOSE:
#  1. This file contains all class definitions and functions that instantiate one of
#  the created classes.
#===============================================

#===============================================
#BUG SECTION:
#===============================================

#===============================================
import random
import items
import math

# do the things in the init method execute in order? Because if they do this will work like a charm.
class Game:
    def __init__(self, conns): #conns are a list of connections... Should I save conns as an attribute of the game class? or player? Player seems to make more sense to me.
        #self.player_conns = player_conns # need this for multiplayer?
        #self.conns = conns

        #self.first_game_menu(conn)
        self.b = self.init_board()
        self.node_list = self.init_nodes()
        self.road_list = self.init_roads()
        self.game_robber = self.init_robber()
        self.dev_cards = self.init_dev_cards()


        if len(conns) == 1:
            conn = conns[0]
            self.first_game_menu(conn)
            self.player_list = self.init_players(conn)
            self.pts_to_win = self.declare_pts_to_win(conn)
            self.curr_player = self.player_list[0]
            self.play(conns)
        else:
            # this is where the multiplayer code is going to go.
            # okay, don't make life harder than it already is, just iterate over the connections and go in turns.

            self.player_list = self.init_multiplayer(conns)
            self.pts_to_win = self.declare_pts_to_win(conns[0])
            self.curr_player = self.player_list[0]
            self.play(conns)


    #===============================================
    #COMMUNICATION FUNCTIONS - Functions for communicating between clients and server
    #===============================================
    def catan_print(self, conn, given_str):
        conn.send(given_str.encode('ascii'))

    def catan_sendall(self, conns, given_str):
        for conn in conns:
            conn.send(given_str.encode('ascii'))


    def catan_read(self, conn, size=1024):
        s = conn.recv(size).decode('ascii').strip()
        return s

    def next_player(self): # need to get the index of the current player before going to the next one.
        i = self.player_list.index(self.curr_player)
        self.curr_player = self.player_list[(i+ 1) % len(self.player_list)]

    #===============================================
    # PRINTING FUNCTIONS - Functions for formating strings/output to user.
    #===============================================

    def display_credits(self, conn):
        self.catan_print(conn,'''
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
        reply = self.catan_read(conn)
        return reply

    def explain_rules(self, conn):
        self.catan_print(conn,'''
        Here are the rules for Catan:


        Please press Enter to go back to the main menu

        ''')
        reply = self.catan_read(conn)
        return reply

    def display_main_menu(self):
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

    def show_board(self):
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

    							  '''.format(str(self.b.tiles[2].number).ljust(2, ' '),str(self.b.tiles[2].resource),str(self.b.tiles[2].id).ljust(2, ' '),str(self.b.tiles[1].number).ljust(2, ' '),
    							  str(self.b.tiles[6].number).ljust(2, ' '),str(self.b.tiles[1].resource),str(self.b.tiles[6].resource),str(self.b.tiles[1].id).ljust(2, ' '), str(self.b.tiles[6].id).ljust(2, ' ')
    							  ,str(self.b.tiles[0].number).ljust(2, ' '),str(self.b.tiles[5].number).ljust(2, ' '),str(self.b.tiles[11].number).ljust(2, ' '), str(self.b.tiles[0].resource),
    							  str(self.b.tiles[5].resource),str(self.b.tiles[11].resource),str(self.b.tiles[0].id).ljust(2, ' '),str(self.b.tiles[5].id).ljust(2, ' '),str(self.b.tiles[11].id).ljust(2, ' '),
    							  str(self.b.tiles[4].number).ljust(2, ' '),str(self.b.tiles[10].number).ljust(2, ' '),str(self.b.tiles[4].resource),str(self.b.tiles[10].resource),
    							  str(self.b.tiles[4].id).ljust(2, ' '),str(self.b.tiles[10].id).ljust(2, ' '),str(self.b.tiles[3].number).ljust(2, ' '),str(self.b.tiles[9].number).ljust(2, ' '),str(self.b.tiles[15].number).ljust(2, ' '),
    							  str(self.b.tiles[3].resource),str(self.b.tiles[9].resource),str(self.b.tiles[15].resource),str(self.b.tiles[3].id).ljust(2, ' '),
    							  str(self.b.tiles[9].id).ljust(2, ' '),str(self.b.tiles[15].id).ljust(2, ' '),str(self.b.tiles[8].number).ljust(2, ' '),str(self.b.tiles[14].number).ljust(2, ' '),str(self.b.tiles[8].resource)
    							  ,str(self.b.tiles[14].resource),str(self.b.tiles[8].id).ljust(2, ' '),str(self.b.tiles[14].id).ljust(2, ' '),str(self.b.tiles[7].number).ljust(2, ' '),str(self.b.tiles[13].number).ljust(2, ' ')
    							  ,str(self.b.tiles[18].number).ljust(2, ' '),str(self.b.tiles[7].resource),str(self.b.tiles[13].resource),str(self.b.tiles[18].resource),
    							  str(self.b.tiles[7].id).ljust(2, ' '),str(self.b.tiles[13].id).ljust(2, ' '),str(self.b.tiles[18].id).ljust(2, ' '),str(self.b.tiles[12].number).ljust(2, ' '),str(self.b.tiles[17].number).ljust(2, ' '),
    							  str(self.b.tiles[12].resource),str(self.b.tiles[17].resource),str(self.b.tiles[12].id).ljust(2, ' '),str(self.b.tiles[17].id).ljust(2, ' '),
    							  str(self.b.tiles[16].number).ljust(2, ' '),str(self.b.tiles[16].resource),str(self.b.tiles[16].id).ljust(2, ' '), self.node_list[0].status(),
    							   self.node_list[1].status(),self.node_list[2].status(),self.node_list[3].status(),
    							   self.node_list[4].status(),self.node_list[5].status(),self.node_list[6].status(),
    							   self.node_list[7].status(),self.node_list[8].status(),self.node_list[9].status(),
    							   self.node_list[10].status(),self.node_list[11].status(),self.node_list[12].status(),
    							   self.node_list[13].status(),self.node_list[14].status(),self.node_list[15].status(),
    							   self.node_list[16].status(),self.node_list[17].status(),self.node_list[18].status(),
    							   self.node_list[19].status(),self.node_list[20].status(),self.node_list[21].status(),
    							   self.node_list[22].status(),self.node_list[23].status(),self.node_list[24].status(),
    							   self.node_list[25].status(),self.node_list[26].status(),self.node_list[27].status(),
    							   self.node_list[28].status(),self.node_list[29].status(),self.node_list[30].status(),
    							   self.node_list[31].status(),self.node_list[32].status(),self.node_list[33].status(),
    							   self.node_list[34].status(),self.node_list[35].status(),self.node_list[36].status(),
    							   self.node_list[37].status(),self.node_list[38].status(),self.node_list[39].status(),
    							   self.node_list[40].status(),self.node_list[41].status(),self.node_list[42].status(),
    							   self.node_list[43].status(),self.node_list[44].status(),self.node_list[45].status(),
    							   self.node_list[46].status(),self.node_list[47].status(),self.node_list[48].status(),
    							   self.node_list[49].status(),self.node_list[50].status(),self.node_list[51].status(),
    							   self.node_list[52].status(),self.node_list[53].status(),self.game_robber.is_on_tile(3)
    							   ,self.game_robber.is_on_tile(2),self.game_robber.is_on_tile(7),self.game_robber.is_on_tile(1),self.game_robber.is_on_tile(6)
    							   ,self.game_robber.is_on_tile(12),self.game_robber.is_on_tile(5),self.game_robber.is_on_tile(11),self.game_robber.is_on_tile(4)
    							   ,self.game_robber.is_on_tile(10),self.game_robber.is_on_tile(16),self.game_robber.is_on_tile(9),self.game_robber.is_on_tile(15)
    							   ,self.game_robber.is_on_tile(8),self.game_robber.is_on_tile(14),self.game_robber.is_on_tile(19),self.game_robber.is_on_tile(13),self.game_robber.is_on_tile(18)
    							   ,self.game_robber.is_on_tile(17),self.road_list[0].show_road(),self.road_list[1].show_road()
    							   ,self.road_list[2].show_road(),self.road_list[3].show_road(),self.road_list[4].show_road()
    							   ,self.road_list[5].show_road(),self.road_list[6].show_road(),self.road_list[7].show_road()
    							   ,self.road_list[8].show_road(),self.road_list[9].show_road(),self.road_list[10].show_road()
    							   ,self.road_list[11].show_road(),self.road_list[12].show_road(),self.road_list[13].show_road()
    							   ,self.road_list[14].show_road(),self.road_list[15].show_road(),self.road_list[16].show_road()
    							   ,self.road_list[17].show_road(),self.road_list[18].show_road(),self.road_list[19].show_road()
    							   ,self.road_list[20].show_road(),self.road_list[21].show_road(),self.road_list[22].show_road()
    							   ,self.road_list[23].show_road(),self.road_list[24].show_road(),self.road_list[25].show_road()
    							   ,self.road_list[26].show_road(),self.road_list[27].show_road(),self.road_list[28].show_road()
    							   ,self.road_list[29].show_road(),self.road_list[30].show_road(),self.road_list[31].show_road()
    							   ,self.road_list[32].show_road(),self.road_list[33].show_road(),self.road_list[34].show_road()
    							   ,self.road_list[35].show_road(),self.road_list[36].show_road(),self.road_list[37].show_road()
    							   ,self.road_list[38].show_road(),self.road_list[39].show_road(),self.road_list[40].show_road()
    							   ,self.road_list[41].show_road(),self.road_list[42].show_road(),self.road_list[43].show_road()
    							   ,self.road_list[44].show_road(),self.road_list[45].show_road(),self.road_list[46].show_road()
    							   ,self.road_list[47].show_road(),self.road_list[48].show_road(),self.road_list[49].show_road()
    							   ,self.road_list[50].show_road(),self.road_list[51].show_road(),self.road_list[52].show_road()
    							   ,self.road_list[53].show_road(),self.road_list[54].show_road(),self.road_list[55].show_road()
    							   ,self.road_list[56].show_road(),self.road_list[57].show_road(),self.road_list[58].show_road()
    							   ,self.road_list[59].show_road(),self.road_list[60].show_road(),self.road_list[61].show_road()
    							   ,self.road_list[62].show_road(),self.road_list[63].show_road(),self.road_list[64].show_road()
    							   ,self.road_list[65].show_road(),self.road_list[66].show_road(),self.road_list[67].show_road()
    							   ,self.road_list[68].show_road(),self.road_list[69].show_road(),self.road_list[70].show_road()
    							   ,self.road_list[71].show_road())
    	return to_print


    def print_dev_cards(self, cards): #BUG: Will not send to client, also unneeded function...
        for c in cards:
            print(c)

    def player_menu(self, conn):
        self.catan_print(conn,
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
    def online_or_local(conn):
        self.catan_print(conn,
    '''
Would you like to play online or locally?

            1. Online
            2. Local
    '''
        )

    #===============================================
    # INITIALIZATION FUNCTIONS - Setting up an instance of the game
    #===============================================

    def init_multiplayer(self, conns):

        color_options = ["Red", "Yellow", "Purple", "Green", "Cyan", "Tan"]
        player_list = []
        for conn in conns:
            template = "Please Enter your player name\n> "
            self.catan_print(conn, template)
            name = self.catan_read(conn)

            p_color =  color_options.pop(self.player_choose_color(conn, color_options)-1)
            self.catan_print(conn, "You selected: " + p_color + "\n")
            color = p_color[0].lower()
            player_list.append(Player(conn, name.strip(),color)) # should I add conn as an attribute of the Player? I feel like i should.
        return player_list


    def init_players(self, conn):
        try:
            player_list = []
            self.catan_print(conn, "Please enter the number of players\n> ")

            num_players = int(self.catan_read(conn))
            i = 0
            color_options = ["Red", "Yellow", "Purple", "Green", "Cyan", "Tan"]

            while i < num_players:
                template = "Please Enter Player " + str((i + 1)) + "'s name\n> "
                self.catan_print(conn, template)
                name = self.catan_read(conn)

                p_color =  color_options.pop(self.player_choose_color(conn, color_options)-1)
                self.catan_print(conn, "You selected: " + p_color + "\n")
                color = p_color[0].lower()
                player_list.append(Player(conn, name.strip(), color))
                i+=1

            return player_list

        except ValueError:
            catan_print(conn, "You must enter an integer")
            return

        except IndexError:
            catan_print(conn, "You must enter one of the provided options")
            return


    def player_choose_color(self, conn, color_options):
            self.catan_print(conn, "Which color will you be?\n")
            i = 1
            for c in color_options:
                color_format = "\t" + str(i) + ". " + c + "\n"
                self.catan_print(conn, color_format)
                i += 1
            try:
                self.catan_print(conn, "Chose the number of the color you'd like.\n> ")
                choice = int(self.catan_read(conn))
                return choice

            except ValueError:
                self.catan_print(conn, "You must enter an integer.") # this exception handling might not work...
                choice = self.player_choose_color(conn, color_options) # I don't want to call this recursively, but im hacking it together.
                return choice


    def random_tile(self, id):
        tile_r = ""
        tile_n = -1

        x = random.randint(1, 5)
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

        tile_n = self.roll_dice()
        while(tile_n == 7):
            tile_n = self.roll_dice()
        rand_tile = Tile(tile_r, tile_n, id)
        return rand_tile

    def init_board(self):
        b = Board()
        for i in range(1,20):
            b.tiles.append(self.random_tile(i))
        return b

    def create_nodes(self):
    	nodes = []
    	for x in range(1,55):
    		nodes.append(Node(x))
    	return nodes

    def init_nodes(self):
        x = self.create_nodes()
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


    def init_roads(self):
    	road_list = []
    	id = 0
    	for n in self.node_list:
    		for thing in n.adj_nodes:
    			if n.id < thing:#class Player
    				new_road = Road(n.id,thing,id)
    				road_list.append(new_road)
    				id+=1
    	return road_list

    def init_dev_cards(self):
        dev_cards = []
        for i in range(0,25):
            if i<14:
                new_card = Dev_Card("Knight")
                dev_cards.append(new_card)
            elif i<19:
                new_card = Dev_Card("Victory Point")
                dev_cards.append(new_card)
            elif i<21:
                new_card = Dev_Card("Year of Plenty")
                dev_cards.append(new_card)
            elif i<23:
                new_card = Dev_Card("Road Building")
                dev_cards.append(new_card)
            else:
                new_card = Dev_Card("Monopoly")
                dev_cards.append(new_card)
        return dev_cards


    def init_robber(self):
    	r = Robber(random.randint(1, 20))
    	return r

    def declare_pts_to_win(self, conn):
        try:
            self.catan_print(conn, "Enter the Amount of Points Required to Win\n> ")
            pts_to_win = int(self.catan_read(conn))
            return pts_to_win
        except ValueError:
            self.catan_print(conn, "You must provide an integer")

    def place_initial(self, conns):
        i = 0
        while i < len(conns):
            self.catan_sendall(conns, "\n" + self.curr_player.p_name.strip() + " is placing their first settlement\n")

            # FIRST SETTLEMENT
            self.server_build_item(conns, "settlement", True)
            self.catan_sendall(conns, self.show_board())


            # FIRST ROAD
            self.catan_sendall(conns, "\n" + self.curr_player.p_name.strip() + " is placing their first road\n")
            self.server_build_item(conns, "road", True)
            self.catan_sendall(conns, self.show_board())

            i += 1
            self.next_player()

        i = 0
        while i < len(conns):
            self.catan_sendall(conns, "\n" + self.curr_player.p_name + " is placing their second settlement\n")
            self.server_build_item(conns, "settlement", True)
            self.catan_sendall(conns, self.show_board())

            # SECOND ROAD
            self.catan_sendall(conns, "\n" + self.curr_player.p_name.strip() + " is placing their second road\n")
            self.server_build_item(conns, "road", True)
            self.catan_sendall(conns, self.show_board())

            # Go back one player.
            i += 1
            index = self.player_list.index(self.curr_player)
            self.curr_player = self.player_list[(index - 1) % len(self.player_list)]


        result = items.give_resources(0, self, True) # I don't know if I can pass the entire object to one of its methods like this. I can!
        self.catan_sendall(conns, result)


    #================================================
    # TRADING FUNCTIONS
    #================================================

    def trade_resources(player, trade_to, want, offer):
        for r in offer:
            player.p_hand.remove(r)
            trade_to.p_hand.append(r)

        for r in want:
            player.p_hand.append(r)
            trade_to.p_hand.remove(r)

    def trade_accepted(self, conn, trade_to, want, offer):
        catan_print(conn, trade_to.p_name + ", " + self.curr_player.p_name + " has offered you: " )
        catan_print(conn, offer + "\n")
        catan_print(conn, "In exchange for: ")
        catan_print(conn, want + "\n")
        choice = ""
        while choice == "":
            catan_print(conn, "Do you want to accept this trade? (y/n)\n> ")
            choice = catan_read(conn)
            if choice not in "yn": #BUG, they could enter "yn" and break the program
                catan_print(conn, "You must enter 'y' or 'n'")
                choice = ""
                continue

        if choice == "y":
            return True
        elif choice == "n":
            return False

    # Add function for trading with ports here.

    #================================================
    # NORMAL TURN FUNCTIONS
    #================================================

    def first_game_menu(self, conn):
        start_game = False
        while not start_game:
            msg = self.display_main_menu()
            self.catan_print(conn, msg)
            selection = self.catan_read(conn)
            selection = int(selection)
            if selection == 1:
                start_game = True
            elif selection == 2:
                self.explain_rules(conn)
                continue
            elif selection == 3:
                self.display_credits(conn)
                continue
            else:
                self.catan_print(conn, "Please enter an appropriate value")

    def play(self,conns):
        # okay, they want to play a game now. Initalize a locally played game
        msg = self.show_board()
        self.catan_sendall(conns, msg)
        self.place_initial(conns)

        winner = False
        while winner != True:
            winner = self.player_turn(conns)
            if winner:
                break
            self.next_player()
        self.catan_print(conn, "\nWINNER: " + self.curr_player.p_name + "\n")

    def player_turn(self, conns):
        self.catan_sendall(conns, "\nIt's " + self.curr_player.p_name + "'s turn!\n")

        self.catan_print(self.curr_player.conn, "Press Enter to Roll Die")
        user_input = self.catan_read(self.curr_player.conn)

        roll = self.roll_dice()
        self.catan_sendall(conns, "\n" + str(roll) + " has been rolled")
        self.catan_sendall(conns, items.give_resources(roll, self)) #Apparent, we can pass an entire object to one of its own methods.


        #Check to see if robber() should be called
        if roll == 7:
            self.game_robber.rob_players(self.curr_player.conn, self) #BUG? can i give the entire object as an argument to one of it's methods?

        #Player Selects an Option
        selection = -1
        while selection != 0:
            self.player_menu(self.curr_player.conn)
            try:
                self.catan_print(self.curr_player.conn, "Please Select One\n"+ self.curr_player.p_name + "> ")
                selection = int(self.catan_read(self.curr_player.conn))
            except ValueError:
                self.catan_print(self.curr_player.conn, "You must enter a number corresponding to an option")
                selection = -1

            if selection == 1:
                self.catan_print(self.curr_player.conn, self.curr_player.show_hand())

            elif selection == 2:
                self.server_build_item(conns, "road")


            elif selection == 3:
                self.server_build_item(conns, "settlement")

            elif selection == 4:
                self.server_build_item(conns, "city")

            elif selection == 5:
                result = items.build_dev_card(self.curr_player, self.dev_cards)
                if isinstance(result, str):
                    self.catan_print(self.curr_player.conn, result)
                elif isinstance(result, int):
                    self.handle_errors(self.curr_player.conn, result)


            elif selection == 6:
                self.catan_print(self.curr_player.conn, "Players:\n")
                counter  = 1
                for p in self.player_list:
                    self.catan_print(self.curr_player.conn, "\t" + str(counter) + ". " + p.p_name + "\n")
                    counter += 1
                self.catan_print(self.curr_player.conn, "\t" + str(counter) + ". Offer trade to everyone\n")
                self.catan_print(self.curr_player.conn, "Who do you want to trade with?\n" + self.curr_player.p_name + "> ")
                option = int(self.catan_read(self.curr_player.conn)) # BUG: gonna have to do error checking on this too... Giving anything other than an int breaks it.
                trade_to = self.player_list[option-1]
                self.catan_print(self.curr_player.conn, "What resource(s) do you want?\n" + self.curr_player.p_name + "> ")
                want = self.catan_read(self.curr_player.conn)
                self.catan_print(self.curr_player.conn, "What resource(s) are you offering in exchange?\n" + self.curr_player.p_name + "> ")
                offer = self.catan_read(self.curr_player.conn)

                if option <= len(self.player_list):
                    if self.curr_player.has_resources(offer):

                        want_to_trade = self.trade_accepted(trade_to.conn, trade_to, want, offer)
                        they_have_resources = trade_to.has_resources(want)
                        if want_to_trade and they_have_resources:
                            self.trade_resources(player, trade_to, want, offer)
                    else:
                        self.catan_print(self.curr_player.conn, "You don't have those resources to offer...")
                elif trade_to == len(player_list) + 1:
                    self.catan_print(self.curr_player.conn, "Trade to all players is coming soon")
                else:
                    self.catan_print(self.curr_player.conn, "Invalid option")

            elif selection == 7:
                self.catan_print(self.curr_player.conn, "What resource do you want?\n" + self.curr_player.p_name + "> ")
                want = self.catan_read(self.curr_player.conn)
                self.catan_print(self.curr_player.conn, "What resource will you be trading 4 of?\n" + self.curr_player.p_name + "> ")
                give = self.catan_read(self.curr_player.conn)
                if player.has_resources(give*4):
                    self.curr_player.p_hand.remove(give)
                    self.curr_player.p_hand.remove(give)
                    self.curr_player.p_hand.remove(give)
                    self.curr_player.p_hand.remove(give)
                    self.curr_player.p_hand.append(want)
                    self.catan_sendall(conns, self.curr_player.p_name + " traded with the bank!\n")

                else:
                    self.catan_print(self.curr_player.conn, "You don't have enough of that resource to trade...")

            elif selection == 8:
                self.catan_print(self.curr_player.conn, "Trade using a port\n")

            elif selection == 9:
                self.catan_print(self.curr_player.conn, self.show_board())

            elif selection == 10:
                self.catan_print(self.curr_player.conn, self.curr_player.show_dev_cards())


            elif selection == 11:
                if self.curr_player.p_dev_cards == []:
                    self.catan_print(self.curr_player.conn, "You have no development cards!!\n")
                    continue
                self.catan_print(conn, "Please select a dev_card: \n")
                msg_to_client = self.curr_player.show_dev_cards()
                self.catan_print(self.curr_player.conn, msg_to_client)
                num = int(self.catan_read(self.curr_player.conn)) # this will break if they give something other than an int.
                card_to_play = self.curr_player.p_dev_cards[num-1]
                card_to_play.play_dev_card(self.curr_player.conn, self) # Again, can I pass the whole game as an argument? Or no?

            elif selection == 12:
                self.catan_print(self.curr_player.conn, player.show_victory_pts())

            elif selection == 0:
                pass


            if int(self.curr_player.show_victory_pts()) >= self.pts_to_win:
                return True

        return False


    def roll_dice(self):
        x = random.randint(1, 6)
        y = random.randint(1, 6)
        return x + y


    def shuffle(self, a_list):
        new_l = []
        max_i = len(a_list)-1

        for i in range(0, len(a_list)):
            random_index = random.randint(0, max_i)
            new_l.append(a_list.pop(random_index))
            max_i -= 1
            i += 1
        return new_l

    #====================================================
    # SHITTY FUNCTIONS - These are ass, I'm so sorry. Don't read these. Just let them do their job for now.
    #====================================================
    # this is the worst function in the history of functions, probably ever.
    def handle_errors(self, conn, result):
        if result == -1:
            self.catan_print(conn, "That's an invalid location\n")
        elif result == -2:
            self.catan_print(conn, "Someone is already on that space!!\n")
        elif result == -3:
            self.catan_print(conn, "Someone is on an adjacent space!!\n")
        elif result == -4:
            self.catan_print(conn, "The correct format is tile,corner\n")
            self.catan_print(conn, "EXAMPLE: 1,2\n")
        elif result == -5:
            self.catan_print(conn, "Your road must be connected to one of your settlements\n")
        elif result == -6:
            self.catan_print(conn,"Not enough resources!!\n")
        elif result == -7:
            self.catan_print(conn,"Already a city!! Cannot upgrade\n")
        elif result == -8:
            self.catan_print(conn,"Cannot upgrade unsettled location...\n")
        elif result == -99:
            self.catan_print(conn, "Invalid input... Please try again.\n")
        else:
            self.catan_print(conn, "That caused some unknown error, please try to not do that again :)\n")

    #this is the second worst function in the history of functions, probably ever.
    def server_build_item(self, conns, item, init = False): #change from conn to conns

        # There's a way to get this down into one thing. More DRY, but i can't figure it out rn.
        # PARTIALLY IMPLEMENTED
        if item == "city":
            catan_print(self.curr_player.conn, "Where would you like to upgrade into a city?\n" + self.curr_player.p_name + "> ")
            location = self.catan_read(self.curr_player.conn)
            result = items.build_city(self.curr_player, location, self.node_list)
            if isinstance(result, int):
                handle_errors(self.curr_player.conn, result)
            elif isinstance(result, str):
                catan_print(self.curr_player.conn, result)

        # There's a way to get this down into one thing. More DRY, but i can't figure it out rn.
        # PARTIALLY IMPLEMENTED
        elif item == "settlement":
            if init:
                settled = False
                while settled == False:
                    self.catan_print(self.curr_player.conn, "Where do you want to place your settlement?\n" + self.curr_player.p_name + "> ")
                    location = self.catan_read(self.curr_player.conn)
                    result = items.build_settlement(self.curr_player, location, self.node_list, True)
                    print(result)
                    if isinstance(result, int):
                        self.handle_errors(self.curr_player.conn, result)
                    elif isinstance(result, str):
                        self.catan_print(self.curr_player.conn, result)
                        settled = True


            else:
                self.catan_print(self.curr_player.conn, "Where do you want to place your settlement?\n" + self.curr_player.p_name + "> ")
                location = self.catan_read(self.curr_player.conn)
                result = items.build_settlement(self.curr_player, location, self.node_list)
                if isinstance(result, int):
                    self.handle_errors(self.curr_player.conn, result)
                elif isinstance(result, str):
                    self.catan_print(self.curr_player.conn, result)

        elif item == "road": # not yet written for anything other than initial setup
            if init:
                first_road = False
                while first_road == False:
                    self.catan_print(self.curr_player.conn, "Where do you want to start your road?\n" + self.curr_player.p_name + "> ")
                    n1 = self.catan_read(self.curr_player.conn)
                    self.catan_print(self.curr_player.conn, "Where do you want to end your road?\n" + self.curr_player.p_name + "> ")
                    n2 = self.catan_read(self.curr_player.conn)
                    result = items.build_road(self.curr_player, n1, n2, self.node_list, self.road_list, self.player_list, True) # just pass the parts and let the function work
                    if isinstance(result, int):
                        self.handle_errors(self.curr_player.conn, result)
                    elif isinstance(result, str):
                        self.catan_print(self.curr_player.conn, result)
                        self.catan_sendall(conns, self.show_board())
                        first_road = True
            else:
                self.catan_print(self.curr_player.conn, "Where do you want to start your road?\n" + self.curr_player.p_name + "> ")
                n1 = self.catan_read(self.curr_player.conn)
                self.catan_print(self.curr_player.conn, "Where do you want to end your road?\n" + self.curr_player.p_name + "> ")
                n2 = self.catan_read(self.curr_player.conn)
                result = items.build_road(self.curr_player, n1, n2, self.node_list, self.road_list, self.player_list)
                if isinstance(result, int):
                    self.handle_errors(self.curr_player.conn, result)
                elif isinstance(result, str):
                    self.catan_print(self.curr_player.conn, result)

        elif item == "dev card":
            self.catan_print(self.curr_player.conn, "Where do you want to start your road?\n" + self.curr_player.p_name + "> ")
            n1 = self.catan_read(self.curr_player.conn)
            self.catan_print(self.curr_player.conn, "Where do you want to end your road?\n" + self.curr_player.p_name + "> ")
            n2 = self.catan_read(self.curr_player.conn)
            result = items.build_dev_card(self.curr_player)
            if isinstance(result, int):
                self.handle_errors(self.curr_player.conn, result)
            elif isinstance(result, str):
                self.catan_print(self.curr_player.conn, result)









class Player:
    def __init__(self, conn, name, color):
        self.conn = conn
        self.p_name = name
        self.p_hand = [] # should be a list of characters
        self.p_color = color # Red, Yellow, Purple, Green, Cyan, Tan
        self.p_victory_pts = 0
        self.p_dev_cards = []
        self.p_played_dev_cards = []
        self.p_order = -1
        self.has_largest_army = False
        self.has_longest_road = False
        self.road_chains = [] #road ids: a list of lists that contain the chains a player has
        self.split_roads = [] #contains the nodes that will split a players chains

    def present(self):
        print(self.p_name)

    def show_hand(self):
        if len(self.p_hand) == 0:
            return "You have no cards"
        else:
            return ''.join(self.p_hand)

    def show_dev_cards(self):
        if len(self.p_dev_cards) == 0:
            return "You have no development cards"
        else:
            counter = 1

            for i in self.p_dev_cards:
                print(str(counter) + "\t" + str(i)) # idk if i is gonna work like That
                counter += 1

    def show_played_dev_cards(self):
        if len(self.p_played_dev_cards) == 0:
            print("You have no played development cards")
        else:
            counter = 1
            for i in self.p_played_dev_cards:
                print("\t" + str(i)) # idk if i is gonna work like That
                counter += 1
            return msg_to_client + "> "

    def has_resources(self, resources_str):
        resource_list = ["B","L","W","S","O"]
        for r in resource_list:
            if resources_str.count(r) > self.p_hand.count(r):
                return False
        return True

    def show_victory_pts(self):
        return str(self.p_victory_pts)

    def has_largest_army(self):
        return self.has_largest_army

    def has_longest_road(self):
        return self.has_longest_road

    def count_road(self):
        max_road = 0
        for i in self.road_chains:
            if len(i) > max_road:
                max_road = len(i)
        return max_road


    def count_knights(self):
        counter = 0
        for i in self.p_played_dev_cards:
            if i.card_type == "Knight":
                counter += 1
        return counter


class Board:
    def __init__(self):
        self.tiles = [] #Is just a list of tiles...

class Tile:

    def __init__(self, resource, number, id):
        self.resource = resource
        self.number = number
        self.id = id

class Robber:

    def __init__(self, first_tile):
        self.on_tile = first_tile

    def is_on_tile(self, tile_num):
        if self.on_tile == tile_num:
            return "!"
        else:
            return " "

    def rob_players(self, conn, a_game):
        a_game.catan_print(conn, "\nROBBER HAS BEEN ROLLED\n") # going to have to include this where it's called

        # Loop checks to see if any players have 7 or more cards
        for p in a_game.player_list:
            if len(p.p_hand) >= 7:
                num_to_discard = math.ceil(len(p.p_hand)/2)
                discard = ""
                has_cards = False
                while len(discard) != num_to_discard or has_cards == False:
                    a_game.catan_print(conn, p.p_name + " this is your current hand: ")
                    i.show_hand()
                    a_game.catan_print(conn, p.p_name + " Please discard " + str(num_to_discard) + " cards\n> ")
                    discard = a_game.catan_read(conn)
                    if len(discard) > num_to_discard:
                        a_game.catan_print(conn, "You have discarded more cards than necessary.")

                    elif len(discard) < num_to_discard:
                        a_game.catan_print(conn, "You didn't discard enough cards... try again.")

                    if p.p_hand.count("O") >= list(discard).count("O") and p.p_hand.count("B") >= list(discard).count("B") and p.p_hand.count("S") >= list(discard).count("S") and p.p_hand.count("W") >= list(discard).count("W") and p.p_hand.count("L") >= list(discard).count("L"):
                        has_cards = True

                    else:
                        has_cards = False
                        a_game.catan_print(conn, "You do not have those cards")
                for card in discard:
                    p.p_hand.remove(card)
                a_game.catan_print(conn, "\n" + p.p_name + " this is your new hand: \n")
                p.show_hand()

        self.move_robber(conn, a_game)

    def move_robber(self, conn, a_game):
        knight_placed = False
        while knight_placed == False:
            a_game.catan_print(conn, "Which tile will you place the robber on?\n> ")
            t = int(a_game.catan_read(conn))
            if t == a_game.game_robber.on_tile: # can i get the board this way or does it have to be an argument? Maybe just put it in config?
                a_game.catan_print(conn, "You must put the robber on a new tile.\n")
                continue
            else:
                # maybe the tile that the robber is on should be an attribute of the robber, because im going to have to iterate over all the times to "undo" the old robber.
                a_game.game_robber.on_tile = t
                knight_placed = True



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

    def status(self):
        if self.owns_node == "":
            return "."
        else:
            return self.owns_node

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

    def __repr__(self):
        return "Node: " + str(self.id)

    def __str__(self):
        return self.owns_node


# options are Knight (14), Road Building(2), Year of Plenty(2), Monopoly(2), Victory Point (5)
class Dev_Card:
    def __init__(self, card_type, can_be_played = False):
        self.card_type = card_type
        self.can_be_played = can_be_played

    def __str__(self):
        return self.card_type

    def play_dev_card(self, conn, a_game): # want this to take a game object... I'll fix this later

        # Partially Implemented
        if self.card_type == "Knight":
            catan_print(conn, a_game.curr_player.p_name + " played a development card: ")
            catan_print(conn, self.card_type + "\n")
            move_robber(conn, a_game.game_robber)
            # steal a card from a player.

        #DONE
        elif self.card_type == "Road Building":
            catan_print(conn, a_game.curr_player.p_name + " played a development card: ")
            catan_print(conn, self.card_type + "\n")
            a_player.p_hand.append("B")
            a_player.p_hand.append("L")
            a_player.p_hand.append("B")
            a_player.p_hand.append("L")

            # force the player to build two roads
            roads_placed = 0
            while roads_placed != 2:
                a_game.catan_print(conn, "Where do you want to start your road?\n> ")
                n1 = a_game.catan_read(conn)
                a_game.catan_print(conn, "Where do you want to end your road?\n> ")
                n2 = a_game.catan_read(conn)
                if items.build_road(curr_player, n1, n2, node_list, road_list) == None:
                    continue
                else:
                    roads_placed += 1

        #DONE
        elif self.card_type == "Year of Plenty":
            a_game.catan_print(conn, a_game.curr_player.p_name + " played a development card: ")
            a_game.catan_print(conn, self.card_type + "\n")

            added_cards = 0
            while added_cards != 2: # even if this loo
                a_game.catan_print(conn, "What resource would you like? Resource (" + str(added_cards+1) + "/2)\n> ")
                wanted_card = a_game.catan_read(conn)
                if wanted_card.upper() in "BLSWO":
                        a_game.curr_player.p_hand.append(wanted_card.upper())
                        added_cards += 1
                else:
                    catan_print(conn, wanted_card + " is not a valid resource")

        #DONE
        elif self.card_type == "Monopoly":
            a_game.catan_print(conn, a_game.curr_player.p_name + " played a development card: ")
            a_game.catan_print(conn, self.card_type + "\n")
            got_resources = False
            while got_resources == False:
                a_game.catan_print(conn, "What resource would you like?\n> ")
                wanted_card = a_game.catan_read(conn)
                if wanted_card.upper() in "BLSWO":
                    num_taken = 0
                    for p in a_game.player_list: # wait, this actually takes cards from the player using it too, since they're in player list. I guess that's okay if i add them back?
                        for resource in p.p_hand:
                            if resource == wanted_card.upper():
                                p.p_hand.remove(resource)
                                num_taken += 1

                    for num in range(0, num_taken):
                        a_game.curr_player.p_hand.append(wanted_card.upper())

                    catan_print(conn, a_game.curr_player.p_name + " took all everyone's " + wanted_card.upper())
                    got_resources = True

                else:
                    a_game.catan_print(conn, wanted_card + " is not a valid resource")


        #DONE
        elif self.card_type == "Victory Point":
            a_game.catan_print(conn, "Victory point card played!!\n") # make sure this is only adding a victory point once, not now and when they get it.
            a_game.curr_player.p_victory_pts += 1 # I don't want to tell anyone else that this was played.

        else:
            a_game.catan_print(conn, "Not a known development card type")


class Road:
    def __init__(self, start_n, end_n, id):
        self.id = id
        self.owns_road = ""
        self.start_n = start_n # id of starting node
        self.end_n = end_n # id of ending node

    def is_owned(self):
        if self.owns_road == "":
            return False
        else:
            return True

    def show_road(self):
        if self.owns_road == "":
            return "."
        else:
            return self.owns_road

    def __repr__(self):
        return "Road: " + str(str(self.start_n) + " " +  str(self.end_n) + " " + str(self.id))


class Port:
    def __init__(self, type, location):
        self.type = type
        self.location = location #List of nodes identify where it is
        self.player_on = ""

    def is_player_on(self, player):
        if self.player_on == player.p_color:
            return True
        else:
            return False

    def __str__(self):
        if self.owns_road == "":
            return "."
        else:
            return self.owns_road
