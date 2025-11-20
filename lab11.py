import tkinter as tk
import random
import time
from enum import Enum

#константы игры
CELL_SIZE = 30
GRID_WIDTH = 19
GRID_HEIGHT = 21
GAME_SPEED = 150
POWER_DURATION = 10


#направления движения
class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    NONE = (0, 0)


#Типы клеток
class CellType(Enum):
    EMPTY = 0
    WALL = 1
    DOT = 2
    POWER_PELLET = 3


#Класс игрового поля
class GameBoard:
    def __init__(self):
        self.grid = self.create_initial_grid()
        self.dots_count = self.count_dots()

    def create_initial_grid(self):
        grid = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1],
            [1, 3, 1, 0, 1, 2, 1, 0, 2, 1, 2, 0, 1, 2, 1, 0, 1, 3, 1],
            [1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1],
            [1, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 1],
            [1, 1, 1, 1, 1, 2, 1, 1, 1, 0, 1, 1, 1, 2, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 2, 1, 0, 1, 1, 1, 0, 1, 2, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 2, 0, 0, 1, 0, 1, 0, 0, 2, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 2, 1, 0, 1, 1, 1, 0, 1, 2, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 2, 1, 0, 1, 1, 1, 0, 1, 2, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1],
            [1, 3, 2, 2, 1, 2, 2, 2, 2, 0, 2, 2, 2, 2, 1, 2, 2, 3, 1],
            [1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        return grid

    def count_dots(self):
        count = 0
        for row in self.grid:
            for cell in row:
                if cell == 2 or cell == 3:
                    count += 1
        return count

    def get_cell_type(self, x, y):
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            return CellType(self.grid[y][x])
        return CellType.WALL

    def eat_dot(self, x, y):
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            if self.grid[y][x] == 2:
                self.grid[y][x] = 0
                self.dots_count -= 1
                return 10
            elif self.grid[y][x] == 3:
                self.grid[y][x] = 0
                self.dots_count -= 1
                return 50
        return 0

    def is_completed(self):
        return self.dots_count == 0


#класс для игровых персонажей
class Character:
    def __init__(self, x, y, color, game_board):
        self.x = x
        self.y = y
        self.color = color
        self.direction = Direction.NONE
        self.next_direction = Direction.NONE
        self.game_board = game_board
        self.speed = 1

    def move(self):
        if self.can_move(self.next_direction):
            self.direction = self.next_direction

        if self.can_move(self.direction):
            dx, dy = self.direction.value
            self.x += dx
            self.y += dy
            return True
        return False

    def can_move(self, direction):
        if direction == Direction.NONE:
            return False

        dx, dy = direction.value
        new_x = self.x + dx
        new_y = self.y + dy

        if new_x < 0 or new_x >= GRID_WIDTH or new_y < 0 or new_y >= GRID_HEIGHT:
            return False

        return self.game_board.get_cell_type(new_x, new_y) != CellType.WALL

    def set_direction(self, direction):
        self.next_direction = direction


#Класс для пакмана
class PacMan(Character):
    def __init__(self, x, y, game_board):
        super().__init__(x, y, "yellow", game_board)
        self.score = 0
        self.lives = 3
        self.power_mode = False
        self.power_start_time = 0
        self.power_remaining = 0

    def move(self):
        if super().move():
            points = self.game_board.eat_dot(self.x, self.y)
            self.score += points

            if points == 50:
                self.activate_power_mode()

            if self.power_mode:
                current_time = time.time()
                self.power_remaining = max(0, POWER_DURATION - (current_time - self.power_start_time))
                if self.power_remaining <= 0:
                    self.power_mode = False

            return True
        return False

    def activate_power_mode(self):
        self.power_mode = True
        self.power_start_time = time.time()
        self.power_remaining = POWER_DURATION

    def lose_life(self):
        self.lives -= 1
        return self.lives > 0


#Класс для призраков
class Ghost(Character):
    def __init__(self, x, y, color, game_board, pacman):
        super().__init__(x, y, color, game_board)
        self.pacman = pacman
        self.scatter_target = (0, 0)
        self.mode = "chase"
        self.mode_timer = 0
        self.frightened_timer = 0
        self.original_color = color

    def move(self):
        self.update_mode()

        if self.mode == "frightened":
            self.direction = self.random_direction()
        elif self.mode == "scatter":
            self.direction = self.find_direction_to_target(self.scatter_target)
        else:
            self.direction = self.find_direction_to_target((self.pacman.x, self.pacman.y))

        return super().move()

    def update_mode(self):
        if self.mode == "frightened":
            self.frightened_timer -= 1
            if self.frightened_timer <= 0:
                self.mode = "chase"
                self.color = self.original_color

        self.mode_timer -= 1
        if self.mode_timer <= 0:
            if self.mode == "chase":
                self.mode = "scatter"
                self.mode_timer = 70
            else:
                self.mode = "chase"
                self.mode_timer = 200

    def random_direction(self):
        directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
        random.shuffle(directions)

        for direction in directions:
            if self.can_move(direction):
                return direction

        return Direction.NONE

    def find_direction_to_target(self, target):
        tx, ty = target

        dx = tx - self.x
        dy = ty - self.y

        if abs(dx) > abs(dy):
            if dx > 0 and self.can_move(Direction.RIGHT):
                return Direction.RIGHT
            elif dx < 0 and self.can_move(Direction.LEFT):
                return Direction.LEFT
            elif dy > 0 and self.can_move(Direction.DOWN):
                return Direction.DOWN
            elif dy < 0 and self.can_move(Direction.UP):
                return Direction.UP
        else:
            if dy > 0 and self.can_move(Direction.DOWN):
                return Direction.DOWN
            elif dy < 0 and self.can_move(Direction.UP):
                return Direction.UP
            elif dx > 0 and self.can_move(Direction.RIGHT):
                return Direction.RIGHT
            elif dx < 0 and self.can_move(Direction.LEFT):
                return Direction.LEFT

        return self.random_direction()

    def set_frightened(self):
        self.mode = "frightened"
        self.frightened_timer = POWER_DURATION * 20
        self.color = "white"


#Класс игры
class PacManGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pac-Man")
        self.root.resizable(False, False)

        #холст для отрисовки
        self.canvas = tk.Canvas(
            self.root,
            width=GRID_WIDTH * CELL_SIZE,
            height=GRID_HEIGHT * CELL_SIZE,
            bg="black"
        )
        self.canvas.pack()

        #Устанавливаем фокус на холст и привязываем все клавиши
        self.canvas.focus_set()
        self.canvas.bind("<KeyPress>", self.on_key_press)

        #Инициализация игры
        self.reset_game()

        #Запускаем игровой цикл
        self.game_loop()

    def reset_game(self):
        #сброс игры
        self.game_board = GameBoard()
        self.pacman = PacMan(9, 15, self.game_board)

        #создаем призраков
        self.ghosts = [
            Ghost(9, 9, "red", self.game_board, self.pacman),
            Ghost(8, 9, "pink", self.game_board, self.pacman),
            Ghost(10, 9, "cyan", self.game_board, self.pacman),
            Ghost(9, 8, "orange", self.game_board, self.pacman)
        ]

        self.ghosts[0].scatter_target = (GRID_WIDTH - 1, 0)
        self.ghosts[1].scatter_target = (0, 0)
        self.ghosts[2].scatter_target = (GRID_WIDTH - 1, GRID_HEIGHT - 1)
        self.ghosts[3].scatter_target = (0, GRID_HEIGHT - 1)

        self.game_over = False
        self.game_won = False


        self.canvas.focus_set()

    def on_key_press(self, event):
        #обработка клавиш
        key = event.keysym.lower()

        #движение пакмана
        if key == "up":
            self.pacman.set_direction(Direction.UP)
        elif key == "down":
            self.pacman.set_direction(Direction.DOWN)
        elif key == "left":
            self.pacman.set_direction(Direction.LEFT)
        elif key == "right":
            self.pacman.set_direction(Direction.RIGHT)

        #рестарт
        elif key == "r":
            if self.game_over or self.game_won:
                self.reset_game()
                print("Game restarted!")

    def game_loop(self):
        if not self.game_over and not self.game_won:
            #двигаем Пакмана
            self.pacman.move()

            #двигаем призраков
            for ghost in self.ghosts:
                ghost.move()

                # Проверяем столкновение с пакманом
                if ghost.x == self.pacman.x and ghost.y == self.pacman.y:
                    if self.pacman.power_mode:
                        #Пакман съедает призрака
                        ghost.x, ghost.y = 9, 9
                        ghost.mode = "chase"
                        ghost.color = ghost.original_color
                        self.pacman.score += 200
                    else:
                        #Призрак съедает пакмана
                        if not self.pacman.lose_life():
                            self.game_over = True
                            print("Game Over! Press R to restart")
                        else:
                            #Возвращаем на начальные позиции
                            self.pacman.x, self.pacman.y = 9, 15
                            self.pacman.direction = Direction.NONE
                            self.pacman.next_direction = Direction.NONE

                            positions = [(9, 9), (8, 9), (10, 9), (9, 8)]
                            for i, ghost in enumerate(self.ghosts):
                                ghost.x, ghost.y = positions[i]
                                ghost.direction = Direction.NONE
                                ghost.mode = "chase"
                                ghost.color = ghost.original_color

            #режим испуга у призраков при съедании энерджайзера
            if self.pacman.power_mode and self.pacman.power_remaining == POWER_DURATION:
                for ghost in self.ghosts:
                    ghost.set_frightened()


            if self.game_board.is_completed():
                self.game_won = True
                print("You Win! Press R to restart")

            #отрисовка игры
            self.draw()

        self.root.after(GAME_SPEED, self.game_loop)

    def draw(self):
        self.canvas.delete("all")

        #рисуем игровое поле
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                cell_type = self.game_board.get_cell_type(x, y)
                x1 = x * CELL_SIZE
                y1 = y * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                if cell_type == CellType.WALL:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill="blue", outline="darkblue"
                    )
                elif cell_type == CellType.DOT:
                    self.canvas.create_oval(
                        x1 + CELL_SIZE // 2 - 2, y1 + CELL_SIZE // 2 - 2,
                        x1 + CELL_SIZE // 2 + 2, y1 + CELL_SIZE // 2 + 2,
                        fill="white", outline=""
                    )
                elif cell_type == CellType.POWER_PELLET:
                    self.canvas.create_oval(
                        x1 + CELL_SIZE // 2 - 5, y1 + CELL_SIZE // 2 - 5,
                        x1 + CELL_SIZE // 2 + 5, y1 + CELL_SIZE // 2 + 5,
                        fill="white", outline=""
                    )

        #рисуем пакмана
        pacman_x = self.pacman.x * CELL_SIZE + CELL_SIZE // 2
        pacman_y = self.pacman.y * CELL_SIZE + CELL_SIZE // 2

        self.canvas.create_oval(
            pacman_x - 10, pacman_y - 10,
            pacman_x + 10, pacman_y + 10,
            fill=self.pacman.color, outline=""
        )

        if self.pacman.direction != Direction.NONE:
            dx, dy = self.pacman.direction.value
            self.canvas.create_polygon(
                pacman_x, pacman_y,
                pacman_x + dx * 10, pacman_y + dy * 10,
                pacman_x + dy * 7, pacman_y - dx * 7,
                fill="black", outline=""
            )

        #рисуем призраков
        for ghost in self.ghosts:
            ghost_x = ghost.x * CELL_SIZE + CELL_SIZE // 2
            ghost_y = ghost.y * CELL_SIZE + CELL_SIZE // 2

            if ghost.mode == "frightened":
                current_time = time.time()
                if self.pacman.power_remaining <= 2.0:
                    blink = int(current_time * 5) % 2
                    color = "white" if blink == 0 else "blue"
                else:
                    color = "white"
            else:
                color = ghost.color

            #тело призрака
            self.canvas.create_rectangle(
                ghost_x - 10, ghost_y - 10,
                ghost_x + 10, ghost_y + 5,
                fill=color, outline=""
            )

            #ноги призрака
            self.canvas.create_polygon(
                ghost_x - 10, ghost_y + 5,
                ghost_x - 7, ghost_y + 10,
                ghost_x - 3, ghost_y + 5,
                ghost_x, ghost_y + 10,
                ghost_x + 3, ghost_y + 5,
                ghost_x + 7, ghost_y + 10,
                ghost_x + 10, ghost_y + 5,
                fill=color, outline=""
            )

            #глаза призрака
            if ghost.mode != "frightened":
                self.canvas.create_oval(
                    ghost_x - 5, ghost_y - 5,
                    ghost_x - 1, ghost_y - 1,
                    fill="white", outline=""
                )
                self.canvas.create_oval(
                    ghost_x - 4, ghost_y - 4,
                    ghost_x - 2, ghost_y - 2,
                    fill="black", outline=""
                )

                self.canvas.create_oval(
                    ghost_x + 1, ghost_y - 5,
                    ghost_x + 5, ghost_y - 1,
                    fill="white", outline=""
                )
                self.canvas.create_oval(
                    ghost_x + 2, ghost_y - 4,
                    ghost_x + 4, ghost_y - 2,
                    fill="black", outline=""
                )
            else:
                #глаза в режиме испуга
                self.canvas.create_oval(
                    ghost_x - 5, ghost_y - 5,
                    ghost_x - 1, ghost_y - 1,
                    fill="blue", outline=""
                )
                self.canvas.create_oval(
                    ghost_x + 1, ghost_y - 5,
                    ghost_x + 5, ghost_y - 1,
                    fill="blue", outline=""
                )

        #счетчик очков и жизней
        self.canvas.create_text(
            50, 10,
            text=f"Score: {self.pacman.score}",
            fill="white",
            anchor="nw",
            font=("Arial", 12)
        )

        self.canvas.create_text(
            GRID_WIDTH * CELL_SIZE - 50, 10,
            text=f"Lives: {self.pacman.lives}",
            fill="white",
            anchor="ne",
            font=("Arial", 12)
        )

        #таймер энерджайзера
        if self.pacman.power_mode:
            power_text = f"Power: {self.pacman.power_remaining:.1f}s"
            self.canvas.create_text(
                GRID_WIDTH * CELL_SIZE // 2, 10,
                text=power_text,
                fill="cyan",
                font=("Arial", 12)
            )

        #сообщения о конце игры
        if self.game_over:
            self.canvas.create_text(
                GRID_WIDTH * CELL_SIZE // 2,
                GRID_HEIGHT * CELL_SIZE // 2,
                text="GAME OVER\nPress R to restart",
                fill="red",
                font=("Arial", 20, "bold"),
                justify="center"
            )

        if self.game_won:
            self.canvas.create_text(
                GRID_WIDTH * CELL_SIZE // 2,
                GRID_HEIGHT * CELL_SIZE // 2,
                text="YOU WIN!\nPress R to restart",
                fill="green",
                font=("Arial", 20, "bold"),
                justify="center"
            )

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    game = PacManGame()
    game.run()