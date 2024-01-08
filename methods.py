import pygame
from pygame.math import Vector2

__all__ = ['center_blit', 'center_rect', 'to_vector2']


def center_blit(sprite, screen):
    """
    Blit some sprite's display_image centered around loc
    :param sprite: Sprite used in this simulation (nodes, edges, vehicles, ...)
    :param screen: Pygame display object
    :return: None
    """
    screen.blit(sprite.display_image,
                (sprite.loc.x - sprite.display_image.get_width()/2,
                 sprite.loc.y - sprite.display_image.get_height()/2))


def center_rect(sprite):
    return sprite.display_image.get_rect().move(sprite.loc.x - sprite.width/2,
                                                sprite.loc.y - sprite.height/2)

def to_vector2(tuple):
    return Vector2(240 * tuple[1], 240 * tuple[0])

def bind_vehicle_to_road(vehicle, road):
    vehicle.road = road
    road.vehicles.push(vehicle)