import sys
import pygame
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_states import GameStates
from button import Button
from scoreboard import ScoreBoard


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # 这里修改游戏屏幕大小为整个屏幕
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_width()
        # self.settings.screen_height = self.screen.get_height()
        pygame.display.set_caption("Alien Invasion")
        # 创建一个飞船实例
        self.ship = Ship(self)
        # 创建一个存储游戏统计信息的实例
        self.states = GameStates(self)
        # 创建一个计分的实例
        self.sb = ScoreBoard(self)
        # 创建存储子弹的编组
        self.bullets = pygame.sprite.Group()
        # 创建存储外星人的编组
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        # 创建一个按钮
        self.play_button = Button(self, "Play")

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()

            if self.states.game_active:
                self.ship.update()
                self._update_bullet()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """响应按键"""
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """响应松开键盘"""
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

    def _check_play_button(self, mouse_pos):
        """玩家单机Play按钮开始新游戏"""
        if self.play_button.rect.collidepoint(mouse_pos) and not self.states.game_active:
            # 重置游戏状态
            self.states.game_active = True
            self.states.reset_states()
            # 重新绘制分数
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            # 清空编组
            self.bullets.empty()
            self.aliens.empty()
            # 重新生成外星人
            self._create_fleet()
            self.ship.center_ship()
            # 隐藏光标
            pygame.mouse.set_visible(False)
            # 重新设置一部分游戏的状态
            self.settings.initialize_dynamic_settings()

    def _fire_bullet(self):
        """发射子弹添加到编组中"""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_bullet(self):
        """更新所有子弹的位置，删除超过屏幕上界的子弹"""
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """删除发生碰撞的子弹和外星人"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            # 根据消灭的外星人增加其分数
            for aliens in collisions.values():
                self.states.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        # 如果外星人被消灭完了，重新创建外星人群
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            # 一群外星人消灭完，提高速度
            self.settings.increase_speed()
            # 提高等级
            self.states.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        """创建一群外星人"""
        new_alien = Alien(self)
        alien_width = new_alien.rect.width
        alien_height = new_alien.rect.height
        # 计算一行能容纳多少外星人
        available_space_x = self.settings.screen_width - 2 * alien_width
        number_alien_x = available_space_x // (2 * alien_width)
        # 计算屏幕能容纳多少行外星人
        available_space_y = self.settings.screen_height - (3 * alien_height) - self.ship.rect.height
        number_alien_y = available_space_y // (2 * alien_height)

        # 外循环行数，内循环每行外星人
        for row_number in range(number_alien_y):
            for alien_number in range(number_alien_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """创建一个外星人"""
        new_alien = Alien(self)
        alien_width, alien_height = new_alien.rect.size
        # 计算外星人的横坐标
        new_alien.x = alien_width + 2 * alien_width * alien_number
        new_alien.rect.x = new_alien.x
        # 计算外星人的纵坐标
        new_alien.rect.y = alien_height + 2 * alien_height * row_number
        self.aliens.add(new_alien)

    def _update_aliens(self):
        """更新外星人的位置，在外星人到达屏幕下边界以及与飞船碰撞时作出响应"""
        self._check_fleet_edges()
        self.aliens.update()
        # 外星人和飞船发生了碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # 检查是否有外星人到达屏幕下界
        self._check_aliens_bottom()

    def _ship_hit(self):
        """响应飞船被外星人撞到"""
        if self.states.ships_left > 1:
            # 将飞船的数量减1
            self.states.ships_left -= 1
            self.sb.prep_ships()
            # 将屏幕中的子弹和外星人清空
            self.aliens.empty()
            self.bullets.empty()
            # 重新创建外星人并将飞船居中
            self._create_fleet()
            self.ship.center_ship()
            # 停顿一会
            sleep(0.5)
        else:
            self.states.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕的下边界"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _check_fleet_edges(self):
        """检查是否有外星人到达了两边的边界"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """存在外星人到达边界时，修改外星人群的y以及移动方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """更新屏幕图像，并切换到到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        """绘制每一个子弹"""
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        # 显示得分
        self.sb.show_score()
        if not self.states.game_active:
            self.play_button.draw_button()
        pygame.display.flip()


if __name__ == '__main__':
    alien = AlienInvasion()
    alien.run_game()
