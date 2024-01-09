from components.component import Component
from components.intersection import Intersection
from components.node import Node
from components.edge import Edge


class Graph(Component):
    def __init__(self, H, L, time=0):
        super(Graph, self).__init__(time=time)
        self.H = H
        self.L = L
        self.construct_inters()
        self.construct_nodes()
        self.construct_edges()
    
    def construct_inters(self):
        H = self.H
        L = self.L
        self.fringe_inters = []
        self.fringe_inters += [Intersection(0, j) for j in range(1, L+1)]
        self.fringe_inters += [Intersection(H+1, j) for j in range(1, L+1)]
        self.fringe_inters += [Intersection(i, 0) for i in range(1, H+1)]
        self.fringe_inters += [Intersection(i, L+1) for i in range(1, H+1)]
        self.interm_inters = []
        for i in range(1, H+1):
            for j in range(1, L+1):
                self.interm_inters.append(Intersection(i, j))
        self.inters = self.fringe_inters + self.interm_inters
    
    def construct_nodes(self):
        H = self.H
        L = self.L
        self.fringe_nodes = []
        for inter in self.fringe_inters:
            if inter.i == 0:
                self.fringe_nodes.append(Node(inter, 'S', True, True))
                self.fringe_nodes.append(Node(inter, 'S', False, True))
            if inter.i == H+1:
                self.fringe_nodes.append(Node(inter, 'N', True, True))
                self.fringe_nodes.append(Node(inter, 'N', False, True))
            if inter.j == 0:
                self.fringe_nodes.append(Node(inter, 'E', True, True))
                self.fringe_nodes.append(Node(inter, 'E', False, True))
            if inter.j == L+1:
                self.fringe_nodes.append(Node(inter, 'W', True, True))
                self.fringe_nodes.append(Node(inter, 'W', False, True))
        self.interm_nodes = []
        for inter in self.interm_inters:
            for dir in ['E', 'N', 'W', 'S']:
                self.interm_nodes.append(Node(inter, dir, True, False))
                self.interm_nodes.append(Node(inter, dir, False, False))
        self.nodes = self.fringe_nodes + self.interm_nodes

    def construct_edges(self):
        H = self.H
        L = self.L
        tup_dir_dict = Component.tup_dir_dict
        op_dir_dict = Component.op_dir_dict
        lt_dir_dict = Component.lt_dir_dict
        rt_dir_dict = Component.rt_dir_dict
        self.edges = []
        for node in self.interm_nodes:
            if node.is_incoming:
                dir_tuple = tup_dir_dict[node.dir]
                from_inter = node.inter + dir_tuple
                i = from_inter.i
                j = from_inter.j
                is_fringe = True if i == 0 or i == H+1 or j == 0 or j == L+1 else False
                from_node_idx = self.nodes.index(Node(from_inter, op_dir_dict[node.dir], False, is_fringe))
                lt_node_idx = self.nodes.index(Node(node.inter, lt_dir_dict[node.dir], False, False))
                gs_node_idx = self.nodes.index(Node(node.inter, op_dir_dict[node.dir], False, False))
                rt_node_idx = self.nodes.index(Node(node.inter, rt_dir_dict[node.dir], False, False))
                from_node = self.nodes[from_node_idx]
                tl_node = self.nodes[lt_node_idx]
                gs_node = self.nodes[gs_node_idx]
                rt_node = self.nodes[rt_node_idx]
                from_edge = Edge(from_node, node, False)
                tl_edge = Edge(node, tl_node, True)
                gs_edge = Edge(node, gs_node, True)
                rt_edge = Edge(node, rt_node, True)
                self.edges.append(from_edge)
                self.edges.append(tl_edge)
                self.edges.append(gs_edge)
                self.edges.append(rt_edge)
                node.connect_to_edge(from_edge, tl_edge, gs_edge, rt_edge)

        for node in self.fringe_nodes:
            if node.is_incoming:
                dir_tuple = tup_dir_dict[node.dir]
                from_inter = node.inter + dir_tuple
                from_node_idx = self.nodes.index(Node(from_inter, op_dir_dict[node.dir], False, False))
                from_node = self.nodes[from_node_idx]
                from_edge = Edge(from_node, node, False)
                self.edges.append(from_edge)
                node.connect_to_edge(from_edge)
    
    def step(self, screen=None):
        for inter in self.inters:
            inter.step(None, screen=screen)
        for node in self.nodes:
            node.step(screen=screen)
        for edge in self.edges:
            edge.step(screen=screen)