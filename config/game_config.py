# 棋盘大小 4*4
BOARD_SIZE = 4
# 格子大小
CELL_SIZE = 100
# 边距
CELL_PADDING = 10
# 窗口尺寸
WINDOW_WIDTH = BOARD_SIZE * CELL_SIZE + (BOARD_SIZE + 1) * CELL_PADDING
WINDOW_HEIGHT = BOARD_SIZE * CELL_SIZE + (BOARD_SIZE + 1) * CELL_PADDING + 80

# 数字背景配色
COLOR_MAP = {
    0: "#cdc1b4",
    2: "#eee4da",
    4: "#ede0c8",
    8: "#f2b179",
    16: "#f59563",
    32: "#f67c5f",
    64: "#f65e3b",
    128: "#edcf72",
    256: "#edcc61",
    512: "#edc850",
    1024: "#edc53f",
    2048: "#edc22e",
}
DEFAULT_COLOR = "#3c3a32"
