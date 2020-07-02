import screen
import objects
#In Game Variables
GRAVITY = 1
FRICTION = 1
DEFAULT_FLOOR_LEVEL = screen.HEIGHT - 5
FLOOR_LEVEL = DEFAULT_FLOOR_LEVEL

FLOOR_LEVEL_LIST = []

def update_floor_height():
    level_list = [[DEFAULT_FLOOR_LEVEL] for i in range(screen.WIDTH)]
    for surface in objects.STATIC_LIST:
        surface_range = surface.get_walkable_surface()
        for pixel in range(surface_range[0], surface_range[1]):
            try:
                if surface.y not in level_list[pixel]:
                    level_list[pixel].append(surface.y)
            except IndexError:
                continue
    return level_list

for pixel in range(screen.WIDTH):
    FLOOR_LEVEL_LIST.append([DEFAULT_FLOOR_LEVEL])

update_floor_height()