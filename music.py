import pygame

playlist=['music/make_it_shine.ogg']

class Music:


    def __init__(self, playlist):
        self.playlist = playlist
        self.playlist = [pygame.mixer.load(track) for track in self.playlist]



    def play(self):
        pygame.music.mixer.play(self.playlist[0])

    def stop(self):
        pygame.music.mixer.stop(self.playlist[0])