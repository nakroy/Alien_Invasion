import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """表示单个外星人的类"""
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # 加载外星人图像设置其rect属性
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # 让每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect. width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def update(self):
        """外星人移动"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """检测外星人是否触碰屏幕边缘"""
        screen_rect = self.screen.get_rect()   # 获取屏幕边缘rect属性
        if self.rect.right >= screen_rect.right or self.rect.left <= screen_rect.left:
            return True
