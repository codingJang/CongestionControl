from components import *

__all__ = ['Vehicle']

class Vehicle(Component):
    def __init__(self, start_node, end_node):
        self.start_node = start_node
        self.end_node = end_node
        if start_node.is_incoming:
            raise AssertionError("start_node should be outgoing, but start_node.is_incoming is True.")
        if not end_node.is_incoming:
            raise AssertionError("end_node should be incoming, but end_node.is_incoming is False.")
        self.build_route()

    def nearest_intermediate_node(self, fringe_node):
        # calculate nearest_intermediate_node
        pass
    def build_route(self):
        start_interm = self.nearest_intermediate_node(self.start).coord
        end_interm = self.nearest_intermediate_node(self.end).coord