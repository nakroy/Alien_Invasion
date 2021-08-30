import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """管理飞船的类"""
    def __init__(self, ai_game):
        """初始化飞船并设置其初始位置"""
        super().__init__()
        self.screen = ai_game.screen  # ai_game是游戏程序实例
        self.settings = ai_game.settings # 给ship添加settings属性
        self.screen_rect = ai_game.screen.get_rect()  # get_rect()方法访问屏幕的rect属性，使我们能将飞船放到屏幕正确的位置

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()  # 将图像的rect属性赋值给飞船的rect图像

        # 对于每艘新飞船，都将其放在屏幕中央底部
        self.rect.midbottom = self.screen_rect.midbottom

        # 飞船位置属性
        self.x = float(self.rect.x)  # 位置精确到小数

        # 移动标志，标志为True时移动，False时停止移动
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """根据移动标志调整飞船位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:  # 第二个条件保证飞船触碰屏幕边缘时不会移出屏幕，下同
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x  # 根据self.x更新rect对象，rect对象只保留整数部分

    def blit_ship(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """让飞船在屏幕底端居中"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)




