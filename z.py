import networkx as nx
import matplotlib.pyplot as plt


class vertice:
    def __init__(self, label, value):
        self.label = label
        self.value = value

    def __lt__(self, other):
        return self.value < other.value

    @staticmethod
    def isEqual(vertice1, vertice2):
        if vertice1.label == vertice2.label and vertice1.value == vertice2.value:
            return True
        else:
            return False

    @staticmethod
    def minimum(arg1, arg2):
        if (arg1.value < arg2.value):
            return arg1
        else:
            return arg2

    @staticmethod
    def maximum(arg1, arg2):
        if (arg1.value > arg2.value):
            return arg1
        else:
            return arg2


class simplice:
    def __init__(self, corner):
        self.corner = corner
        self.vertices = corner
        self.edges = []
        self.edges_init = []
        self.edges_frag = []
        self.fragments = []
        self.vertGraph = []
        self.vert_vertices = []
        self.vert_edges = []
        self.max_vertice = None
        self.min_vertice = None
        for elem in corner:
            if (self.max_vertice == None or elem > self.max_vertice):
                self.max_vertice = elem
            if (self.min_vertice == None or elem < self.min_vertice):
                self.min_vertice = elem

        for elem in self.corner:
            if (elem.label != self.max_vertice.label and elem.label != self.min_vertice.label):
                self.mid_vertice = elem

    def edgeExists(self, edge):
        for ed in self.edges:
            if (((ed[0].label == edge[0].label and ed[1].label == edge[1].label))
                        or ((ed[0].label == edge[1].label and ed[1].label == edge[0].label))
                    ):
                return True
        return False

    def edgeExistsInitially(self, edge):
        for ed in self.edges_init:
            if (((ed[0].label == edge[0].label and ed[1].label == edge[1].label))
                        or ((ed[0].label == edge[1].label and ed[1].label == edge[0].label))
                    ):
                return True
        return False

    def verticeInSimplice(self, vertice):
        for vert in self.vertices:
            if vert.label == vertice.label:
                return True
        return False

    def addVertice(self, new_vertice):
        try:
            self.vertices.append(new_vertice)
        except:
            self.vertices.extend(new_vertice)

    def setCorners(self, vertice_array):
        self.corner = vertice_array

    def addEdge(self, edge_tuple):
        self.edges.extend(edge_tuple)

    def insertVerticeBetween(self, edge, vertice):
        small = vertice.minimum(edge[0], edge[1])
        large = vertice.maximum(edge[0], edge[1])
        self.edges.append((small, vertice))
        self.edges.append((vertice, large))
        self.vertices.append(vertice)

        i = 0
        for entity in self.edges:
            if ((vertice.isEqual(entity[0], edge[0]) and vertice.isEqual(entity[1], edge[1]))
                    or (vertice.isEqual(entity[1], edge[0]) and vertice.isEqual(entity[0], edge[1]))):
                self.edges.pop(i)
            i = i + 1

    @staticmethod
    def commonEdges(simplice1, simplice2):
        commonList = []
        for edge1 in simplice1.edges:
            if simplice2.edgeExists(edge1):
                commonList.append(edge1)

        return commonList

    def fragmentation(self):
        for vert in self.vertices:
            for anotherVert in self.vertices:
                if (vert.label != anotherVert.label and vert.value == anotherVert.value):
                    if (not self.edgeExists((vert, anotherVert)) or not self.edgeExists((anotherVert, vert))):
                        self.edges.append((vert, anotherVert))
                        self.edges_frag.append((vert, anotherVert))

        self.edges_frag.sort(key=lambda v: v[0].value)

    def getFragments(self):
        fragArray = [[self.min_vertice]]
        fragArray.extend(self.edges_frag)
        fragArray.append([self.max_vertice])
        # for elem in fragArray:
        #     if len(elem) == 1:
        #         print(elem[0].label, elem[0].value)
        #     elif len(elem) == 2:
        #         print(elem[0].label, elem[0].value,
        #               elem[1].label, elem[1].value)

        if len(fragArray) == 2:
            a = fragment()
            a.label = self.min_vertice.value
            a.vertices = self.vertices[:]
            a.edges = self.edges[:]
            self.fragments.append(a)
            return 0

        i = 0
        while (i < len(fragArray)):
            if (len(fragArray[i]) == 1):
                if (i == 0):
                    if (fragArray[i+1][0].value < self.mid_vertice.value):
                        a = fragment()
                        a.vertices = [self.min_vertice,
                                      fragArray[i+1][0],
                                      fragArray[i+1][1]]

                        a.label = self.min_vertice.value
                        a.belongsTo = self

                        a.edges.append((self.min_vertice, fragArray[i+1][0]))
                        a.edges.append((fragArray[i+1][0], fragArray[i+1][1]))
                        a.edges.append((self.min_vertice, fragArray[i+1][1]))
                        self.fragments.append(a)

                    elif (fragArray[i+1][0].value > self.mid_vertice.value):
                        a = fragment()
                        a.vertices = [self.min_vertice,
                                      fragArray[i+1][0],
                                      fragArray[i+1][1],
                                      self.mid_vertice]

                        a.label = self.min_vertice.value
                        a.belongsTo = self

                        a.edges.append((self.min_vertice, self.mid_vertice))
                        a.edges.append((fragArray[i+1][0], fragArray[i+1][1]))

                        if self.edgeExists((self.min_vertice, fragArray[i+1][0])):
                            a.edges.append(
                                (self.min_vertice, fragArray[i+1][0]))
                            a.edges.append(
                                (self.mid_vertice, fragArray[i+1][1]))

                        elif self.edgeExists((self.min_vertice, fragArray[i+1][1])):
                            a.edges.append(
                                (self.min_vertice, fragArray[i+1][1]))
                            a.edges.append(
                                (self.mid_vertice, fragArray[i+1][0]))

                        self.fragments.append(a)

                elif (i == len(fragArray) - 1):
                    break

            elif (len(fragArray[i]) == 2):
                if (len(fragArray[i+1]) == 1):
                    if (fragArray[i][0].value > self.mid_vertice.value):
                        a = fragment()
                        a.vertices = [self.max_vertice,
                                      fragArray[i][0],
                                      fragArray[i][1]]

                        a.label = fragArray[i][0].value
                        a.belongsTo = self

                        a.edges.append((self.max_vertice, fragArray[i][0]))
                        a.edges.append((fragArray[i][0], fragArray[i][1]))
                        a.edges.append((self.max_vertice, fragArray[i][1]))
                        self.fragments.append(a)

                    elif (fragArray[i][0].value < self.mid_vertice.value):
                        a = fragment()
                        a.vertices = [self.max_vertice,
                                      fragArray[i][0],
                                      fragArray[i][1],
                                      self.mid_vertice]

                        a.label = fragArray[i][0].value
                        a.belongsTo = self

                        a.edges.append((self.mid_vertice, self.max_vertice))
                        a.edges.append((fragArray[i][0], fragArray[i][1]))

                        if self.edgeExists((self.mid_vertice, fragArray[i][0])):
                            a.edges.append((self.mid_vertice, fragArray[i][0]))
                            a.edges.append((self.max_vertice, fragArray[i][1]))

                        elif self.edgeExists((self.mid_vertice, fragArray[i][1])):
                            a.edges.append((self.mid_vertice, fragArray[i][1]))
                            a.edges.append((self.max_vertice, fragArray[i][0]))

                        self.fragments.append(a)

                elif (len(fragArray[i+1]) == 2):
                    if ((fragArray[i][0].value < self.mid_vertice.value)
                            and (fragArray[i+1][0].value < self.mid_vertice.value)):
                        a = fragment()
                        a.vertices = [fragArray[i][0],
                                      fragArray[i][1],
                                      fragArray[i+1][0],
                                      fragArray[i+1][1]]

                        a.label = fragArray[i][0].value
                        a.belongsTo = self

                        a.edges.append((fragArray[i][0], fragArray[i][1]))
                        a.edges.append((fragArray[i+1][0], fragArray[i+1][1]))

                        if self.edgeExists((fragArray[i][0], fragArray[i+1][0])):
                            a.edges.append(
                                (fragArray[i][0], fragArray[i+1][0]))
                            a.edges.append(
                                (fragArray[i][1], fragArray[i+1][1]))

                        elif self.edgeExists((fragArray[i][0], fragArray[i+1][1])):
                            a.edges.append(
                                (fragArray[i][0], fragArray[i+1][0]))
                            a.edges.append(
                                (fragArray[i][1], fragArray[i+1][1]))

                        self.fragments.append(a)

                    elif ((fragArray[i][0].value < self.mid_vertice.value)
                            and (fragArray[i+1][0].value > self.mid_vertice.value)):
                        a = fragment()
                        a.vertices = [fragArray[i][0],
                                      fragArray[i][1],
                                      fragArray[i+1][0],
                                      fragArray[i+1][1],
                                      self.mid_vertice]

                        a.label = fragArray[i][0].value
                        a.belongsTo = self

                        a.edges.append((fragArray[i][0], fragArray[i][1]))
                        a.edges.append((fragArray[i+1][0], fragArray[i+1][1]))

                        lastedge = []

                        if self.edgeExists((self.mid_vertice, fragArray[i][0])):
                            a.edges.append((self.mid_vertice, fragArray[i][0]))
                            lastedge.append(fragArray[i][1])

                        elif self.edgeExists((self.mid_vertice, fragArray[i][1])):
                            a.edges.append((self.mid_vertice, fragArray[i][1]))
                            lastedge.append(fragArray[i][0])

                        if self.edgeExists((self.mid_vertice, fragArray[i+1][0])):
                            a.edges.append(
                                (self.mid_vertice, fragArray[i+1][0]))
                            lastedge.append(fragArray[i+1][1])

                        elif self.edgeExists((self.mid_vertice, fragArray[i+1][1])):
                            a.edges.append(
                                (self.mid_vertice, fragArray[i+1][1]))
                            lastedge.append(fragArray[i+1][0])
                           

                        a.edges.append((lastedge[0], lastedge[1]))
                        self.fragments.append(a)

                    elif ((fragArray[i][0].value > self.mid_vertice.value)
                            and (fragArray[i+1][0].value > self.mid_vertice.value)):

                        a = fragment()
                        a.vertices = [fragArray[i][0],
                                      fragArray[i][1],
                                      fragArray[i+1][0],
                                      fragArray[i+1][1]]

                        a.label = fragArray[i][0].value
                        a.belongsTo = self

                        a.edges.append((fragArray[i][0], fragArray[i][1]))
                        a.edges.append((fragArray[i+1][0], fragArray[i+1][1]))

                        if self.edgeExists((fragArray[i][0], fragArray[i+1][0])):
                            a.edges.append(
                                (fragArray[i][0], fragArray[i+1][0]))
                            a.edges.append(
                                (fragArray[i][1], fragArray[i+1][1]))

                        elif self.edgeExists((fragArray[i][0], fragArray[i+1][1])):
                            a.edges.append(
                                (fragArray[i][0], fragArray[i+1][0]))
                            a.edges.append(
                                (fragArray[i][1], fragArray[i+1][1]))

                        self.fragments.append(a)

            i = i + 1

        for frag in self.fragments:
            print("FRAGMENT LABEL:", frag.label)
            for edge in frag.edges:
                print(edge[0].label, edge[0].value,
                      "-----", edge[1].label, edge[1].value)
            print("Done\n")
        print("\nOVER\n")

    def verticalGraphVertices(self):
        global vert_count
        self.fragments.sort(key=lambda v: v.label)

        i = 0
        while (i < len(self.fragments)):
            self.vert_vertices.append(
                vertice(vert_count, self.fragments[i].label))
            vert_count = vert_count - 1
            i = i + 1

        return self.vert_vertices

    def verticalGraphEdges(self):

        i = 0
        while (i < len(self.vert_vertices)):
            if (i != 0):
                self.vert_edges.append(
                    (self.vert_vertices[i-1], self.vert_vertices[i]))
            i = i + 1

        return self.vert_edges


