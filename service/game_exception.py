class GameBaseException(Exception):
    """游戏基础异常"""
    pass


class InvalidMoveException(GameBaseException):
    """无效移动方向异常"""
    pass


class BoardFullException(GameBaseException):
    """棋盘已满，无法生成新数字"""
    pass
