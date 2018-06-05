#!/usr/bin/env python3

# This program implements most of the features needed for a game to run on
# the Raspbery Pi arcade machine. Adding to the code should allow a real game
# to be created. I did not create any of the assets included with the program,
# although I may have modified them.
# - Ciaran


import pygame
import pygame.mixer
import sys
import random
import math

# This corresponds to objects.py and contains functions for manipulating
# in-game objects.
import objects

# This is for drawing to the screen, and for loading images
# NOTE: All images are stored in the assets folder. The folder name does NOT
# need to be added to the file names. This is so that the assets will load
# correctly on the Raspberry Pi.
import display

# This is keyboard.py and contains functions for handling user input
import keyboard




SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768
display.WIDTH = SCREEN_WIDTH
display.HEIGHT = SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Set the background
display.set_background("background.png")

speed_scale = 1
speed_scale_base = 1

# Store pressed keys in a set. Good for quickly checking if a key is down.
pressed_keys = set()

# This linked list is used to keep track of objects for, for example, rendering
lives = 2
lost = False
offset = 0

pygame.mixer.init()
pygame.mixer.music.load('assets/sss.mp3')
pygame.mixer.music.play(-1)
round = 0

while True:
    if round == 1:
        pygame.mixer.music.load('assets/sssr.mp3')
        pygame.mixer.music.play(-1)

    object_list = objects.G_obj_list_el(None, None, None)

    # The player's data field will be used to track their projectile and its index
    # in the list of objects.
    player = objects.new_game_object([SCREEN_WIDTH / 2, 0.89713541 * SCREEN_HEIGHT],
            "skeleton.png")
    # This is always the first object, so the definition can be very specific.
    object_list.next = objects.G_obj_list_el(player, object_list, None)

    # The enemies' data fields will give their indices in the objects array and the
    # prawns array.
    prawns = objects.G_obj_list_el(None, None, None)
    prawnjectiles = objects.G_obj_list_el(None, None, None)
    p_dirx = 1
    p_switch_dir = False
    PL_WIDTH = 12
    PL_HEIGHT = 4
    n_prawns = PL_WIDTH * PL_HEIGHT
    p_width = int(40 * SCREEN_WIDTH / 1366)
    p_height = int(38 * SCREEN_HEIGHT / 1366)
    p_spacing = 55 / 1366 * SCREEN_WIDTH
    for i in range(0, PL_HEIGHT):
        for j in range(0, PL_WIDTH):
            p = objects.new_game_object([20 + p_spacing*j, 20 + offset + p_spacing*i],
                    "prawn.png")
            l = objects.G_obj_list_el(p, object_list, object_list.next)
            lp = objects.G_obj_list_el(p, prawns, prawns.next)
            p.data = [l, lp]
            objects.g_l_insert(object_list, l)
            objects.g_l_insert(prawns, lp)


    # Render everything once
    display.render_objects(object_list, screen)
    pygame.display.update()

    speed_scale = speed_scale_base
    speed_scale_base *= (1.02 ** PL_WIDTH)
    lives += 1

    while 1:
        for event in pygame.event.get():
            # Handle keys being pressed
            if event.type == pygame.KEYDOWN:
                # Sets do not allow repeated members, so we don't need to worry
                # about checking if the key is already listed.
                pressed_keys.add(event.key)
            elif event.type == pygame.KEYUP:
                # Remove the key from the set of pressed keys.
                if event.key in pressed_keys:
                    pressed_keys.remove(event.key)

        # See if the player has won
        if prawns.next == None:
            # Placeholder
            pygame.time.delay(2000)
            break
        # See if the player has lost
        if lives == 0 or lost:
            # Placeholder
            pygame.time.delay(5000)
            sys.exit()

        # Evolution of projectiles
        if player.data != None:
            if player.data[0].pos[1] < -5:
                l =  player.data[1]
                objects.g_l_remove(l)
                del l
                player.data = None

            else:
                objects.move(player.data[0], (0, -8*SCREEN_HEIGHT/768 * speed_scale))
        prjl = prawnjectiles.next
        while prjl != None:
            prj = prjl.data.data
            objects.move(prj, (0, 10*SCREEN_HEIGHT/768 * math.sqrt(speed_scale)))
            # Player collision
            if ((abs(player.pos[0] - prj.pos[0])) < (player.width + prj.width)/2 and
                (abs(player.pos[1] - prj.pos[1])) < (player.height + prj.height)/2):
                objects.g_l_remove(prjl.data)
                objects.g_l_remove(prjl)
                lives -= 1
            # Out of bounds
            if prj.pos[1] > 709 * SCREEN_HEIGHT / 768:
                objects.g_l_remove(prjl.data)
                objects.g_l_remove(prjl)
            # Projectile collision
            if (player.data != None and (abs(player.data[0].pos[0] - prj.pos[0])) <
                    (player.data[0].width + prj.width)/2
                    and (abs(player.data[0].pos[1] - prj.pos[1])) < 
                    (player.data[0].height + prj.height)/2):
                objects.g_l_remove(prjl.data)
                objects.g_l_remove(prjl)
                objects.g_l_remove(player.data[1])
                player.data = None
            prjl = prjl.next


        # Evolution of prawns
        pl = prawns.next
        while pl != None:
            p = pl.data
            objects.move(p, (2*SCREEN_WIDTH/1366 * p_dirx * speed_scale, 0))
            if p.pos[1] > player.pos[1] - 1/2 * player.height + p.height/2:
                lost = True
            # Check for a collision
            if player.data != None:
                projectile = player.data[0]
                if ((abs(projectile.pos[0] - p.pos[0])) < (projectile.width + p_width)/2
                        and (abs(projectile.pos[1] - p.pos[1])) < (projectile.width + p_width)/2):
                    # Delete prawn and projectile, and update indicies of others
                    objects.g_l_remove(player.data[1])
                    objects.g_l_remove(pl)
                    objects.g_l_remove(p.data[0])
                    player.data = None
                    speed_scale *= 1.02
                    n_prawns -= 1
            # Time for the prawn to fire
            if n_prawns > 0 and (random.random() < 0.0005 * PL_WIDTH * PL_HEIGHT *
                    speed_scale / (n_prawns)) :
                proj = objects.new_game_object(p.pos[:], "projectile.png")
                obj_l_el = objects.G_obj_list_el(proj, object_list, object_list.next)
                objects.g_l_insert(object_list, obj_l_el)
                proj_l_el = objects.G_obj_list_el(obj_l_el, prawnjectiles,
                        prawnjectiles.next)
                objects.g_l_insert(prawnjectiles, proj_l_el)



            if p.pos[0] < p_width / 2 or p.pos[0] > SCREEN_WIDTH - p_width / 2:
                p_switch_dir = True
            pl = pl.next
        if p_switch_dir:
            p_dirx *= -1
            pl = prawns.next
            while pl != None:
                p = pl.data
                objects.move(p, (0, p_spacing*0.8))
                pl = pl.next
            p_switch_dir = False

        keyboard.keyboard_handler(pressed_keys, object_list, player, speed_scale)
        display.render_objects(object_list, screen)
        pygame.display.update()
    offset += p_spacing
    round += 1