class fragment:
    def __init__(self):
        self.vertices = []
        self.edges = []
        self.label = None
        self.belongsTo = None


def genVert(value):
    global last_vertice
    last_vertice = last_vertice - 1
    a = vertice(last_vertice, value)
    return a


def edgePresent(edgeArray):
    for ed in edgeArray:
        if (((ed[0].label == edge[0].label and ed[1].label == edge[1].label))
            or ((ed[0].label == edge[1].label and ed[1].label == edge[0].label))
            ):
            return True
        return False

def createSimplice(v1,v2,v3):
    v = [v1, v2, v3]
    newSimplice = simplice(v)   
    newSimplice.addEdge([(newSimplice.min_vertice, newSimplice.max_vertice),
                         (newSimplice.min_vertice, newSimplice.mid_vertice), 
                         (newSimplice.mid_vertice, newSimplice.max_vertice)])
    newSimplice.edges_init.extend(newSimplice.edges)
    return newSimplice
    

discrete_val = []

inparr = []
m = None # no. of lines in grid
n = None # inputs on one line of grid

with open("input.txt", "r") as f:
    # read the first line containing m and n
    m, n = map(int, f.readline().split())

    # read the second line containing the res values
    discrete_val = list(map(float, f.readline().split()))

    # read the remaining m lines containing n integers each
    
    for i in range(m):
        row = list(map(int, f.readline().split()))
        inparr.insert(0, row)  # insert row at the beginning of the list

