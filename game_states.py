class GameStates:
    """游戏的统计信息"""

    def __init__(self, ai_game):
        """初始化统计信息"""
        self.settings = ai_game.settings
        self.reset_states()
        # 游戏的活跃状态
        self.game_active = False
        # 最高得分
        self.high_score = 0

    def reset_states(self):
        """初始化在游戏期间可能发生变化的统计信息"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
