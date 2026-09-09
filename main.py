import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from dto.game_board_dto import GameBoardDTO
from service.game_service import Game2048Service
from service.game_exception import InvalidMoveException, BoardFullException
from config.game_config import *


class GameMainWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Python 2048游戏")
        self.root.resizable(False, False)
        self.game_dto = GameBoardDTO()

        # 难度中文映射
        self.diff_map = {
            "简易": "easy",
            "普通": "normal",
            "困难": "hard"
        }
        # 保存上次选择的难度，重开复用
        self.last_selected_diff_key = "normal"

        # 先启动难度选择弹窗
        self.show_diff_select_window()

    def show_diff_select_window(self):
        """启动游戏：难度选择弹窗，选完才创建游戏界面"""
        # 弹窗顶层窗口
        diff_win = tk.Toplevel(self.root)
        diff_win.title("选择游戏难度")
        diff_win.geometry("320x160")
        diff_win.grab_set()  # 模态窗口，必须关闭才能操作主窗口

        tk.Label(diff_win, text="请选择游戏难度", font=("Arial", 16)).pack(pady=15)
        diff_var = tk.StringVar(value="普通")
        comb = ttk.Combobox(diff_win, textvariable=diff_var, values=["简易", "普通", "困难"], width=10, state="readonly")
        comb.pack()
        comb.current(1)

        def confirm_diff():
            selected_cn = diff_var.get()
            self.last_selected_diff_key = self.diff_map[selected_cn]
            self.game_dto.difficulty = self.last_selected_diff_key
            diff_win.destroy()
            # 关闭弹窗后，初始化游戏画布界面
            self.init_game_ui()

        tk.Button(diff_win, text="确认开始游戏", command=confirm_diff, font=("Arial",12)).pack(pady=15)
        # 禁止直接关闭主窗口，必须选难度
        self.root.withdraw()

    def init_game_ui(self):
        """初始化游戏棋盘UI，在选择难度之后执行"""
        self.root.deiconify()
        target = DIFFICULTY_CONFIG[self.last_selected_diff_key]["win_target"]
        self.root.title(f"Python 2048游戏 | 当前难度：{self.last_selected_diff_key} 目标:{target}")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT + 40}")

        # 顶部信息标签
        self.info_label = tk.Label(self.root, text=f"分数：{self.game_dto.score}", font=("Arial", 16))
        self.info_label.pack(pady=3)

        # 按钮容器：重开一局 / 暂停 / 退出
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=2)

        self.btn_restart = tk.Button(btn_frame, text="重开一局", command=self.restart_game, font=("Arial",12))
        self.btn_restart.grid(row=0, column=0, padx=5)

        self.btn_pause = tk.Button(btn_frame, text="暂停", command=self.toggle_pause, font=("Arial",12))
        self.btn_pause.grid(row=0, column=1, padx=5)

        self.btn_exit = tk.Button(btn_frame, text="退出游戏", command=self.exit_game, font=("Arial",12))
        self.btn_exit.grid(row=0, column=2, padx=5)

        self.canvas = tk.Canvas(self.root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT - 80, bg="#bbada0")
        self.canvas.pack()

        # 绑定方向按键
        self.root.bind("<Left>", self.on_key_press)
        self.root.bind("<Right>", self.on_key_press)
        self.root.bind("<Up>", self.on_key_press)
        self.root.bind("<Down>", self.on_key_press)

        # 初始化游戏数据
        Game2048Service.init_new_game(self.game_dto)
        self.draw_board()

    def draw_board(self):
        """绘制棋盘"""
        self.canvas.delete("all")
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                val = self.game_dto.board[row][col]
                x1 = col * CELL_SIZE + (col + 1) * CELL_PADDING
                y1 = row * CELL_SIZE + (row + 1) * CELL_PADDING
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                bg_color = COLOR_MAP.get(val, DEFAULT_COLOR)
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=bg_color, outline="#bbada0", width=3)
                if val > 0:
                    self.canvas.create_text(
                        (x1 + x2) / 2,
                        (y1 + y2) / 2,
                        text=str(val),
                        font=("Arial", 24, "bold"),
                        fill="#776e65"
                    )
        target = DIFFICULTY_CONFIG[self.game_dto.difficulty]["win_target"]
        self.info_label.config(text=f"分数：{self.game_dto.score}  目标：{target}")

        # 暂停遮罩
        if self.game_dto.is_paused:
            self.canvas.create_rectangle(0,0,WINDOW_WIDTH, WINDOW_HEIGHT, fill="#000000", stipple="gray50")
            self.canvas.create_text(WINDOW_WIDTH//2, (WINDOW_HEIGHT-80)//2, text="游戏已暂停", font=("Arial",30,"bold"), fill="white")

        # 胜利/失败弹窗
        if self.game_dto.is_win:
            target_val = DIFFICULTY_CONFIG[self.game_dto.difficulty]["win_target"]
            messagebox.showinfo("恭喜！", f"你合成{target_val}，游戏胜利！")
        if self.game_dto.is_game_over:
            messagebox.showwarning("游戏结束", "棋盘已满，没有可合并方块，游戏结束！")

    def toggle_pause(self):
        """暂停/继续"""
        self.game_dto.is_paused = not self.game_dto.is_paused
        if self.game_dto.is_paused:
            self.btn_pause.config(text="继续游戏")
        else:
            self.btn_pause.config(text="暂停")
        self.draw_board()

    def restart_game(self):
        """重开一局：复用上次选择的难度，不再弹出难度选择"""
        answer = messagebox.askyesno("确认重开", "确定放弃当前对局，重新开始吗？")
        if answer:
            # 保持难度不变，只重置棋盘、分数、状态
            Game2048Service.init_new_game(self.game_dto)
            self.btn_pause.config(text="暂停")
            self.draw_board()

    def exit_game(self):
        """退出游戏"""
        answer = messagebox.askyesno("退出确认", "确定要退出游戏吗？")
        if answer:
            self.root.destroy()

    def on_key_press(self, event):
        """键盘事件"""
        try:
            key_map = {
                "Left": "left",
                "Right": "right",
                "Up": "up",
                "Down": "down"
            }
            direction = key_map.get(event.keysym)
            if not direction:
                return

            if self.game_dto.is_paused or self.game_dto.is_game_over or self.game_dto.is_win:
                return

            moved = Game2048Service.move(self.game_dto, direction)
            if moved:
                Game2048Service.add_random_number(self.game_dto)
            Game2048Service.check_game_status(self.game_dto)
            self.draw_board()

        except InvalidMoveException as e:
            print(f"移动异常：{e}")
        except BoardFullException as e:
            print(f"生成方块异常：{e}")
        except Exception as e:
            messagebox.showerror("运行异常", f"发生未知错误：{str(e)}")


if __name__ == "__main__":
    try:
        main_root = tk.Tk()
        app = GameMainWindow(main_root)
        main_root.mainloop()
    except Exception as global_err:
        print(f"程序启动异常 {global_err}")
