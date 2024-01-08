from components import *
import random

__all__ = ['Vehicle']

class Vehicle(Component):
    def __init__(self, id, start_time, start_node, end_node):
        super(Vehicle, self).__init__()
        self.id = id
        self.start_time = start_time
        self.start_node = start_node
        self.end_node = end_node
        self.current_node = start_node
        if start_node.is_incoming:
            raise AssertionError("start_node should be outgoing, but start_node.is_incoming is True.")
        if not end_node.is_incoming:
            raise AssertionError("end_node should be incoming, but end_node.is_incoming is False.")
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

    def nearest_intermediate_node(self, fringe_node):
        inter = fringe_node.inter
        dir = fringe_node.dir
        is_incoming = fringe_node.is_incoming
        is_fringe = fringe_node.is_fringe
        if not is_fringe:
            raise AssertionError("is_fringe should be True.")
        dir_dict = Component.dir_dict
        opposite_dir = Component.opposite_dir
        new_inter = inter + dir_dict[dir]
        new_dir = opposite_dir[dir]
        new_is_incoming = not is_incoming
        new_is_fringe = False
        return Node(new_inter, new_dir, new_is_incoming, new_is_fringe)

    def build_route_dirs(self):
        start_interm_node = self.nearest_intermediate_node(self.start_node)
        end_interm_node = self.nearest_intermediate_node(self.end_node)
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
        opposite_dir = Component.opposite_dir
        route_dirs.append(opposite_dir[self.end_node.dir])
        self.route_dirs = route_dirs
        
    def build_route(self):
        route_dirs = self.route_dirs
        route = []
        sn = self.start_node
        node_now_out = Node(sn.inter, sn.dir, sn.is_incoming, sn.is_fringe)
        dir_dict = Component.dir_dict
        opposite_dir = Component.opposite_dir
        for i in range(len(route_dirs)-1):
            dir_now = route_dirs[i]
            dir_next = route_dirs[i+1]
            if node_now_out.is_incoming:
                raise AssertionError("node_now should be outgoing, not incoming.")
            node_now_in = Node(node_now_out.inter + dir_dict[dir_now], opposite_dir[dir_now], True, False)
            node_next_out = Node(node_now_in.inter, dir_next, False, False)
            # Append nodes and edges
            route.append(node_now_out)
            route.append(Edge(node_now_out, node_now_in, False))
            route.append(node_now_in)
            route.append(Edge(node_now_in, node_next_out, True))
            node_now_out = node_next_out
        # print(route_dirs)
        # for element in route:
        #     print(element)
        final_dir = route_dirs[-1]
        if node_now_out.is_incoming:
                raise AssertionError("node_now should be outgoing, not incoming.")
        node_now_in = Node(node_now_out.inter + dir_dict[final_dir], opposite_dir[final_dir], True, True)
        if node_now_in != self.end_node:
            raise AssertionError("The last node of the route is not the destination node.")
        route.append(node_now_out)
        route.append(Edge(node_now_out, node_now_in, False))
        route.append(node_now_in)
        self.route = route
        

# initialization test
if __name__ == '__main__':
    my_car = Vehicle('Car0', 0, Node(Intersection(1, 0), 'E', False, True), Node(Intersection(3, 4), 'N', True, True))
    print(my_car)