discrete_val.sort()

print("m =", m)
print("n =", n)
print("res =", discrete_val)
print("arr =", inparr)

i = 0
j = 0

last_vertice = 0

vertMatrix = []

while (i < m):
    vertMatrix.append([])
    j = 0
    while(j < n):
        vertMatrix[i].append(genVert(inparr[i][j]))
        j = j + 1
    i = i + 1       

i = 0
j = 0
Graph = []
simList = []

while (i < m):
    j = 0
    if (i == 0):
        while (j < n):
            if (j == n - 1):
                pass
            else:
                Graph.append((vertMatrix[i][j],vertMatrix[i][j+1]))
                simList.append(createSimplice(vertMatrix[i][j],
                                              vertMatrix[i][j+1],
                                              vertMatrix[i+1][j]))
            j = j + 1    
    elif (i != m-1):
        while (j < n):
            if (j == n - 1):
                Graph.append((vertMatrix[i][j], vertMatrix[i-1][j]))
            else:
                Graph.append((vertMatrix[i][j],vertMatrix[i][j+1]))
                Graph.append((vertMatrix[i][j], vertMatrix[i-1][j]))
                Graph.append((vertMatrix[i][j], vertMatrix[i-1][j+1]))
                simList.append(createSimplice(vertMatrix[i][j],
                                              vertMatrix[i][j+1],
                                              vertMatrix[i+1][j]))
                simList.append(createSimplice(vertMatrix[i][j],
                                              vertMatrix[i][j+1],
                                              vertMatrix[i-1][j+1]))
            j = j + 1
    
    elif (i == m - 1):
        while (j < n):
            if (j == n - 1):
                Graph.append((vertMatrix[i][j], vertMatrix[i-1][j]))
            else:
                Graph.append((vertMatrix[i][j], vertMatrix[i][j+1]))
                Graph.append((vertMatrix[i][j], vertMatrix[i-1][j]))
                Graph.append((vertMatrix[i][j], vertMatrix[i-1][j+1]))
                simList.append(createSimplice(vertMatrix[i][j],
                                              vertMatrix[i][j+1],
                                              vertMatrix[i-1][j+1]))
            j = j + 1
                            
                
    i = i + 1        
        
