from typing import Callable, Optional, Union
from random import choice
import tkinter as tk
from tkinter import messagebox as mbox
from tkinter import ttk

from . import t3sc

class UIHost():
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.style = ttk.Style(self.root)
        self.style.theme_use("default")
        self.style.configure("TFrame", background="#eee")
        self.style.configure("TLabel", background="#eee")
        self.style.configure("Danger.TButton", foreground="lightgray")
        self.style.configure("Danger.TButton", background="#e00")
        self.style.map("Danger.TButton",
            foreground=[("active", "white")],
            background=[("active", "red")]
        )
        self.style.map("X.TButton",
            foreground=[("disabled", "white")],
            background=[("disabled", "blue")]
        )
        self.style.map("O.TButton",
            foreground=[("disabled", "black")],
            background=[("disabled", "yellow")]
        )
        self.win_tally = [0, 0]
        self.frame: ttk.Frame = MainMenu(self, self.root)
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.filemenu = tk.Menu(self.menu, tearoff=False)
        self.filemenu.add_command(
            label="Main Menu", underline=0, command=self.main_menu_callback
        )
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", underline=0, command=self.root.destroy)
        self.menu.add_cascade(label="File", menu=self.filemenu, underline=0)
        self.root.minsize(640, 480)
        self.root.geometry("800x600")
        self.root.mainloop()

    def main_menu_callback(self) -> None:
        if isinstance(self.frame, MainMenu):
            return
        elif isinstance(self.frame, ResultsFrame):
            self.frame.destroy()
            self.frame = MainMenu(self, self.root)
            self.win_tally = [0, 0]
            return
        n = mbox.askyesno("End Game?", "Return to Main Menu?")
        if n:
            self.frame.destroy()
            self.frame = MainMenu(self, self.root)
            self.win_tally = [0, 0]

    def start_game_callback(self, cpu: bool, size: Union[int, Callable]) -> Callable[[], None]:
        def callback_func():
            self.frame.destroy()
            self.frame = GameFrame(self, self.root, cpu, size if isinstance(size, int) else size())
        return callback_func

    def game_over_callback(self, winner: int, cpu: bool, size: int):
        def callback_func():
            self.frame.destroy()
            if winner > 0:
                self.win_tally[winner - 1] += 1
            self.frame = ResultsFrame(self, self.root, winner, cpu, size)
        return callback_func

class MainMenu(ttk.Frame):
    def __init__(self, host: UIHost, master: Optional[tk.Tk]=None):
        super().__init__(master)
        self.master = master
        self.host = host
        self.master.title("Tic Tac Toe | Main Menu")
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=4)
        self.rowconfigure(2, weight=3)
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(column=1, row=1, sticky="NEW")
        # self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_label = ttk.Label(
            self.main_frame, text="Tic Tac Toe", font=("Segoe UI", 15), padding=(5,10),
            anchor=tk.CENTER
        )
        self.main_label.grid(column=0, row=0, columnspan=2, sticky="NEW")
        self.size_var = tk.IntVar(self, 3)
        self.size_label = ttk.Label(self.main_frame, text="Board Size:")
        self.size_label.grid(column=0, row=1, sticky="NEW")
        self.size_input = ttk.Spinbox(
            self.main_frame, from_=2, to=11, textvariable=self.size_var
        )
        self.size_input.grid(column=1, row=1, sticky="NEW")
        self.sp_btn = ttk.Button(
            self.main_frame, text="Singleplayer",
            command=self.host.start_game_callback(True, self.size_var.get)
        )
        self.sp_btn.grid(column=0, row=2, columnspan=2, sticky="NEW")
        self.mp_btn = ttk.Button(
            self.main_frame, text="Multiplayer",
            command=self.host.start_game_callback(False, self.size_var.get)
        )
        self.mp_btn.grid(column=0, row=3, columnspan=2, sticky="NEW")
        self.exit_btn = ttk.Button(
            self.main_frame, text="Exit", command=self.master.destroy, style="Danger.TButton"
        )
        self.exit_btn.grid(column=0, row=4, columnspan=2, sticky="NEW")

