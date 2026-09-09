import random
from typing import List, Tuple
from dto.game_board_dto import GameBoardDTO
from service.game_exception import InvalidMoveException, BoardFullException
from config.game_config import DIFFICULTY_CONFIG


class Game2048Service:
    @staticmethod
    def add_random_number(dto: GameBoardDTO):
        """根据当前难度，在空白位置随机生成2或4"""
        empty_positions: List[Tuple[int, int]] = []
        for i in range(4):
            for j in range(4):
                if dto.board[i][j] == 0:
                    empty_positions.append((i, j))
        if not empty_positions:
            raise BoardFullException("棋盘已满，无法生成新方块")

        # 读取当前难度的4生成概率
        prob_4 = DIFFICULTY_CONFIG[dto.difficulty]["prob_4"]
        row, col = random.choice(empty_positions)
        dto.board[row][col] = 4 if random.random() < prob_4 else 2

    @staticmethod
    def _merge_one_row(row: List[int]) -> Tuple[List[int], int]:
        """
        单行向左合并
        :param row: 原始行数组
        :return: (合并之后的新行, 本次合并获得的分数)
        """
        nums = [v for v in row if v != 0]
        add_score = 0
        for i in range(len(nums) - 1):
            if nums[i] == nums[i + 1]:
                merge_val = nums[i] * 2
                nums[i] = merge_val
                nums[i + 1] = 0
                add_score += merge_val // 4

        nums = [v for v in nums if v != 0]
        while len(nums) < 4:
            nums.append(0)
        return nums, add_score

    @staticmethod
    def move_left(dto: GameBoardDTO) -> bool:
        old_board = [r.copy() for r in dto.board]
        total_add = 0
        for idx in range(4):
            new_row, score = Game2048Service._merge_one_row(dto.board[idx])
            dto.board[idx] = new_row
            total_add += score
        dto.score += total_add
        return old_board != dto.board

    @staticmethod
    def move_right(dto: GameBoardDTO) -> bool:
        old_board = [r.copy() for r in dto.board]
        total_add = 0
        for idx in range(4):
            reversed_row = dto.board[idx][::-1]
            merged, score = Game2048Service._merge_one_row(reversed_row)
            dto.board[idx] = merged[::-1]
            total_add += score
        dto.score += total_add
        return old_board != dto.board

    @staticmethod
    def move_up(dto: GameBoardDTO) -> bool:
        old_board = [r.copy() for r in dto.board]
        transpose = list(zip(*dto.board))
        transpose = [list(item) for item in transpose]
        total_add = 0
        for i in range(4):
            new_row, score = Game2048Service._merge_one_row(transpose[i])
            transpose[i] = new_row
            total_add += score
        dto.board = [list(x) for x in zip(*transpose)]
        dto.score += total_add
        return old_board != dto.board

    @staticmethod
    def move_down(dto: GameBoardDTO) -> bool:
        old_board = [r.copy() for r in dto.board]
        transpose = list(zip(*dto.board))
        transpose = [list(item) for item in transpose]
        total_add = 0
        for i in range(4):
            rev = transpose[i][::-1]
            merged, score = Game2048Service._merge_one_row(rev)
            transpose[i] = merged[::-1]
            total_add += score
        dto.board = [list(x) for x in zip(*transpose)]
        dto.score += total_add
        return old_board != dto.board

    @staticmethod
    def move(dto: GameBoardDTO, direction: str) -> bool:
        direction_map = {
            "left": Game2048Service.move_left,
            "right": Game2048Service.move_right,
            "up": Game2048Service.move_up,
            "down": Game2048Service.move_down
        }
        if direction not in direction_map:
            raise InvalidMoveException(f"非法移动方向:{direction}")
        return direction_map[direction](dto)

    @staticmethod
    def check_game_status(dto: GameBoardDTO):
        """检查胜利/失败状态，根据难度判断胜利目标"""
        win_target = DIFFICULTY_CONFIG[dto.difficulty]["win_target"]
        # 判断胜利：达到目标值
        for row in dto.board:
            if win_target in row:
                dto.is_win = True

        # 存在空格，游戏继续
        for row in dto.board:
            if 0 in row:
                dto.is_game_over = False
                return

        # 无空格，检查是否还可以合并
        can_merge = False
        size = 4
        for i in range(size):
            for j in range(size):
                if j + 1 < size and dto.board[i][j] == dto.board[i][j+1]:
                    can_merge = True
                if i + 1 < size and dto.board[i][j] == dto.board[i+1][j]:
                    can_merge = True
        dto.is_game_over = not can_merge

    @staticmethod
    def init_new_game(dto: GameBoardDTO):
        """初始化一局新游戏，生成两个随机方块"""
        dto.reset()
        Game2048Service.add_random_number(dto)
        Game2048Service.add_random_number(dto)