print        
        
    
 
# vertice_1 = genVert(1)
# vertice_2 = genVert(2)
# vertice_3 = genVert(3)
# vertice_4 = genVert(4)

# Graph = [(vertice_2, vertice_4),
#          (vertice_1, vertice_4),
#          (vertice_1, vertice_2),
#          (vertice_1, vertice_3),
#          (vertice_3, vertice_4)]

# s1 = [vertice_4, vertice_1, vertice_2]
# s2 = [vertice_3, vertice_1, vertice_4]


# simplice1 = simplice(s1)
# simplice2 = simplice(s2)

# simplice1.addEdge([(vertice_2, vertice_1), (vertice_1,
#                    vertice_4), (vertice_2, vertice_4)])

# simplice2.addEdge([(vertice_3, vertice_1), (vertice_1,
#                    vertice_4), (vertice_3, vertice_4)])


# simplice1.edges_init.extend(simplice1.edges)

# simplice2.edges_init.extend(simplice2.edges)

# simList = [simplice1, simplice2]



max_num = None
min_num = None

compar = []

for i, j in Graph:
    if (i.value not in compar):
        compar.append(i.value)
    if (j.value not in compar):
        compar.append(j.value)

for elem in compar:
    if (max_num == None or elem > max_num):
        max_num = elem
    if (min_num == None or elem < min_num):
        min_num = elem


