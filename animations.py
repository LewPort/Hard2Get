import pygame
import objects
import random
import objects
import time

class Animation():

    def __init__(self, frame_list, frame_delta, loop_delay, random=False, flip_x=False, flip_y=False):
        self.raw_frame_list = frame_list
        self.frame_list = self.load_frames(self.raw_frame_list)
        self.flip_x = flip_x
        self.flip_y = flip_y
        if flip_x:
            self.flip_x_frame_list = self.load_frames(self.raw_frame_list, flip_x=True)
        if flip_y:
            self.flip_y_frame_list = self.load_frames(self.raw_frame_list, flip_y=True)
        self.frame_delta = frame_delta/1000
        self.current_frame = 0
        self.last_frame_time = time.time()
        self.random_order = random

    def __len__(self):
        return len(self.frame_list)-1

    def load_frames(self, rawframes, flip_x=False, flip_y=False):
        tempList = []
        for frame in rawframes:
            frame = pygame.image.load(frame)
            # frame = pygame.transform.scale(frame, (200,200))
            if flip_x:
                frame = pygame.transform.flip(frame, True, False)
            elif flip_y:
                frame = pygame.transform.flip(frame, False, True)
            tempList.append(frame)
        return tempList

    def advance_frame(self):
        if self.last_frame_time + self.frame_delta <= time.time():
            if self.random_order:
                self.current_frame = random.randint(0, len(self))
            elif self.current_frame == len(self):
                self.current_frame = 0
            else:
                self.current_frame += 1
            self.last_frame_time = time.time()

    def return_frame(self):
        if self.flip_x:
            return self.flip_x_frame_list[self.current_frame]
        if self.flip_y:
            return self.flip_y_frame_list[self.current_frame]
        else:
            return self.frame_list[self.current_frame]

playerAnimationRepertoire = {'running_right':
                                 Animation(['anim/run1.png',
                                            'anim/run2.png',
                                            'anim/run3.png',
                                            'anim/run2.png'],
                                           100, 1000),
                             'running_left':
                                 Animation(['anim/run1.png',
                                            'anim/run2.png',
                                            'anim/run3.png',
                                            'anim/run2.png'],
                                           100, 1000, flip_x=True),
                             'jumping_right':
                                 Animation(['anim/run3.png'],
                                           200, 1000),
                             'jumping_left':
                                 Animation(['anim/run3.png'],
                                           200, 1000, flip_x=True),
                             'still':
                                 Animation(['anim/still1.png',
                                            'anim/still2.png',
                                            'anim/still3.png'],
                                           500, 1000, random=True)}

box1AnimationRepertoire = {'still':
                               Animation(['anim/box1.png'], 0, 0)}

bg = {'still': Animation(['anim/bg.png'], 0, 0)}