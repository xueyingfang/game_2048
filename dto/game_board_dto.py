from typing import List


class GameBoardDTO:
    def __init__(self):
        # 4*4棋盘二维列表
        self.board: List[List[int]] = [[0 for _ in range(4)] for _ in range(4)]
        self.score: int = 0
        self.is_game_over: bool = False
        self.is_win: bool = False
        # 新增：暂停标记
        self.is_paused: bool = False

    def reset(self):
        """重置游戏数据"""
        self.board = [[0 for _ in range(4)] for _ in range(4)]
        self.score = 0
        self.is_game_over = False
        self.is_win = False
        self.is_paused = False