# for sim in simList:
#     for edge in sim.edges_init:
#         max_v = vertice.maximum(edge[0], edge[1])
#         min_v = vertice.minimum(edge[0], edge[1])
#         for val in discrete_val:
#             if (val > min_v.value and val < max_v.value):
#                 insVert = genVert(val)
#                 sim.insertVerticeBetween((min_v, max_v), insVert)
#                 min_v = insVert

for edge in Graph:
    max_v = vertice.maximum(edge[0], edge[1])
    min_v = vertice.minimum(edge[0], edge[1])
    for val in discrete_val:
        if (val > min_v.value and val < max_v.value):
            insVert = genVert(val)
            for sim in simList:
                if sim.edgeExistsInitially(edge):
                    sim.insertVerticeBetween((min_v, max_v), insVert)
            min_v = insVert


for sim in simList:
    sim.fragmentation()


print("___________________")

i = 1

for sim in simList:
    print("\nsimplice", i, sep="")
    for edge in sim.edges:
       print(edge[0].label, edge[0].value,
             "-----", edge[1].label, edge[1].value)
    i = i + 1


print("___________________\n")

for sim in simList:
    sim.getFragments()


vert_vertices_list = []
vert_edges_list = []
vert_count = -1

dualTreeEdges = []
dualTreeVertices = []

for sim in simList:
    vert_vertices_list.append(sim.verticalGraphVertices())
    vert_edges_list.append(sim.verticalGraphEdges())

print("Printing vertices of dual tree:\n")
for vert_vertice in vert_vertices_list:
    print("START")
    for vert in vert_vertice:
        dualTreeVertices.append(vert)
        print(vert.label, vert.value)
    print("\n")

print("Printing INIT edges of dual tree:\n")
for edge_vertice in vert_edges_list:
    print("START")
    for edge in edge_vertice:
        dualTreeEdges.append(edge)
        print(edge[0].label, edge[0].value,
              "-----", edge[1].label, edge[1].value)
    print("\n")


i = 0
comEdges = []
while (i < len(simList)):
    j = i + 1
    while (j < len(simList)):
        comEdges = []
        if (len(simplice.commonEdges(simList[i], simList[j])) == 0):
            j = j + 1
            continue
        else:
            comEdges = simplice.commonEdges(simList[i], simList[j])
            labels = []
            for edge in comEdges:
                min_vert = vertice.minimum(edge[0], edge[1])
                max_vert = vertice.maximum(edge[0], edge[1])
                labels.append(min_vert.value)
                
            print(labels)    

            for label in labels:
                k = 0
                v1 = None
                v2 = None
                while (k < len(vert_vertices_list[i])):
                    if (vert_vertices_list[i][k].value == label):
                        v1 = vert_vertices_list[i][k]
                        break
                    k = k + 1
                k = 0
                while (k < len(vert_vertices_list[j])):
                    if (vert_vertices_list[j][k].value == label):
                        v2 = vert_vertices_list[j][k]
                        break
                    k = k + 1
                    
                if (v1 != None and v2 != None):
                    dualTreeEdges.append((v1, v2))

        j = j + 1

    i = i + 1

print("PRINTING DUAL TREE VERTICES:")
for vert in dualTreeVertices:
    print(vert.label, vert.value)

print("\n")

print("PRINTING DUAL TREE EDGES:")
for edge in dualTreeEdges:
    try:
        print(edge[0].label, edge[0].value, "-----", edge[1].label, edge[1].value)
    except:
        print("Error")    

print("\n")
# for sim in simList:
#     for edge in sim.edges:
#         print(edge[0].label, edge[0].value,
#               "-----", edge[1].label, edge[1].value)
#     print("next")
# create an empty graph
print("PLOTTING DUAL TREE...")

G = nx.Graph()

