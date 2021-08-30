class Settings:
    """存储游戏中所有设置的类"""
    def __init__(self):
        """初始化游戏设置"""
        # 屏幕设置
        self.screen_width = 1600
        self.screen_height = 900
        self.bg_color = (255, 255, 255)   # 背景色设置白色

        # 飞船属性设置
        self.ship_speed = 1.5  # 飞船横移速度
        self.ship_limit = 3    # 飞船可用次数

        # 子弹属性设置
        self.bullet_speed = 1.5  # 子弹垂直移动速度
        self.bullet_width = 30
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3       # 允许最大射击子弹数量

        # 外星人属性设置
        self.alien_speed = 1.0   # 外星人横移速度
        self.fleet_drop_speed = 20   # 外星人下落速度
        self.fleet_direction = 1   # 外星人移动方向标志，1为向右移动，-1为向左移动

        # 游戏难度设置
        self.speedup_scale = 1.1  # 游戏节奏速度
        self.score_scale = 1.5    # 难度升级时射杀外星人的得分奖励提升速度
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0
        self.fleet_direction = 1
        self.alien_points = 50  # 每射杀一个外星人的得分

    def increase_speed(self):
        """提高游戏速度设置"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

