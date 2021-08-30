import pygame


file_name = "music\Martin Garrix,Clinton Kane - Drown (feat. Clinton Kane).mp3"
pygame.mixer.init()
pygame.mixer.music.load(file_name)
pygame.mixer.music.play(1)