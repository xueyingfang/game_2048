import json
import os
from dto.game_board_dto import GameBoardDTO

# 各难度独立存档文件名
SAVE_MAP = {
    "easy": "save_easy.json",
    "normal": "save_normal.json",
    "hard": "save_hard.json"
}

def save_game(dto: GameBoardDTO):
    """根据dto里的难度，保存到对应存档文件"""
    filename = SAVE_MAP[dto.difficulty]
    save_data = {
        "board": dto.board,
        "score": dto.score,
        "is_game_over": dto.is_game_over,
        "is_win": dto.is_win,
        "is_paused": dto.is_paused,
        "difficulty": dto.difficulty
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(save_data, f, ensure_ascii=False, indent=2)


def load_game(diff_key: str) -> GameBoardDTO | None:
    """读取指定难度的存档，无文件/损坏返回None"""
    filename = SAVE_MAP[diff_key]
    if not os.path.exists(filename):
        return None
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        dto = GameBoardDTO()
        dto.board = data["board"]
        dto.score = data["score"]
        dto.is_game_over = data["is_game_over"]
        dto.is_win = data["is_win"]
        dto.is_paused = data["is_paused"]
        dto.difficulty = data["difficulty"]
        return dto
    except Exception:
        return None


def clear_save(diff_key: str):
    """清空指定难度存档，其他难度不受影响"""
    filename = SAVE_MAP[diff_key]
    if os.path.exists(filename):
        os.remove(filename)
