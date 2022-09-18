import pygame


class Ship:
    """管理飞船的类"""
    def __init__(self, ai_game):
        """初始化飞船，并设置其初始位置"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        """加载飞船图像并获取其外接矩形"""
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()

        """设置飞船的初始位置"""
        self.rect.midbottom = self.screen_rect.midbottom

        """存储飞船的实际位置"""
        self.x = float(self.rect.x)

        """设置飞船的移动标记"""
        self.moving_left = False
        self.moving_right = False

    def update(self):
        """根据标记移动飞船的实际位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        """重新设置飞船的位置"""
        self.rect.x = self.x

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)
