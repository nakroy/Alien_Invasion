import sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import json


class AlienInvasion:
    """管理游戏资源和行为的类"""
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()  # 使用pygame.init()初始化背景设置
        self.settings = Settings()  # 初始化设置实例，使用Settings类
        self.screen = pygame.display.set_mode((
            self.settings.screen_width, self.settings.screen_height
        ))   # set_mode()设置游戏窗口大小
        pygame.display.set_caption("Alien Invasion")  # set_caption()显示游戏标题
        pygame.mixer.init()     # 初始化pygame的音乐播放模块
        pygame.mixer.music.load('music/Vicetone - Tremble.flac')   # 加载背景音乐
        self.ship = Ship(self)  # 创建飞船实例
        self.bullets = pygame.sprite.Group()   # 创建子弹实例编组
        self.aliens = pygame.sprite.Group()    # 创建外星人实例编组
        self._create_fleet()          # 创建外星人群
        self.stats = GameStats(self)   # 创建用于存储游戏统计信息的实例
        self.play_button = Button(self, "Play", 'topright')       # 创建Play按钮
        self.pause_button = Button(self, "Pause", 'right')     # 创建Pause按钮
        self.end_game_button = Button(self, "End Game", "bottomright")   # 创建End Game按钮
        self.sb = Scoreboard(self)        # 创建计分板

    def run_game(self):
        """开始游戏主循环"""
        while True:
            self._check_events()
            if self.stats.game_active and not self.stats.pause_flag:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_screen()

            elif not self.stats.game_active:
                self.screen.fill(self.settings.bg_color)  # fill()为颜色渲染方法，将背景色填充屏幕
                self.play_button.draw_button()
                self.pause_button.draw_button()
                self.end_game_button.draw_button()
                pygame.display.flip()   # flip()函数用于屏幕刷新，不断更新外星人和飞船的位置

    def _check_events(self):
        """响应鼠标和按键事件"""

        # 监视键盘和鼠标事件，event.get()返回上一次调用后所有操作事件所组成的列表
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pygame.QUIT事件指玩家关闭游戏窗口的操作
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:   # MOUSEBUTTONDOWN是对按下鼠标键的检测
                mouse_pos = pygame.mouse.get_pos()   # mouse.get_pos()返回鼠标按下时的x,y坐标
                self._check_play_button(mouse_pos)
                self._check_pause_button(mouse_pos)
                self._check_end_game_button(mouse_pos)

            # 飞船按键事件监视，模拟飞船的左右移动
            elif event.type == pygame.KEYDOWN:  # KEYDOWN是对按下键的事件监视
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:  # KEYUP是对松开键的事件监视
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        """让玩家在单击Play按钮时开始新游戏"""
        button_click = self.play_button.rect.collidepoint(mouse_pos)
        if button_click and not self.stats.game_active:   # 鼠标按下并且游戏处于停止状态时，响应Play按钮事件
            # 按下Play按钮时需要重置统计信息，重置游戏场景
            self.stats.reset_stats()
            self.stats.game_active = True
            self.stats.music_play_flag = True
            self.sb.prep_score()
            self.sb.prep_high_score()
            self.sb.prep_level()
            self.sb.prep_ship()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            pygame.mixer.music.play(-1)             # 循环播放背景音乐
            self.settings.initialize_dynamic_settings()

    def _check_pause_button(self, mouse_pos):
        """让玩家在单击Pause按钮时暂停游戏，再次点击时继续游戏"""
        button_click = self.pause_button.rect.collidepoint(mouse_pos)
        if button_click and self.stats.game_active and not self.stats.pause_flag:   # 鼠标按下且游戏处于运行状态时，响应Pause按钮事件
            self.stats.pause_flag = True
            pygame.mixer.music.pause()
            self.stats.music_play_flag = False
        elif button_click and self.stats.game_active and self.stats.pause_flag:     # 再次按下Pause按钮时继续游戏
            self.stats.pause_flag = False
            pygame.mixer.music.unpause()
            self.stats.music_play_flag = True

    def _check_end_game_button(self, mouse_pos):
        """让玩家在单击End Game按钮时退出游戏"""
        button_click = self.end_game_button.rect.collidepoint(mouse_pos)
        if button_click:
            sys.exit()

    def _check_keydown_events(self, event):
        """响应按键按下事件"""
        if event.key == pygame.K_RIGHT:  # 按右键向右移动飞船
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:  # 按左键向左移动飞船
            self.ship.moving_left = True
        elif event.key == pygame.K_ESCAPE:    # 按Esc快捷键退出游戏
            sys.exit()
        elif event.key == pygame.K_SPACE:   # 按空格键发射子弹
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """响应按键松开事件"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets中"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹位置并删除消失子弹"""
        # 更新子弹位置
        self.bullets.update()
        # 删除消失子弹
        for bullet in self.bullets.copy():  # 遍历子弹编组的副本(直接遍历子弹编组无法完整实现remove操作)
            if bullet.rect.bottom <= 0:  # 当子弹飞离屏幕顶部时，删除子弹
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision()

    def _create_alien(self, alien_number, row_number):
        """创建外星人, alien_number决定每行创建多少外星人，row_number决定创建多少行外星人"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _create_fleet(self):
        """创建外星人群"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size   # size返回包含宽度和高度的元组
        available_space_x = self.settings.screen_width - (2 * alien_width)  # 2 * alien_width为预留的屏幕两边的空白间距
        number_alien_x = available_space_x // (2 * alien_width)   # 每两个外星人之间的间距是外星人的宽度
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)   # 外星人的行距为外星人的高度
        for row_number in range(number_rows):
            for alien_number in range(number_alien_x):
                self._create_alien(alien_number, row_number)

    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整群外星人下移，并改变横移方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_bullet_alien_collision(self):
        """检查和响应子弹与外星人碰撞事件"""
        collisions = pygame.sprite.groupcollide(     # 检查子弹是否击中外星人
            self.bullets, self.aliens, True, True)   # groupcollide()用于检查子弹和外星人rect属性是否有重叠，True表示重叠时删除对象
        if collisions:    # 如果击中外星人则增加得分
            for aliens in collisions.values():   # 遍历collisions的字典键值对，确保每个子弹击中的外星人都能得分
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:          # 检查是否需要生成新的外星人群
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()    # 将这一批外星人消灭后，游戏难度升级
            self.stats.level += 1
            self.sb.prep_level()

    def _ship_hit(self):
        """响应外星人与飞船相撞事件"""
        if self.stats.ship_left > 1:
            self.stats.ship_left -= 1   # 外星人与飞船相撞时可用飞船数减一
            self.sb.prep_ship()

            # 清空余下外星人和子弹并重新创建一群外星人
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()

            self.ship.center_ship()   # 让飞船重新出现在屏幕底端中央
            sleep(0.5)   # 游戏暂停0.5秒，让玩家知道飞船和外星人相撞
        else:
            with open('high_score.json', 'w') as file_object:    # 保存最高得分纪录
                json.dump(self.stats.high_score, file_object)
            pygame.mixer.music.stop()     # 停止背景音乐
            self.stats.game_active = False   # 飞船可用次数用完时游戏结束

    def _check_aliens_bottom(self):
        """响应外星人到达屏幕底端事件"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:  # 检查是否有外星人到达屏幕底端
                self._ship_hit()   # 响应时按照外星人与飞船相撞处理
                break   # 只需检测到一个外星人即可响应，无需全部循环完

    def _update_aliens(self):
        """更新外星人群中所有外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):  # 检测是否有外星人和飞船相撞
            self._ship_hit()   # 相撞时响应事件
        self._check_aliens_bottom()  # 检测是否有外星人到达屏幕底部并响应事件

    def _update_screen(self):
        """更新屏幕图像并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)  # 每次循环时都改变背景色，fill()将背景色填充屏幕
        self.ship.blit_ship()  # 在屏幕上显示飞船
        for bullet in self.bullets.sprites():  # sprites()返回一个包含编组bullets所有精灵的列表，在屏幕上绘制每个精灵
            bullet.draw_bullet()
        self.aliens.draw(self.screen)    # 用draw函数接收屏幕参数，在屏幕上绘制外星人
        self.sb.show_score()     # 显示得分
        if not self.stats.game_active:    # 游戏处于非活动状态时绘制Play按钮
            self.play_button.draw_button()
        self.pause_button.draw_button()
        self.end_game_button.draw_button()
        pygame.display.flip()   # flip()函数用于屏幕刷新，不断更新外星人和飞船的位置


if __name__ == '__main__':
    # 创建游戏实例并运行
    ai = AlienInvasion()
    ai.run_game()