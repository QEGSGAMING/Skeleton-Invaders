import pygame
import display
import os


# The data property can be used to attach additional data to an object - for
# example, their type and health. Inheritance could be used instead.
# The pos property gives the position of the CENTRE of the object.
class Game_object:
    def __init__(self, pos, img_idx, height, width, data):
        self.pos = pos
        self.img_idx = img_idx
        self.height = height
        self.width = width
        self.data = data

def move(obj, vector):
    ow = obj.width
    oh = obj.height
    obj.pos[0] += vector[0]
    obj.pos[1] += vector[1]


def new_game_object(pos, image_name, data=None):
    # Function to handle loading of image and initialisation of class.
    # data is an optional argument
    img_idx = display.load_image(image_name)
    width = display.images[img_idx].get_width()
    height = display.images[img_idx].get_height()
    return Game_object(pos, img_idx, height, width, data)

def launch_bone(player):
    return new_game_object([player.pos[0], player.pos[1] - player.height/2 +5],
            "bone.png")


class G_obj_list_el:
    def __init__(self, data, prev, next):
        self.data = data
        self.prev = prev
        self.next = next

def g_l_insert(l, n):
    if l.next != None:
        l.next.prev = n
    l.next = n

def g_l_remove(n):
    n.prev.next = n.next
    if n.next != None:
        n.next.prev = n.prev
