import json
import os
from dto.game_board_dto import GameBoardDTO

SAVE_FILE = "game_save.json"

def save_game(dto: GameBoardDTO):
    """保存游戏DTO到json文件"""
    save_data = {
        "board": dto.board,
        "score": dto.score,
        "is_game_over": dto.is_game_over,
        "is_win": dto.is_win,
        "is_paused": dto.is_paused,
        "difficulty": dto.difficulty
    }
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(save_data, f, ensure_ascii=False, indent=2)


def load_game() -> GameBoardDTO | None:
    """读取存档，无存档返回None"""
    if not os.path.exists(SAVE_FILE):
        return None
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
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
        # 存档损坏直接丢弃
        return None


def clear_save():
    """清空存档（重开一局调用）"""
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
