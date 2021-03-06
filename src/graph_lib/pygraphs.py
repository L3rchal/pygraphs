""" Pygraphs

Graph library, this file should be splitted when goes bigger.
split into classes over inheritance
"""

__author__ = 'Ales Lerch'

import os
import sys
import pprint
import copy
import random
import collections
from functools import reduce

"""
graph = { "a" : [("c",4)],
          "b" : ["c", "e"],
          "c" : ["a", "b", "d", "e"],
          "d" : ["c"],
          "e" : ["c", "b"],
          "f" : []
        }
"""
class HMGraph:
    """
    Hash Matrix Graph implementation.
    """

    def __init__(self,setup_nodes = [], edges_with_val = False, first_node =
            None):
        """
        Maybe different library for for hashmax if to include order key inputs if
        needed in this data structure
        data_dict = collections.OrderedDict(sorted(data_dict.items()))
        """
        self.hashmax = {}
        self.hashmax = collections.OrderedDict()
        self.double_round = False
        self.edges_value = edges_with_val
        self.first_node = first_node
        if setup_nodes and isinstance(setup_nodes,list):
            """
            In case to use indexes as int use range(len(setup_nodes))
            else let it as key name it's python
            """
            for spec_node in setup_nodes:
                self.hashmax[spec_node.strip()] = []

    def add_node(self,name = "",edges = [], update = ()):
        if name and name not in self.hashmax.keys():
            if not edges:
                print("Info: No edges were inputed with node %s" % name)
            self.hashmax[name] = edges
        else:
            print('Error: Node: [%s] is alredy in this graph' % name)
        if update:
            for up_node in update:
                self.hashmax[up_node].append(name)
                """
                update graph with new edges
                """

    def remove_node(self,which = None):
        """
        there should be somthing done with else statement, what to do if which
        is set?
        """
        if which:
            del self.hashmax[which]
            for hash_list in self.hashmax.values():
                hash_list.remove(which)
        else:
            pass

    def insert_edge(self,node,target_edge,edge_val = None,name_val = None):
        """
        current dilema on graph structure - should be same architecture
        with value as zeros like g : ('n',0) or have two architerues
        should be third paramater non mandatori?
        """
        if not self.edges_value:
            if target_edge in self.hashmax[node]:
                self.double_round = True
            else:
                self.hashmax[node].append(target_edge)

        elif self.edges_value and edge_val and not name_val:
            if target_edge in map(lambda x:x[0], self.hashmax[node]):
                self.double_round = True
            else:
                self.hashmax[node].append((target_edge,int(edge_val)))

        elif self.edges_value and edge_val and name_val:
            if target_edge in map(lambda x:x[0], self.hashmax[node]):
                self.double_round = True
            else:
                self.hashmax[node].append((target_edge,int(edge_val),name_val))


    def print_hashMap(self, sorted_ = False, level = None):
        """
        Currently just pretty print.
        """
        pp = pprint.PrettyPrinter(indent=2)
        if level:
            pprint.pprint(self.hashmax,width=level)
        else:
            print('{')
            if sorted_:
                for key,val in sorted(self.hashmax.items(), key=lambda x:x[0]):
                    print('  \"%s\" : %s' % (key,sorted(val,key=lambda x:x[0])))
            else:
                for key,val in self.hashmax.items():
                    print('  \"%s\" : %s' % (key,val))
            print('}')

    def get_nodes(self,specific = None):
        nodes = sorted([nod for nod in self.hashmax.keys()])
        if not specific:
            return nodes
        else:
            return nodes[specific]

    def get_edges(self):
        fin_edges = []
        for node,edges in self.hashmax.items():
            for edge in edges:
                fin_edges.append((node,edge))
        return fin_edges

    def find_most_used_node(self):
        """
        this is first task this may be putting into distribution.py
        if all values are same then output all of them
        if all[va for val in most_used.values()]
        """
        most_used = {key: 0 for key in self.get_nodes()}
        for key,val in self.hashmax.items():
            most_used[key] += len(val)
            most_used[key] += [True if key in val else False for val in
                    self.hashmax.values()].count(True)

        max_used = max(most_used, key = lambda k : most_used[k])
        return (max_used,most_used[max_used])

    def has_cycle(self):

        def dfs(graph, node, color, found_cycle):
            if not found_cycle:
                color[node] = "gray"
                for vertex in graph[node]:
                    if color[vertex] == "gray":
                        found_cycle.append(True)
                        return
                    if color[vertex] == "white":
                        dfs(graph,vertex, color, found_cycle)
                color[node] = "black"
            else:
                return

        color = {node : "white" for node in self.get_nodes()}
        found_cycle = []
        graph = self.hashmax.copy()
        for node in self.get_nodes():
            if color[node] == "white":
                dfs(graph,node, color, found_cycle)
            if found_cycle[0]:
                break
        return found_cycle[0]

    def has_cycle_undericted(self):
        start = self.get_nodes()[0]
        visited, stack = [], [start]

        while stack:
            vertex = stack.pop()
            visited.append(vertex)
            for node in self.hashmax[vertex]:
                if node in stack:
                    return True
                if node not in visited:
                    stack.append(node)
        return False


    def is_united(self):
        visited, stack = [], [random.choice(list(self.hashmax.keys()))]
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.append(vertex)
            for next_ in self.hashmax[vertex]:
                if next_ not in visited:
                    stack.append(next_)
        return True if sorted(visited) == sorted(list(self.hashmax.keys())) else False

    def is_a_tree(self):
        """
        simple code that call two system methods to check abilit tree graph
        that is if it has no cycle and is united
        inicialization may look weird but it's all because new checker
        """

        has_cycle = self.has_cycle_undericted()
        is_united = self.is_united()

        return True if not has_cycle and is_united else False

    def is_biparted(self):
        """
        is_biparted fistly create dict of nodes with None color and then create
        other... not woking - fix it!
        d = {key: value for (key, value) in iterable}
        """
        colors = {x: None for x in self.get_nodes()}
        start = self.get_nodes()[0]
        visited, queue = set(), [start]
        colors[start] = "cervena"
        while queue:
            vertex = queue.pop(0)
            if vertex not in visited:
                visited.add(vertex)
                for vert in self.hashmax[vertex]:
                        if vert not in visited:
                            queue.append(vert)
                for x in [node for node in self.get_nodes() if node not in
                        visited]:
                    if colors[x] == colors[vertex]:
                        return False
                    colors[x] = "zelena" if colors[vertex] == "cerverna" else "cerverna"

        return colors

    def find_graph_skeleton(self):
        key = 0
        min_ = float("inf")
        key_edge = ()
        skeleton = []
        visited = set()
        copy_graph = self.hashmax.copy()

        if self.edges_value and self.hashmax:
            while sorted(list(visited)) != self.get_nodes():
                """
                min_edge = min([(x,y) for x,y in copy_graph.items()],key = lambda x: x[1])
                min_edge_reverse = (min_edge[1][0],min_edge[0])
                map(lambda x: visited.add(x),[min_edge[0],min_edge[1][0]])
                nedalo by se toto taky dat jenom na jeden radek
                """
                for x,y in copy_graph.items():
                    if y:
                        val = min(y,key = lambda b : b[1])[1]
                        if val < min_:
                            min_ = val
                            key_edge = min(y,key = lambda b : b[1])
                            key = x
                if copy_graph[key]:
                    copy_graph[key].remove(key_edge)
                if copy_graph[key_edge[0]]:
                    copy_graph[key_edge[0]].remove((key,key_edge[1]))
                skeleton.append((key,key_edge))
                visited.add(key)
                visited.add(key_edge[0])
                min_ = float("inf")

        return skeleton

    def find_articulation(self):
        answer = {}
        for node in self.get_nodes():
            copy_graph = {}
            for node_, edge in self.hashmax.items():
                copy_graph[node_] = edge[:]
            del copy_graph[node]
            for edge in copy_graph.values():
                try:
                    edge.remove(node)
                except ValueError:
                    pass
            visited = []
            stack = [random.choice(list(copy_graph.keys()))]
            while stack:
                vertex = stack.pop()
                if vertex not in visited:
                    visited.append(vertex)
                for next_ in copy_graph[vertex]:
                    if next_ not in visited:
                        stack.append(next_)

            edited = self.get_nodes()
            edited.remove(node)
            answer[node] = True if sorted(visited) == edited else False
        return answer

    def find_bridge(self,articulations):
        if articulations:
            bridges = {}
            for key, val in articulations.items():
                respond = {}
                if not val:
                    for next_node in self.hashmax[key]:
                        copy_graph = {}
                        for node_, edge in self.hashmax.items():
                            copy_graph[node_] = edge[:]
                        copy_graph[key].remove(next_node)
                        copy_graph[next_node].remove(key)
                        """
                        go through whole graph and find out if there is another
                        complete
                        """
                        visited = []
                        stack = [random.choice(list(copy_graph.keys()))]
                        while stack:
                            vertex = stack.pop()
                            if vertex not in visited:
                                visited.append(vertex)
                            for next_ in copy_graph[vertex]:
                                if next_ not in visited:
                                    stack.append(next_)

                        respond[next_node] = True if sorted(visited) == self.get_nodes() else False
                    bridges[key] = respond
            return bridges
        else:
            return "Error: No input articulations"

    def djikstra(self,first,number = 0):
        if self.edges_value and first:
            djisktra = {x: [None,float("inf")] for x in self.get_nodes() if x != first}
            djisktra[first] = [None,0]
            stack, visited = [(first,0)], []
            while number <= len(self.get_nodes()) and stack:
                number += 1
                vertex = stack.pop(0)
                visited.append(vertex[0])
                for edge in self.hashmax[vertex[0]]:
                    calculated = djisktra[vertex[0]][1] + edge[1]
                    if calculated < djisktra[edge[0]][1]:
                        djisktra[edge[0]] = [vertex,calculated]
                for next_ in self.hashmax[vertex[0]]:
                    if not next_[0] in visited:
                        stack.append(next_)
            return djisktra
        else:
            return "Error something went wrong"

    """
    this methond is commented due to killing cpu
    1)Vytvorim graf na cyklu,2)Odecist z radku min, 3)Kde je nula tam je phi,4) Najit
    nejvetsi phi,5) Tvrit hranu do grafu,6) Smazat hranu z matice, 7) Vytvorit opacne
    inf, 8) konec self.max.nodes == new graf nodes
    """
    def travelling_salesman(self):
        salesman = {}
        travel = HMGraph(self.get_nodes())
        for key in sorted(self.hashmax.keys()):
            salesman[key] = sorted(self.hashmax[key][:], key = lambda x : x[0])

        while len(salesman.keys()) > 1:
            for row in sorted(salesman.keys()):
                min_ = min(salesman[row],key = lambda x: x[1])
                coa = [col for col in salesman[row] if col[1] != float("inf")]
                if len([col for col in salesman[row] if col[1] != float("inf")]) >= 2:
                    new_row = []
                    for column in salesman[row]:
                        new_row.append((column[0],column[1] - min_[1]))
                    salesman[row] = new_row
            """
            jeste bych mel dodelat vertikalni nuly vsude
            """
            zeros = {}
            for key, row in salesman.items():
                for column in row:
                    if column[1] == 0:
                        min_row = min([r for r in row if r != column], key = lambda x: x[1])
                        min_column = [[(r[0],r[1]) for r in row_ if r[0] ==
                            column[0] and row != row_] for row_ in salesman.values()]
                        min_column = min([min_[0] for min_ in min_column if min_],key=lambda x:x[1])
                        zeros[(key,column[0])] = min_row[1] + min_column[1]

            if zeros:
                sigma = max(sorted(zeros.items(),key=lambda x:x[0]),key=lambda x: x[1])
                travel.insert_edge(sigma[0][0],sigma[0][1])
                del salesman[sigma[0][0]]
                for key, val in salesman.items():
                    salesman[key] = [(v[0],float("inf")) if key == sigma[0][1] and v[0] ==
                            sigma[0][0] else v for v in val if v[0] != sigma[0][1]]
        return travel

    def floyd_warshall(self):
        """
        classic floyd warshall implemetation in python, has table transforms to
        matrix in which is dound statisitc nimber, those number are used in
        floy warhall algorithm, this algortim finds if there is negative cycle
        """
        floyd = {}
        theta = len(self.get_nodes())
        for key, val in sorted(self.hashmax.items(),key=lambda x: x[1]):
            floyd[key] = sorted(val[:], key = lambda x : x[0])
            floyd[key].append((key,0))

        matrix = []
        for key, val in sorted(floyd.items(), key=lambda x: x[0]):
            matrix.append([s[1] for s in sorted(val, key = lambda x : x[0])])

        for k in range(0, theta):
            for i in range(0, theta):
                for j in range(0, theta):
                    matrix[i][j] = max(matrix[i][j], matrix[i][k] + matrix[k][j])

        for k in range(0, theta):
            for i in range(0, theta):
                for j in range(0, theta):
                    if (matrix[i][k] + matrix[k][j] < matrix[i][j]):
                        matrix[i][j] = float("-inf")

    def paring_hungarian(self):
        """copying main graph"""
        madar = {}
        for key,val in sorted(self.hashmax.items(),key=lambda x: x[0]):
            if key[0] == 'B':
                madar[key] = val

        """editing all rows"""
        for key, val in sorted(madar.items(),key=lambda x: x[0]):
            if 0 not in [x[1] for x in val]:
                min_ = min(val,key = lambda k: k[1])
                madar[key] = [(y[0],y[1]-min_[1]) for y in val]
        """editing all columns"""
        for i, data in enumerate(sorted(madar.items(),key=lambda x: x[0])):
            if 0 not in list(reduce(list.__add__,
                [[col for col in row if row.index(col) == i] for row in madar.values()])):
                min_ = min(list(reduce(list.__add__,
                    [[col for col in row if row.index(col) == i] for row in madar.values()])),
                    key = lambda k: k[1])
                madar[data[0]] = [(y[0],y[1]-min_[1]) if data[1].index(y) == i else y for y in data[1]]

        while(True):
            """
            finding independece zeros -> M
            """
            independent_zero = [False for t in madar.keys()]
            positions = []
            visited = []
            for key_l, line in sorted(madar.items(),key = lambda x:x[0]):
                for r in range(len(line)):
                    if line[r][1] == 0 and not independent_zero[r]:
                        independent_zero[r] = True
                        positions.append((key_l,r))
                        visited.append(key_l)
                        break
            if all(independent_zero):
                if len(positions) == len(madar.keys()):
                    right_destinations = {}
                    index = 0
                    for des in positions:
                        right_destinations[index] = ("%s %s" %
                                (des[0],madar[des[0]][des[1]][0]),self.hashmax[des[0]][r][1])
                        index += 1
                    return right_destinations

            """könig's line"""
            k=0
            konig = {}
            all_zeros = True
            shortcut = False
            for key, val in sorted(madar.items(),key = lambda x:x[0]):
                konig[key] = [(v[0],v[1],0) for v in val]

            """getting index to right columns and rows
            """
            marked_row = list(set(madar.keys()) - set(visited))[0]
            marked_column = independent_zero.index(False)

            column_indexes = []
            for ind,mr in enumerate(madar[marked_row]):
                if mr[1] == 0:
                    column_indexes.append(ind)

            row_indexes = []
            for key,value in sorted(madar.items(),key = lambda x:x[0]):
                if value[marked_column][1] == 0:
                    row_indexes.append(key)

            #obravim sloupec
            for ci in column_indexes:
                for key,k_line in sorted(konig.items(),key = lambda x:x[0]):
                    konig[key] = [(y[0],y[1],y[2]+1) if konig[key].index(y) ==
                            ci else y for y in konig[key]]

                for i, k_line in enumerate(sorted(konig.items(),key = lambda
                    x:x[0])):
                    if i == ci:
                        konig[k_line[0]] = [(n_l[0],n_l[1],True) for n_l in k_line[1]]

            #obarvim radek
            for ri in row_indexes:
                konig[ri] = [(y[0],y[1],y[2]+1) for y in konig[ri]]

            #kontrola jestli jsou oznacene nuly
            for line in konig.values():
                    for l in line:
                        if l[1] == 0 and l[2] == 0:
                            all_zeros = False

            if not all_zeros:
                """finding rest zeros """
                for k in range(len(konig.keys())):
                    zeros_line = (0,None)
                    zeros_column = (0,None)

                    """finding column with highes zero count"""
                    for i,line in enumerate(konig.values()):
                        if line.count(0) > zeros_line[0] and all([t[2] for t in line]):
                            zeros_line = (line.count(0),i)

                    """finding column with highes zero count"""
                    for i in range(len(madar.keys())):
                        column = []
                        for line in madar.values():
                            column.append(line[i])
                        if column.count(0) > zeros_column[0] and all([t[2] for t in column]):
                            zeros_column = (line.count(0),i)

                    if not zeros_column and not zeros_line:
                        print("Error no zeros found canceling out")
                        return None

                    elif zeros_column[0] < zeros_line[0] or zeros_line[0] == zeros_column[0]:
                        #obravim slopec
                        for i, k_line in enumerate(konig.items()):
                            if i == zeros_line[1]:
                                konig[k_line[0]] = [(n_l[0],n_l[1],n_l[2]+1) for n_l in k_line[1]]

                    elif zeros_column[0] > zeros_line[0]:
                        #obravim radek, data[1] == line
                        for i,data in enumerate(konig.items()):
                            konig[data[0]] = [(y[0],y[1],y[2]+1) if data[1].index(y) == i else y for y in data[1]]

                    #jsou vsechny nuly obarveny?
                    for line in konig.values():
                        for l in line:
                            if l[1] == 0 and l[2] == 0:
                                all_zeros = False

                    if all_zeros:
                        break
            else:
                shortcut = True

            if all_zeros and k == len([x for x in independent_zero if x]):
                pass
            elif (all_zeros and k < len([x for x in independent_zero if x])) or\
            (all_zeros and shortcut):
                konig_min = min(list(reduce(list.__add__,[[l[1] for l in line if
                    l[2] == 0] for line in konig.values()])))
                for key, value in sorted(konig.items(),key = lambda x:x[0]):
                    chosen_one = []
                    for va in value:
                        if va[2] == 0:
                            chosen_one.append((va[0],va[1]-konig_min))
                        elif va[2] == 1:
                            chosen_one.append((va[0],va[1]))
                        elif va[2] == 2:
                            chosen_one.append((va[0],va[1]+konig_min))
                    madar[key] = chosen_one
            else:
                print('Error nejsou zaskrtnuty vsechny nuly')
                sys.exit()

    def edmons_karp(self):
        id_ = 0
        paths = {}
        worker = copy.deepcopy(self.hashmax)
        while True:
            stack, visited, vertex = [(self.first_node,float('inf'),'')],[],' '
            while stack and vertex[0] != 'EXIT':
                vertex = stack.pop()
                visited.append(vertex)
                for next_ in worker[vertex[0]]:
                    if next_[0] not in [st[0] for st in stack] and \
                       next_[0] not in [vis[0] for vis in visited] and \
                       next_[1] > 0:
                        stack.append(next_)
                        """
                        this finds one specific way, however when it's used
                        algorithm does not find very good way, in some cases
                        giberish
                        break
                        """
            if not stack and 'EXIT' not in list(map(lambda x:x[0],visited)):
                break
            paths[id_] = (visited,min(visited,key = lambda x: x[1])[1],
                    len(list(filter(lambda x:x[1] < float("inf"),visited))))
            for i in range(len(visited)-1):
                if visited[i][1] > 0:
                    worker[visited[i][0]] = [(x[0],x[1]-paths[id_][1],x[2]) if
                            x[0] == visited[i+1][0] else x for x in
                            worker[visited[i][0]]]
                    worker[visited[i+1][0]] = [(x[0],x[1]+paths[id_][1],x[2]) if
                            x[0] == visited[i][0] else x for x in
                            worker[visited[i+1][0]]]
            id_ += 1
        max_path = max(paths.values(),key = lambda x: x[2])
        if not id_:
            return None
        else:
            return (sum([x[1] for x in paths.values()]),worker,max_path)



    def cpm_long(self,first_node,s_nodes):
        """
        this algirithm is similar to critial path method, only uses main part
        of this algortihm, find the biggest way where higer number of edge in
        node is better
        """
        cpm_nodes = {x: (None,0,0) for x in self.get_nodes()}
        for spec in s_nodes:
            cpm_nodes[spec[0]] = (None,0,1)

        for key, val in sorted(self.hashmax.items(),key=lambda x: x[0]):
            for v in val:
                cpm_nodes[v[0]] = max(cpm_nodes[v[0]],
                        (key,v[1]+cpm_nodes[key][1]+cpm_nodes[v[0]][2],cpm_nodes[v[0]][2]),
                        key=lambda x:x[1])

        return cpm_nodes

    def coloring_grups(self,max_grups):
        if len(self.get_nodes()) > 3:
            grups = {}
            for a in range(max_grups):
                grups["grup_n%s" % a] = []
            start = self.get_nodes()[0]
            visited, stack = [], [start]
            while stack:
                vertex = stack.pop(0)
                visited.append(vertex)
                found_colors = []
                for neighbor in self.hashmax[vertex]:
                    if neighbor not in visited and neighbor not in stack:
                        stack.append(neighbor)
                    try:
                        found_colors.append(list(filter(lambda x: neighbor in x[1],
                            [(grup_color,nodes) for grup_color,nodes in grups.items()]))[0][0])
                    except (IndexError,AttributeError):
                        pass
                """
                Test if there are any free colors to take, if not end algorithm
                with None
                """
                if set(found_colors) == set(grups.keys()):
                    return None
                if not found_colors:
                    found_colors = list(grups.keys())[:]
                else:
                    found_colors = list(set(grups.keys()) - set(found_colors))
                found = min([(grp,len(grups[grp])) for grp in found_colors],
                        key = lambda x: x[1])
                grups[found[0]].append(vertex)
            return grups
        else:
            return None

    def find_clique(self):

        def contin(edges):
            counter = [count_edges[1] for count_edges in edges.values()]
            return all([counter[0] == leng for leng in counter])

        def body(edited_hash):
            """
            body delet all nodes that are in clique, and others field then
            return clique and updated hash table-dict
            """
            counting_edges = {}
            for vertex, edit_edge in edited_hash.items():
                counting_edges[vertex] = (edit_edge[:],len(edit_edge))

            while not contin(counting_edges):
                del_key = min([(ed,val) for ed,val in
                    counting_edges.items()],key = lambda x : x[1][1])[0]
                del counting_edges[del_key]
                for node, edge in counting_edges.items():
                    try:
                        edge[0].remove(del_key)
                        new_edge_list = edge[0]
                    except ValueError:
                        new_edge_list = edge[0]
                    except AttributeError:
                        new_edge_list = edge[0]
                    counting_edges[node] = (new_edge_list,len(new_edge_list))

            clique = []
            for cliq_node in counting_edges.keys():
                del edited_hash[cliq_node]
                for editing_key in edited_hash.keys():
                    try:
                        edited_hash[editing_key].remove(cliq_node)
                    except ValueError:
                        pass
                    except AttributeError:
                        pass
                clique.append(cliq_node)

            return (clique,edited_hash)

        cliques = []
        graph = self.hashmax.copy()
        while graph:
            (cli,graph) = body(graph)
            cliques.append(cli)
        return cliques
