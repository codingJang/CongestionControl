import pygame

__all__ = ['center_blit', 'center_rect']


def center_blit(screen, sprite):
    """
    Blit some sprite's display_image centered around loc
    :param sprite: Sprite used in this simulation (nodes, edges, vehicles, ...)
    :return: None
    """
    screen.blit(sprite.display_image,
                (sprite.loc.x - sprite.display_image.get_width()/2,
                 sprite.loc.y - sprite.display_image.get_height()/2))


def center_rect(sprite):
    return sprite.display_image.get_rect().move(sprite.loc.x - sprite.width/2,
                                                sprite.loc.y - sprite.height/2)
