import levels
import animations
import screen

BG_LIST = []
STATIC_LIST = []
DYNAMIC_OBJ_LIST = []

class Object():


    def __init__(self, animation_repertoire, x, y, velX, velY, friction, falls=True, collisions=True):
        self.animation_repertoire = animation_repertoire
        self.x = x
        self.y = y
        self.velX = velX
        self.velY = velY
        self.onFloor = False
        self.floor_level = levels.DEFAULT_FLOOR_LEVEL
        self.friction = friction
        self.object_state = 'still'
        self.falls = falls
        self.collisions = collisions
        self.height = self.get_height()
        self.width = self.get_width()

    def get_width(self):
        return self.animation_repertoire[self.object_state].return_frame().get_width()

    def get_height(self):
        return self.animation_repertoire[self.object_state].return_frame().get_height()

    def get_rect(self):
        return ((self.x, self.y),
                (self.right_side(), self.y),
                (self.right_side(), self.bottom(),)
                (self.x, self.bottom()))

    def x_centre(self):
        return int(self.x + self.width/2)

    def y_centre(self):
        return self.y + self.height/2

    def top(self):
        return self.x

    def bottom(self):
        return self.y + self.get_height()

    def right_side(self):
        return self.x + self.width

    def translate(self, vecX, vecY):
        self.x += vecX
        self.y += vecY


    def collision_detected(self, other):
        if other.collisions:
            if self.right_side() >= other.x and self.x <= other.right_side():
                if self.bottom() >= other.y and self.y <= other.bottom():
                    return True
        else:
            return False

    def collision_side(self, other):
        if self.collision_detected(other):
            if self.right_side() > other.x:
                return 'right'
            elif self.x < other.right_side():
                return 'left'
            elif self.y > other.bottom():
                return 'top'
            elif self.bottom() < other.y():
                return 'bottom'
            else:
                return None


    def process_applicable_floor(self, x):
        floor_level = levels.DEFAULT_FLOOR_LEVEL
        try:
            for level in sorted(levels.FLOOR_LEVEL_LIST[x], reverse=True):
                if level >= self.y + self.height:
                    floor_level = level
        except IndexError:
            pass
        return floor_level

    def floor_behaviour(self):
        #Stops Obj falling through whatever floor its on
        if self.bottom() >= self.floor_level:
            self.onFloor = True
            self.velY = 0
            self.y = self.floor_level - self.get_height()
        #Gives object friction so it doesn't slide along the floor forever
        if self.onFloor:
            if abs(self.velX) < self.friction:
                self.velX = 0
            elif self.velX > 0:
                self.velX -= self.friction
            elif self.velX < 0:
                self.velX += self.friction

    def screen_edge_behaviour(self):
        #What will the object do when it goes beyond the bounds of the screen?
        if self.x_centre() <= 0:
            self.velX = 0
            self.x = 0 - (self.width/2)+1
        elif self.x_centre() >= screen.WIDTH:
            self.velX = 0
            self.x = screen.WIDTH - int(self.width/2)-1

    def process_surface_interractions(self):
        self.floor_behaviour()
        self.screen_edge_behaviour()
        self.floor_level = self.process_applicable_floor(self.x_centre())

    def draw(self):
        screen.DISPLAY.blit(self.animation_repertoire[self.object_state].return_frame(), (self.x, self.y))
        self.animation_repertoire[self.object_state].advance_frame()

    def update(self):
        self.x += self.velX
        self.y += self.velY
        if self.falls:
            self.velY += levels.GRAVITY
        self.process_surface_interractions()
        self.draw()




class Player(Object):

    def __init__(self, img, x, y, velX, velY, friction):
        super().__init__(img, x, y, velX, velY, friction)
        self.speed_increment = 1
        self.max_vel = 2
        self.jump_power = 10

    def move(self, direction):
        if direction == 'right' and self.velX < self.max_vel:
            self.velX += self.speed_increment
        elif direction == 'left' and self.velX > -self.max_vel:
            self.velX -= self.speed_increment
        elif direction == 'jump' and self.onFloor:
            self.velY = -self.jump_power
            self.onFloor = False

    def choose_animation(self):
        if self.onFloor:
            if self.velX == 0:
                self.object_state = 'still'
            if self.velX > 0:
                self.object_state = 'running_right'
            elif self.velX < 0:
                self.object_state = 'running_left'
        elif not self.onFloor and type(self).__name__ is not 'Background':
            if self.velX > 0:
                self.object_state = 'jumping_right'
            elif self.velX < 0:
                self.object_state = 'jumping_left'
            else:
                self.object_state = 'jumping_up'

    def process_surface_interractions(self):
        self.floor_behaviour()
        self.screen_edge_behaviour()
        for obj in STATIC_LIST:
            if self.collision_side(obj):
                print(self.collision_side(obj))
            if self.collision_side(obj) == 'top':
                self.velY -= self.speed_increment
            elif self.collision_side(obj) == 'left':
                self.velX += self.speed_increment
            elif self.collision_side(obj) == 'bottom':
                self.velY += self.speed_increment
            elif self.collision_side(obj) == 'right':
                self.velX -= self.speed_increment
        self.floor_level = self.process_applicable_floor(self.x_centre())

    def update(self):
        self.process_surface_interractions()
        self.x += self.velX
        self.y += self.velY
        if self.falls:
            self.velY += levels.GRAVITY
        self.choose_animation()
        self.draw()


class Static(Object):

    def __init__(self, img, x, y, velX=0, velY=0, friction=0, falls=False, collisions=True):
        super().__init__(img, x, y, velX, velY, friction, falls, collisions)
        STATIC_LIST.append(self)


    def get_walkable_surface(self):
        if self.collisions:
            return (self.x, self.x + self.width)
        else:
            return (0, 0)

    def get_walls(self):
        if self.collisions:
            return ((self.x, self.x + self.width),
                    (self.x + self.width, self))

class Background(Object):

    def __init__(self, img, x, y, velX=0, velY=0, friction=0, falls=False):
        super().__init__(img, x, y, velX, velY, friction, falls)
        BG_LIST.append(self)

    def update(self):
        self.x += self.velX
        self.y += self.velY
        self.process_surface_interractions()
        self.draw()

    def process_surface_interractions(self):
        if self.x > screen.WIDTH:
            self.x = -screen.WIDTH
        # elif self.x < -screen.WIDTH and self.velX < 0:
        #     self.x = screen.WIDTH

