import json


class GameStats:
    """跟踪游戏的统计信息的类"""
    def __init__(self, ai_game):
        """初始化统计信息"""
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False    # 游戏活动状态标志，True表示游戏进行中，False表示游戏停止
        self.pause_flag = False    # 暂停键的活动标志，False时表示不暂停，True表示暂停
        self.music_play_flag = False    # 背景音乐播放标志，True表示播放，False表示不播放
        self.high_score = 0      # 最高得分记录（第一次运行游戏时为0）
        with open('high_score.json') as f_obj:
            self.high_score = json.load(f_obj)     # 载入最高得分记录

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ship_left = self.settings.ship_limit  # 剩余可用飞船数初始时为最大可用飞船数
        self.score = 0       # 得分
        self.level = 1       # 游戏难度等级
