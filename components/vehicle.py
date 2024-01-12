from components.component import Component
from components.node import Node
from components.edge import Edge
from components.methods.methods import *
import random
import pygame

__all__ = ['Vehicle']

class Vehicle(Component):
    def __init__(self, id, start_node, end_node, time=0):
        super(Vehicle, self).__init__(time=time)
        self.id = id
        self.start_node = start_node
        self.end_node = end_node
        self.current = start_node.to_edge
        self.current_idx = 1
        self.loc = start_node.loc
        self.is_finished = False
        self.time = time
        self.start_time = time
        self.finish_time = None
        self.travel_time = None
        self.cum_wait_time = 0
        self.history = []
        assert not start_node.is_incoming, "start_node should be outgoing, but start_node.is_incoming is True."
        assert end_node.is_incoming, "end_node should be incoming, but end_node.is_incoming is False."
        self.build_route_dirs()
        self.build_route()
        self.min_travel_time = self.calculate_min_travel_time()
        self.set_image('images/vehicle_opaque_50.png')
        self.update_rotation()
        # print(self.short_str())

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
        new_inter = inter + self.tup_dir_dict[dir]
        new_dir = self.op_dir_dict[dir]
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
        route_dirs.append(self.op_dir_dict[self.end_node.dir])
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
    
    def calculate_min_travel_time(self):
        min_travel_time = 0
        for element in self.route:
            if isinstance(element, Edge):
                min_travel_time += element.delta_t
        return min_travel_time

    def blit(self, screen):
        center_blit(self.display_image, self.loc, screen)

    def update_rotation(self):
        if isinstance(self.current, Edge):
            edge_vec = self.current.end_node.loc - self.current.start_node.loc
            _, self.theta = edge_vec.as_polar()
            self.display_image = pygame.transform.rotate(self.image, -self.theta-90)
    
    def step(self, screen=None):
        if self.is_finished:
            return
        assert self.current is self.route[self.current_idx], \
        f"self.current={self.current}, self.route[self.current_idx]={self.route[self.current_idx]}"
        if isinstance(self.current, Edge):
            # print('self.timer:',self.timer)
            delta_t = self.current.delta_t
            start_node = self.current.start_node
            end_node = self.current.end_node
            progress = self.timer / delta_t
            self.loc = (1-progress) * start_node.loc + progress * end_node.loc
            self.timer += 1
            if self.timer == delta_t:
                if not end_node.is_fringe:
                    next_edge = self.route[self.current_idx + 2]
                    if next_edge is end_node.lt_edge:
                        next_edge.start_node.lt_queue.appendleft(self)
                        self.current = end_node
                        self.current_idx += 1
                        self.timer = None
                    elif next_edge is end_node.gs_edge:
                        next_edge.start_node.gs_queue.appendleft(self)
                        self.current = end_node
                        self.current_idx += 1
                        self.timer = None
                    elif next_edge is end_node.rt_edge or next_edge is end_node.to_edge:
                        self.current = next_edge
                        self.current_idx += 2
                        self.timer = 0
                else:
                    self.is_finished = True
                    self.current = None
                    self.finish_time = self.time + 1
                    self.travel_time = self.finish_time - self.start_time
        elif isinstance(self.current, Node):
            self.cum_wait_time += 1
        if screen is not None:
            self.update_rotation()
            self.blit(screen)
        self.time += 1
