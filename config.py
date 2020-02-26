# include all the globably needed stuff in here.

def create_nodes():
	nodes = []
	for x in range(1,55):
		nodes.append(Node(x))
	return nodes

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


def create_roads(list_of_nodes):
    roads =[]
    for n in list_of_nodes:
        for thing in n.adj_nodes:
            if n.id < thing:
                new_road = Road(n.id,thing)
                roads.append(new_road)
    return roads


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

	def __str__(self):
		return "Node: " + str(self.id)

node_list = init_nodes()
road_list = create_roads(node_list)
