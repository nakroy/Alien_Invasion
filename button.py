import pygame.font


class Button:
    """管理按钮属性的类"""
    def __init__(self, ai_game, msg, location='center', y=0):
        """初始化按钮属性"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # 设置按钮尺寸和其他属性
        self.width, self.height = 200, 50
        self.button_color = (255, 0, 0)       # 红色按钮
        self.text_color = (255, 255, 255)     # 白色字体
        self.font = pygame.font.SysFont("arial", 40)   # SysFont()指定了渲染文本的字体和字体型号

        # 创建按钮rect对象，再设置其位置
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        if location == 'center':
            self.rect.center = self.screen_rect.center
        elif location == 'right':
            self.rect.right = self.screen_rect.right
            self.rect.top = 700
        elif location == 'topright':
            self.rect.right = self.screen_rect.right
            self.rect.top = 500
        elif location == 'bottomright':
            self.rect.bottomright = self.screen_rect.bottomright
        self.rect.y += int(y)
        self._prep_msg(msg)     # 创建按钮标签

    def _prep_msg(self, msg):
        """将msg渲染为图像，并使其在按钮上居中"""
        # font.render()方法将msg文本转换为图像并存储在self.msg_image中，True表示开启反锯齿功能
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center      # 使msg_image图像处于按钮对象的位置

    def draw_button(self):
        """绘制颜色填充的按钮，再绘制文本"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)