import tkinter as tk
from tkinter import messagebox
import random


class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Крестики-нолики")
        self.window.resizable(False, False)

        #Настройка стилей
        self.bg_color = "#f0f0f0"
        self.button_color = "#ffffff"
        self.x_color = "#ff4444"
        self.o_color = "#4444ff"
        self.win_color = "#ffff99"
        self.font = ("Arial", 20, "bold")

        self.window.configure(bg=self.bg_color)

        #Переменные игры
        self.current_player = "X"
        self.board = [""] * 9
        self.game_over = False
        self.winning_combo = None

        #Создание интерфейса
        self.create_widgets()

        #Запуск игры
        self.window.mainloop()

    def create_widgets(self):
        # Заголовок
        self.title_label = tk.Label(
            self.window,
            text="Крестики-нолики",
            font=("Arial", 24, "bold"),
            bg=self.bg_color,
            fg="#333333"
        )
        self.title_label.grid(row=0, column=0, columnspan=3, pady=20)

        #Отображение текущего игрока
        self.status_label = tk.Label(
            self.window,
            text=f"Сейчас ходит: {self.current_player}",
            font=("Arial", 14),
            bg=self.bg_color,
            fg="#666666"
        )
        self.status_label.grid(row=1, column=0, columnspan=3, pady=10)

        #Игровое поле
        self.buttons = []
        for i in range(9):
            row, col = divmod(i, 3)
            button = tk.Button(
                self.window,
                text="",
                font=self.font,
                width=6,
                height=3,
                bg=self.button_color,
                relief="raised",
                bd=3,
                command=lambda idx=i: self.player_move(idx)
            )
            button.grid(row=row + 2, column=col, padx=2, pady=2)
            self.buttons.append(button)

        #Кнопка новой игры
        self.new_game_button = tk.Button(
            self.window,
            text="Новая игра",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            relief="raised",
            bd=2,
            command=self.reset_game
        )
        self.new_game_button.grid(row=5, column=0, columnspan=3, pady=20, ipadx=20)

    def player_move(self, position):
        if self.game_over or self.board[position] != "":
            return

        #Ход игрока
        self.make_move(position, "X")

        if not self.game_over:
            #Ход компьютера
            self.window.after(500, self.computer_move)

    def computer_move(self):
        if self.game_over:
            return

        move = self.get_best_move()
        if move is not None:
            self.make_move(move, "O")

    def make_move(self, position, player):
        self.board[position] = player
        color = self.x_color if player == "X" else self.o_color
        self.buttons[position].config(text=player, fg=color, state="disabled")

        #Проверяем победителя
        winner, winning_combo = self.check_winner(player)

        if winner:
            self.game_over = True
            self.winning_combo = winning_combo
            self.highlight_winning_combo()

            winner_text = "Игрок" if player == "X" else "Компьютер"
            messagebox.showinfo("Игра окончена", f"{winner_text} победил!")
            self.status_label.config(text=f"Победил: {player}")
        elif "" not in self.board:
            self.game_over = True
            messagebox.showinfo("Игра окончена", "Ничья!")
            self.status_label.config(text="Ничья!")
        else:
            self.current_player = "O" if player == "X" else "X"
            self.status_label.config(text=f"Сейчас ходит: {self.current_player}")

    def check_winner(self, player):
        #проверяет, есть ли победитель. возвращает (is_winner, winning_combo)
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Горизонтальные
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Вертикальные
            [0, 4, 8], [2, 4, 6]  # Диагональные
        ]

        for combo in winning_combinations:
            if all(self.board[i] == player for i in combo):
                return True, combo
        return False, None

    def highlight_winning_combo(self):
        if self.winning_combo:
            for position in self.winning_combo:
                self.buttons[position].config(bg=self.win_color)

    def get_best_move(self):
        #1. ПРИОРИТЕТ: Выиграть сейчас
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"
                winner, _ = self.check_winner("O")
                self.board[i] = ""
                if winner:
                    return i

        #2. ПРИОРИТЕТ: Блокировать игрока
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "X"
                winner, _ = self.check_winner("X")
                self.board[i] = ""
                if winner:
                    return i

        #3. ПРИОРИТЕТ: Занять центр
        if self.board[4] == "":
            return 4

        #4. ПРИОРИТЕТ: Занять углы
        corners = [0, 2, 6, 8]
        available_corners = [c for c in corners if self.board[c] == ""]
        if available_corners:
            return random.choice(available_corners)

        #5. Любая доступная клетка
        available_moves = [i for i in range(9) if self.board[i] == ""]
        if available_moves:
            return random.choice(available_moves)

        return None

    def reset_game(self):
        #Сброс игры
        self.current_player = "X"
        self.board = [""] * 9
        self.game_over = False
        self.winning_combo = None

        #Сброс кнопок к исходному состоянию
        for button in self.buttons:
            button.config(
                text="",
                state="normal",
                bg=self.button_color,
                fg="black"
            )

        #Обновление статуса
        self.status_label.config(text=f"Сейчас ходит: {self.current_player}")


if __name__ == "__main__":
    game = TicTacToe()