# add the vertices to the graph
for vert in dualTreeVertices:
    G.add_node(vert.label, value=vert.value)

# add the edges to the graph
for edge in dualTreeEdges:
    G.add_edge(edge[0].label, edge[1].label)

# draw the graph
# compute node positions using a spring layout algorithm
pos = nx.spring_layout(G)
plt.title("DUAL GRAPH")
nx.draw(G, pos=pos, with_labels=False, node_color='white',
        node_size=500, font_size=10)  # draw the nodes and edges
nx.draw_networkx_labels(G, pos=pos, labels={(
    vert.label): f"{(vert.label, vert.value)}" for vert in dualTreeVertices}, font_size=8)  # add node labels


plt.axis('off')  # turn off the axis
plt.show()


countour_tree_vertices = dualTreeVertices[:]
countour_tree_edges = dualTreeEdges[:]


# i = 0
# label_remove = None
# for edge in countour_tree_edges:
#     if (edge[0].value == edge[1].value):
#         label_remove = edge[1].label
#         edge[1].label = edge[0].label
#         for ed in countour_tree_edges:
#             if ed[0].label == label_remove:
#                 ed[0].label == edge[0].label
#             elif ed[1].label == label_remove:
#                 ed[1].label == edge[0].label

i = 0
label_remove = None
while i < len(countour_tree_edges):
    edge = countour_tree_edges[i]
    if edge[0].value == edge[1].value:
        label_remove = edge[1].label
        edge[1].label = edge[0].label
        j = 0
        while j < len(countour_tree_edges):
            ed = countour_tree_edges[j]
            if ed[0].label == label_remove:
                ed[0].label = edge[0].label
            elif ed[1].label == label_remove:
                ed[1].label = edge[0].label
            j += 1
    i += 1

# print("PRINTING COUNTOUR TREE VERTICES:")
# for vert in countour_tree_vertices:
#     print(vert.label, vert.value)

# print("\n")

# print("PRINTING COUNTOUR TREE EDGES:")
# for edge in countour_tree_edges:
#     print(edge[0].label, edge[0].value, "-----", edge[1].label, edge[1].value)

final_countour_tree_vertices = []
final_countour_tree_edges = []

for vert in countour_tree_vertices:
    verInFinalTree = False
    for ver in final_countour_tree_vertices:
        if (vert.label == ver.label):
            verInFinalTree = True
            break
    if (not verInFinalTree):
        final_countour_tree_vertices.append(vert)

for edge in countour_tree_edges:
    edInFinalTree = False
    isSelfEdge = False
    if (edge[0].label == edge[1].label):
        isSelfEdge = True
    for ed in final_countour_tree_edges:
        if (edge[0].label == ed[0].label and edge[1].label == ed[1].label
            or
                edge[0].label == ed[1].label and edge[1].label == ed[0].label):
            edInFinalTree = True
            break
    if (not edInFinalTree and not isSelfEdge):
        final_countour_tree_edges.append(edge)
        
    

print("PRINTING FINAL COUNTOUR TREE VERTICES:")
for vert in final_countour_tree_vertices:
    print(vert.label, vert.value)

print("\n")

print("PRINTING FINAL COUNTOUR TREE EDGES:")
for edge in final_countour_tree_edges:
    print(edge[0].label, edge[0].value, "-----", edge[1].label, edge[1].value)

print("PLOTTING COUNTOUR TREE...")
# create an empty graph
G1 = nx.Graph()

# add the vertices to the graph
for vert in final_countour_tree_vertices:
    G1.add_node(vert.label, value=vert.value)

# add the edges to the graph
for edge in final_countour_tree_edges:
    G1.add_edge(edge[0].label, edge[1].label)

# draw the graph
# compute node positions using a spring layout algorithm
pos = nx.spring_layout(G1)
plt.title("COUNTOUR TREE")
nx.draw(G1, pos=pos, with_labels=False, node_color='white',
        node_size=500, font_size=10)  # draw the nodes and edges
nx.draw_networkx_labels(G1, pos=pos, labels={(
    vert.label): f"{(vert.label, vert.value)}" for vert in final_countour_tree_vertices}, font_size=8)  # add node labels

plt.axis('off')  # turn off the axis
plt.show()  # display the plot
