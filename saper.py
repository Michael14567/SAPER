import tkinter as tk
from tkinter import messagebox
import random
import time

class CustomButton(tk.Button):

    def __init__(self, master, x, y, rows, columns, game_instance, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.x = x
        self.y = y
        self.rows = rows  # Add rows
        self.columns = columns  # Add columns
        self.game = game_instance  # Add game instance
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False  # Флаг для отслеживания, установлен ли флаг
        
        # Добавление обработчиков событий для кликов
        self.bind("<Button-1>", self.on_left_click)  # Левый клик
        self.bind("<Button-3>", self.on_right_click)  # Правый клик

    def on_left_click(self, event):
        if not self.is_flagged:
            self.reveal()

    def on_right_click(self, event):
        if not self.is_revealed:
            self.toggle_flag()

    def toggle_flag(self):
        self.is_flagged = not self.is_flagged
        self.update_display()

    def reveal(self):
        if not self.is_flagged and not self.is_revealed:
            self.is_revealed = True
            if self.is_mine:
                self.config(text="*", background="red")
            else:
                mine_count = self.count_mines_around()
                self.config(text=str(mine_count), background="green")

    def update_display(self):
        if self.is_flagged:
            self.config(text="F", background="orange")
        else:
            self.config(text="", background="SystemButtonFace")

    def set_mine(self):
        self.is_mine = True

    def count_mines_around(self):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:  # Skip the button itself
                    continue
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < self.rows and 0 <= ny < self.columns:
                    if self.game.buttons[nx][ny].is_mine:
                        count += 1
        return count

    def reveal(self):
        if self.is_mine:
            self.game.end_game("Проигрыш")
        # Если клетка уже открыта или помечена флагом, ничего не делаем
        if self.is_revealed or self.is_flagged:
            return

        self.is_revealed = True
        mine_count = self.count_mines_around()

        if self.is_mine:
            self.config(text="*", background="red")
        elif mine_count > 0:
            self.config(text=str(mine_count), background="green")
        else:
            # Если вокруг нет мин, открываем соседние клетки
            self.config(background="green")
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = self.x + dx, self.y + dy
                    if 0 <= nx < self.rows and 0 <= ny < self.columns:
                        # Рекурсивно открываем соседние клетки
                        self.game.buttons[nx][ny].reveal()


class sapper():
    # Создание основного окна
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Сапер")
        self.rows = 9
        self.columns = 9
        self.buttons = []

        self.button_size = 50  # Размер кнопки в пикселях адапитровать под монитор 

        width = self.columns * self.button_size
        self.additional_space = 60
        height = self.rows * self.button_size + self.additional_space  # Дополнительное место для таймера и т.д.
        self.root.geometry(f"{width}x{height}")
        self.create_buttons()
        self.create_widgets()
        self.menu()

        self.start_time = None
        
        self.set_difficulty("новичок") 

    def update_window_size(self):
        # Предполагаем, что у вас есть self.button_size и self.additional_space
        width = self.columns * self.button_size
        height = self.rows * self.button_size + self.additional_space
        self.root.geometry(f"{width}x{height}")

        self.timer_label = tk.Label(self.root, text="00:00", fg="red", font=("Helvetica", 16))
        self.timer_label.grid(row=self.rows, column=0, columnspan=self.columns, sticky="ew")


    def create_buttons(self):
        # Удаление старых кнопок, если они есть
        for row in self.buttons:
            for button in row:
                button.destroy()

        # Создание нового списка кнопок
        self.buttons = []
        for i in range(self.rows):
            temp = []
            for j in range(self.columns):
                # Pass the current instance of sapper to each CustomButton
                btn = CustomButton(self.root, i, j, self.rows, self.columns, self, width=3, font='Arial 15 bold')
                temp.append(btn)
            self.buttons.append(temp)
        self.create_widgets()  # Расположение новых кнопок на поле
    
    def menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        difficulty_menu = tk.Menu(menu)
        menu.add_cascade(label="Сложность", menu=difficulty_menu)
        difficulty_menu.add_command(label="Новичок", command=lambda: self.set_difficulty("новичок"))
        difficulty_menu.add_command(label="Любитель", command=lambda: self.set_difficulty("любитель"))
        difficulty_menu.add_command(label="Профессионал", command=lambda: self.set_difficulty("профессионал"))
        difficulty_menu.add_command(label="Особый", command=lambda: self.set_difficulty("особый"))

    
    def distribute_mines(self, mine_count):
        all_positions = [(i, j) for i in range(self.rows) for j in range(self.columns)]
        mine_positions = random.sample(all_positions, mine_count)

        for x, y in mine_positions:
            self.buttons[x][y].set_mine()
    
    def create_widgets(self):
        for i in range(self.rows):
            for j in range(self.columns):
                btn = self.buttons[i][j]
                btn.grid(row=i, column=j)

    # Добавление меню для выбора сложности
    def set_difficulty(self, level):
        # Определение параметров для разных уровней сложности
        if level == "новичок":
            self.rows, self.columns, self.mine_count = 9, 9, 10
        elif level == "любитель":
            self.rows, self.columns, self.mine_count = 16, 16, 40
        elif level == "профессионал":
            self.rows, self.columns, self.mine_count = 16, 30, 99
        elif level == "особый":
            # Можно добавить логику для пользовательского ввода или предопределенные значения
            self.rows, self.columns, self.mine_count = 20, 20, 60  # Пример значений
        else:
            print("Неизвестный уровень сложности!")
            return
        
        # Пересоздаем игровое поле и кнопки
        self.update_window_size() 
        self.create_buttons()
        self.create_widgets()
        self.start_game(self.mine_count)

    def start(self):
        self.root.mainloop()

    def start_game(self, mine_count):
        self.start_time = time.time()
         # Убедитесь, что игровое поле и кнопки уже созданы
        self.distribute_mines(mine_count)
        for row in self.buttons:
            for button in row:
                mines_count = button.count_mines_around()

        self.update_timer()

    def update_timer(self):
        if self.start_time:
            elapsed_time = int(time.time() - self.start_time)
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
            self.timer_label.config(text=f"{minutes:02}:{seconds:02}")
            self.root.after(1000, self.update_timer)

    def print_btn(self):
        for row_btn in self.buttons:
            print(row_btn)

    def check_win(self):
        for row in self.buttons:
            for button in row:
                if not button.is_mine and not button.is_revealed:
                    return  # Еще есть неоткрытые не-мины
        self.end_game("Победа")

    def end_game(self, result):
        # Остановка таймера
        if self.start_time:
            elapsed_time = int(time.time() - self.start_time)
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
            time_str = f"Время игры: {minutes:02}:{seconds:02}"
        else:
            time_str = "Время не отслеживалось"

        # Создание всплывающего окна с результатом
        result_window = tk.Toplevel(self.root)
        result_window.title("Игра окончена!")

        result_label = tk.Label(result_window, text=f"{result}!\n{time_str}", font=("Helvetica", 16))
        result_label.pack(side="top", fill="x", pady=10)

        # Кнопка начать заново
        restart_button = tk.Button(result_window, text="Начать заново", command=self.restart_game)
        restart_button.pack(pady=20)

    def restart_game(self):
        # Очистка текущего игрового поля
        for row in self.buttons:
            for button in row:
                button.destroy()
        
        # Пересоздание игрового поля и кнопок
        self.create_buttons()
        self.create_widgets()
        
        # Перезапуск таймера
        self.start_time = time.time()
        self.update_timer()

        # Перезапуск игры с текущими настройками сложности
        self.start_game(self.mine_count)

game=sapper()
game.start()