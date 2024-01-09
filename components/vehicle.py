from components.component import Component
from components.node import Node
import random

__all__ = ['Vehicle']

class Vehicle(Component):
    def __init__(self, id, start_node, end_node, time=0):
        super(Vehicle, self).__init__(time=time)
        self.id = id
        self.start_node = start_node
        self.end_node = end_node
        self.current_node = start_node
        assert not start_node.is_incoming, "start_node should be outgoing, but start_node.is_incoming is True."
        assert end_node.is_incoming, "end_node should be incoming, but end_node.is_incoming is False."
        self.build_route_dirs()
        self.build_route()

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        route_dirs_string = str(self.route_dirs)
        route_string = ''
        for element in self.route:
            route_string += str(element) + '\n'
        return f'Vehicle id: {self.id}\n' + route_dirs_string + '\n' + route_string + '\n'
    
    def short_str(self):
        route_dirs_string = str(self.route_dirs)
        route_string = ''
        for element in self.route:
            if isinstance(element, Node):
                route_string += str(element) + '\n'
        return f'Vehicle id: {self.id}\n' + route_dirs_string + '\n' + route_string + '\n'

    def nearest_intermediate_node(self, fringe_node):
        inter = fringe_node.inter
        dir = fringe_node.dir
        is_incoming = fringe_node.is_incoming
        is_fringe = fringe_node.is_fringe
        assert is_fringe, "is_fringe should be True."
        dir_dict = Component.tup_dir_dict
        opposite_dir = Component.op_dir_dict
        new_inter = inter + dir_dict[dir]
        new_dir = opposite_dir[dir]
        new_is_incoming = not is_incoming
        new_is_fringe = False
        return Node(new_inter, new_dir, new_is_incoming, new_is_fringe)

    def build_route_dirs(self):
        start_interm_node = self.start_node.to_edge.end_node
        end_interm_node = self.end_node.from_edge.start_node
        start_interm_inter = start_interm_node.inter
        end_interm_inter = end_interm_node.inter
        delta_i = end_interm_inter.i - start_interm_inter.i
        delta_j = end_interm_inter.j - start_interm_inter.j
        num_ver_moves = delta_i if delta_i >= 0 else -delta_i
        num_hor_moves = delta_j if delta_j >= 0 else -delta_j
        ver_move = 'S' if delta_i >= 0 else 'N'
        hor_move = 'E' if delta_j >= 0 else 'W'
        interm_route_dirs = num_ver_moves * [ver_move] + num_hor_moves * [hor_move]
        random.shuffle(interm_route_dirs)
        route_dirs = []
        route_dirs.append(self.start_node.dir)
        route_dirs += interm_route_dirs
        opposite_dir = Component.op_dir_dict
        route_dirs.append(opposite_dir[self.end_node.dir])
        self.route_dirs = route_dirs
        
    def build_route(self):
        route_dirs = self.route_dirs
        route = []
        node_0 = self.start_node
        for i in range(len(route_dirs)):
            dir_now = route_dirs[i]
            if i != len(route_dirs) - 1:
                dir_next = route_dirs[i+1]
            assert not node_0.is_incoming, "node_0 should be outgoing, not incoming."
            assert node_0.dir == dir_now, "node_0 should be aligned with dir_now."
            edge_0 = node_0.to_edge
            node_1 = edge_0.end_node
            if i != len(route_dirs)-1:
                for edge_option in [node_1.lt_edge, node_1.gs_edge, node_1.rt_edge]:
                    if edge_option.end_node.dir == dir_next:
                        edge_1 = edge_option
                        break
                route += [node_0, edge_0, node_1, edge_1]
                node_0 = edge_1.end_node
            else:
                route += [node_0, edge_0, node_1]
        self.route = route
