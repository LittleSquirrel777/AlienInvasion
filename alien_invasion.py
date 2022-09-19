import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()
        # self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # 这里修改游戏屏幕大小为整个屏幕
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.ship = Ship(self)
        self.settings.screen_width = self.screen.get_width()
        self.settings.screen_height = self.screen.get_height()
        # 创建存储子弹的编组
        self.bullets = pygame.sprite.Group()

        # 创建存储外星人的编组
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        pygame.display.set_caption("Alien Invasion")

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullet()
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

    def _update_screen(self):
        """更新屏幕图像，并切换到到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        """绘制每一个子弹"""
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        pygame.display.flip()


if __name__ == '__main__':
    alien = AlienInvasion()
    alien.run_game()
