Readme for SAPER

Описание 

обычная игра сапер с 3 режимами и таймером 
Как запустить
Для запуска игры убедитесь, что у вас установлен Python и Tkinter.
 Запустите файл игры командой:
 python saper.py

 Описание классов и методов
class CustomButton(tk.Button):
Этот класс представляет собой кастомную кнопку на игровом поле, являющуюся клеткой "Сапёра".

__init__: Инициализирует кнопку с нужными параметрами и обработчиками событий.
on_left_click: Обрабатывает нажатие левой кнопки мыши (открытие клетки).
on_right_click: Обрабатывает нажатие правой кнопки мыши (установка/снятие флага).
toggle_flag: Устанавливает или снимает флаг с клетки.
reveal: Открывает клетку и показывает, сколько мин находится рядом, или заканчивает игру, если открыта мина.
update_display: Обновляет отображение кнопки.
set_mine: Отмечает кнопку как содержащую мину.
count_mines_around: Считает количество мин вокруг данной клетки.
class Sapper():
Основной класс игры, управляющий игровым процессом и интерфейсом.

__init__: Инициализация основного игрового окна и всех виджетов.
update_window_size: Обновляет размеры окна в зависимости от размеров игрового поля.
create_buttons: Создает кнопки игрового поля.
menu: Создает меню для выбора уровня сложности.
distribute_mines: Распределяет мины по игровому полю.
create_widgets: Располагает виджеты на игровом поле.
set_difficulty: Устанавливает уровень сложности игры.
start: Запускает основной игровой цикл.
start_game: Начинает новую игру.
update_timer: Обновляет таймер игры.
check_win: Проверяет, выиграл ли игрок.
end_game: Обрабатывает окончание игры и показывает результат.
restart_game: Перезапускает игру.
Зависимости
Python (версия 3.6 или выше)
Tkinter
Авторы
[Dnec4]
