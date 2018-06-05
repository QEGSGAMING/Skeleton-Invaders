import pygame
import pygame.transform

import os


# Store display dimensions
WIDTH = 0
HEIGHT = 0

# This will be an array of all the unique images used by the program
images = []
# The dictionary is to map image names to indices in the above array. This will
# give slightly better performance as repeated string comparisons are avoided
image_file_indices = {}

def load_image(image_name, bg=False):
    # This works for both loading images into memory and finding the numbers
    # corresponding to stored images.
    # Allocate memory for the image only if necessary
    global images
    global image_file_indices
    if image_name in image_file_indices.keys():
        return image_file_indices[image_name]
    else:
        i = None
        if image_name[-3:] == "png":
            i = pygame.image.load(os.path.join("assets",
                image_name)).convert_alpha()
        else:
            i = pygame.image.load(os.path.join("assets",
                image_name)).convert()
        if bg:
            i = pygame.transform.scale(i, (WIDTH, HEIGHT))
        images.append(i)
        l = len(images) - 1
        image_file_indices[image_name] = l
        return l

background_idx = None
def set_background(image_name):
    global background_idx
    background_idx = load_image(image_name, bg=True)


def draw_object(obj, screen):
    screen.blit(images[obj.img_idx], (int(obj.pos[0] - obj.width/2),
        int(obj.pos[1] - obj.height/2)))


def render_objects(lst, screen):
    # Clear the screen
    #screen.fill((0, 0, 0))
    # Draw the background
    if background_idx != None:
        screen.blit(images[background_idx], (0, 0))
    # Draw the objects
    o = lst.next
    while o != None:
        draw_object(o.data, screen)
        o = o.next



