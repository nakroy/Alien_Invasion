import pygame


class Trump:
    """管理人物Trump的类"""
    def __init__(self, ai_game):
        """初始化人物Trump并设置其初始位置"""
        self.screen = ai_game.screen  # ai_game是游戏程序实例
        self.screen_rect = ai_game.screen.get_rect()  # get_rect()方法访问屏幕的rect属性，使我们能将人物放到屏幕正确的位置

        # 加载人物Trump图像并获取其外接矩形
        self.image = pygame.image.load('images/trump.bmp')
        self.rect = self.image.get_rect()  # 将图像的rect属性赋值给人物的rect属性

        # 对于每个人物Trump，都将其放在屏幕右上角
        self.rect.topleft = self.screen_rect.topleft

    def blit_trump(self):
        """在指定位置绘制人物Trump"""
        self.screen.blit(self.image, self.rect)