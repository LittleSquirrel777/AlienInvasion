class Settings:
    """游戏的配置类"""
    def __init__(self):
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 飞船的设置
        self.ship_speed = 1.5
        self.ship_limit = 3

        # 子弹设置
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)

        # 外星人的设置
        self.alien_speed = 3.5
        self.fleet_drop_speed = 10
        # 1表示向左移动，-1表示向右移动
        self.fleet_direction = 1