class GameFrame(ttk.Frame):
    def __init__(self, host: UIHost, master: tk.Tk, cpu: bool, size: int):
        super().__init__(master)
        self.master = master
        self.host = host
        self.cpu = cpu
        self.game = t3sc.TicTacToeScalable(size)
        self.master.title(f"Tic Tac Toe | {'Singleplayer' if cpu else 'Multiplayer'}")
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.turn_label = ttk.Label(self, text="Player 1 (X) turn", anchor=tk.CENTER)
        self.turn_label.grid(row=0, column=0)
        self.tally_label = ttk.Label(
            self, text=f"P1: {self.host.win_tally[0]}/P2: {self.host.win_tally[1]}",
            anchor=tk.CENTER
        )
        self.tally_label.grid(row=0, column=1)
        self.btn_frame = ttk.Frame(self)
        self.btn_frame.grid(row=1, column=0, columnspan=2, sticky="NESW")
        self.btns: list[list[ttk.Button]] = []
        for i in range(self.game.size):
            self.btns.append([])
            for j in range(self.game.size):
                tmp_btn = ttk.Button(self.btn_frame, text="", command=self.btn_callback(i, j))
                tmp_btn.grid(row=i, column=j, sticky="NESW")
                self.btns[i].append(tmp_btn)

        for i in range(self.game.size):
            self.btn_frame.rowconfigure(i, weight=1)
            self.btn_frame.columnconfigure(i, weight=1)

    def btn_callback(self, row: int, col: int) -> Callable[[], None]:
        def callback_func():
            current_turn = self.game.current_turn()
            turn_result = self.game.move(row, col)
            if turn_result is t3sc.TurnResult.SUCCESS:
                btntxt = ["X", "O"][current_turn - 1]
                lbltxt = ["X", "O"][self.game.current_turn() - 1]
                self.turn_label["text"] = f"Player {self.game.current_turn()} ({lbltxt}) turn"
                self.btns[row][col].config(
                    text=btntxt, state=tk.DISABLED, style=btntxt + ".TButton"
                )
                if self.cpu and lbltxt == "O":
                    self.cpu_turn()
            elif turn_result is t3sc.TurnResult.WINNER:
                self.host.game_over_callback(current_turn, self.cpu, self.game.size)()
            elif turn_result is t3sc.TurnResult.DRAW:
                self.host.game_over_callback(0, self.cpu, self.game.size)()
        return callback_func

    def cpu_turn(self):
        valid_pos_list = []
        for i in range(self.game.size):
            for j in range(self.game.size):
                if self.game.board[i][j] == 0:
                    valid_pos_list.append((i, j))
        pos = choice(valid_pos_list)
        self.btn_callback(*pos)()

class ResultsFrame(ttk.Frame):
    def __init__(self, host: UIHost, master: tk.Tk, winner: int, cpu: bool, size: int):
        super().__init__(master)
        self.master = master
        self.host = host
        self.cpu = cpu
        self.game_size = size
        self.winner = winner
        self.wintext = (
            f"Player {winner} ({['X', 'O'][winner - 1]}) won!" if winner > 0 else "Draw..."
        )
        self.master.title("Tic Tac Toe | Results")
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=4)
        self.rowconfigure(2, weight=3)
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(column=1, row=1, sticky="NEW")
        self.main_frame.columnconfigure(0, weight=1)
        self.main_label = ttk.Label(
            self.main_frame, text=self.wintext, font=("Segoe UI", 15), padding=(5,10),
            anchor=tk.CENTER
        )
        self.main_label.grid(column=0, row=0, sticky="NEW")
        self.wins_label = ttk.Label(self.main_frame, text="Total Wins:", anchor=tk.CENTER)
        self.wins_label.grid(column=0, row=1, sticky="NEW")
        self.tally_label = ttk.Label(
            self.main_frame, text=f"P1: {self.host.win_tally[0]}/P2: {self.host.win_tally[1]}",
            anchor=tk.CENTER
        )
        self.tally_label.grid(column=0, row=2, sticky="NEW")
        self.again_btn = ttk.Button(
            self.main_frame, text="Play Again?",
            command=self.host.start_game_callback(self.cpu, self.game_size)
        )
        self.again_btn.grid(column=0, row=3, sticky="NEW")
        self.mainmenu_btn = ttk.Button(
            self.main_frame, text="Main Menu",
            command=self.host.main_menu_callback
        )
        self.mainmenu_btn.grid(column=0, row=4, sticky="NEW")
        self.exit_btn = ttk.Button(
            self.main_frame, text="Exit", command=self.master.destroy, style="Danger.TButton"
        )
        self.exit_btn.grid(column=0, row=5, sticky="NEW")
