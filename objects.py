import levels
import animations
import screen

BG_LIST = []
STATIC_LIST = []
DYNAMIC_OBJ_LIST = []

class Object():


    def __init__(self, animation_repertoire, x, y, velX, velY, friction, falls=True):
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
        self.height = self.get_height()
        self.width = self.get_width()

    def get_width(self):
        return self.animation_repertoire[self.object_state].return_frame().get_width()

    def get_height(self):
        return self.animation_repertoire[self.object_state].return_frame().get_height()

    def x_centre(self):
        return int(self.x + self.width/2)

    def y_centre(self):
        return self.y + self.height/2

    def abs_x_range(self):
        pass

    def top(self):
        return self.x

    def bottom(self):
        return self.y + self.get_height()

    def right_side(self):
        return self.x + self.width

    def translate(self, vecX, vecY):
        self.x += vecX
        self.y += vecY

    def get_floor_height(self, x):
        floor_level = levels.DEFAULT_FLOOR_LEVEL
        try:
            for level in sorted(levels.FLOOR_LEVEL_LIST[x], reverse=True):
                if level >= self.y + self.height:
                    floor_level = level
        except IndexError:
            pass
        return floor_level

    def process_surface_interractions(self):
        if self.bottom() >= self.floor_level:
            self.onFloor = True
            self.velY = 0
            self.y = self.floor_level - self.get_height()
        if self.onFloor:
            if abs(self.velX) < self.friction:
                self.velX = 0
            elif self.velX > 0:
                self.velX -= self.friction
            elif self.velX < 0:
                self.velX += self.friction
        if self.x_centre() <= 0:
            self.velX = 0
            self.x = 0 - (self.width/2)+1
        elif self.x_centre() >= screen.WIDTH:
            self.velX = 0
            self.x = screen.WIDTH - int(self.width/2)-1
        self.floor_level = self.get_floor_height(self.x_centre())

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

    def update(self):
        self.x += self.velX
        self.y += self.velY
        if self.falls:
            self.velY += levels.GRAVITY
        self.process_surface_interractions()
        self.draw()
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


class Static(Object):

    def __init__(self, img, x, y, velX=0, velY=0, friction=0, falls=False):
        super().__init__(img, x, y, velX, velY, friction, falls)
        STATIC_LIST.append(self)

    def get_walkable_surface(self):
        return (self.x, self.x + self.width)

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