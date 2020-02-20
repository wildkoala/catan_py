class Node:
	def __init__(self, id): # Just gonna have every node have an id.
		self.id = id
		self.owns_node = "" # player with a settlement or city on this node 
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

	def is_settlment():
		if self.owns_node.is_lower():
			return True
		else:
			return False

	def __str__(self):
		return "Node: " + str(self.id)


def create_nodes():
    nodes = []
    for x in range(1,55):
    	nodes.append(Node(x))
    return nodes

def print_nodes(node_list):
    for n in node_list:
    	print(n)


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
x[40].alias = [(13,3),(15,5),(17,1)]
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

print(x[32].alias)

'''
x[0].adj_nodes = 
x[1].adj_nodes = 
x[2].adj_nodes = 
x[3].adj_nodes = 
x[4].adj_nodes = 
x[5].adj_nodes = 
x[6].adj_nodes = 
x[7].adj_nodes = 
x[8].adj_nodes = 
x[9].adj_nodes = 
x[10].adj_nodes = 
x[11].adj_nodes = 
x[12].adj_nodes = 
x[13].adj_nodes = 
x[14].adj_nodes = 
x[15].adj_nodes = 
x[16].adj_nodes = 
x[17].adj_nodes = 
x[18].adj_nodes = 
x[19].adj_nodes = 
x[20].adj_nodes = 
x[21].adj_nodes = 
x[22].adj_nodes = 
x[23].adj_nodes = 
x[24].adj_nodes = 
x[25].adj_nodes = 
x[26].adj_nodes = 
x[27].adj_nodes = 
x[28].adj_nodes = 
x[29].adj_nodes = 
x[30].adj_nodes = 
x[31].adj_nodes = 
x[32].adj_nodes = 
x[33].adj_nodes = 
x[34].adj_nodes = 
x[35].adj_nodes = 
x[36].adj_nodes = 
x[37].adj_nodes = 
x[38].adj_nodes = 
x[39].adj_nodes = 
x[40].adj_nodes = 
x[41].adj_nodes = 
x[42].adj_nodes = 
x[43].adj_nodes = 
x[44].adj_nodes = 
x[45].adj_nodes = 
x[46].adj_nodes = 
x[47].adj_nodes = 
x[48].adj_nodes = 
x[49].adj_nodes = 
x[50].adj_nodes = 
x[51].adj_nodes = 
x[52].adj_nodes = 
x[53].adj_nodes = 
'''