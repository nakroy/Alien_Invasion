import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """管理飞船所发射子弹的类"""
    def __init__(self, ai_game):
        """在飞船当前位置创建一个子弹对象"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # 在(0, 0)处使用Rect类来创建一个表示子弹的矩形实例，再设置正确的位置
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop  # 子弹初始位置位于飞船的正上方

        # 存储用小数表示的子弹位置，以便调整子弹速度
        self.y = float(self.rect.y)

    def update(self):
        """向上移动子弹"""
        self.y -= self.settings.bullet_speed   # 更新表示子弹位置的小数值
        self.rect.y = self.y    # 更新表示子弹的rect位置

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        # draw.rect()函数用于存储在self.color颜色填充的子弹rect部分(self.rect)占据屏幕(self.screen)的部分
        pygame.draw.rect(self.screen, self.color, self.rect)

