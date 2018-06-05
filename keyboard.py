import pygame
import sys

import objects
import display


hspeed = 5

def keyboard_handler(pressed_keys, object_list, player, speed_scale):
    # Run through the list of mapped keys and check if they are pressed.
    # This could be achieved with an array and a large number of functions,
    # but this will do.
    if pygame.K_q in pressed_keys:
        # q key to quit
        sys.exit()
    if pygame.K_a in pressed_keys:
        if player.pos[0] - player.width/2 > 0:
            objects.move(player, (-hspeed * speed_scale, 0))
    if pygame.K_d in pressed_keys:
        if player.pos[0] + player.width/2 < display.WIDTH:
            objects.move(player, (hspeed * speed_scale, 0))
    if pygame.K_e in pressed_keys:
        if player.data == None:
            b = objects.launch_bone(player)
            l = objects.G_obj_list_el(b, object_list, object_list.next)
            player.data = (b, l)
            objects.g_l_insert(object_list, l)
