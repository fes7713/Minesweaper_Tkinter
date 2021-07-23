import random
import tkinter as tk
import colors as c
from tkinter import ttk, IntVar


def generateGrid_with_num(row, col, num):
    grid = [[0]*cols for _ in range(rows)]
    for i in range(row):
        for j in range(col):
            grid[i][j] = num
    return grid


# Keita
def generateGrid(row, col, no_bomb, y_cursor, x_cursor):
    grid = [[0]*cols for _ in range(rows)]
    for i in range(no_bomb):
        y = random.randrange(row)
        x = random.randrange(col)
        while grid[y][x] == 9 or (-1 <= x - x_cursor <= 1  and -1 <= y - y_cursor <= 1):
            y = random.randrange(row)
            x = random.randrange(col)
        grid[y][x] = 9
    for i in range(row):
        for j in range(col):
            if grid[i][j] != 9:
             grid[i][j] = count_Bomb(grid, i, j)
    return grid


def open3x3(grid_user, grid_answer, cursor_y, cursor_x):
    for i in range(-1, 2):
        if not(0 <= i+cursor_y < rows):
            continue
        for j in range(-1, 2) :
            if not(0 <= j+cursor_x < cols):
                continue
            if grid_user[i+cursor_y][j+cursor_x] != -1:
                continue
            grid_user[i+cursor_y][j+cursor_x] = grid_answer[i+cursor_y][j+cursor_x]
            if grid_user[i+cursor_y][j+cursor_x] == 0:
                open3x3(grid_user, grid_answer, i+cursor_y, j+cursor_x)

def count_Bomb(grid, y, x):
    count = 0
    for i in range(-1, 2):
        if not(0 <= i+y < len(grid)):
            continue
        for j in range(-1, 2):
            if not(0 <= j+x < len(grid[0])):
                continue
            if grid[y+i][x+j] == 9:
               count += 1
    return count


#######################   main
def update_GUI_Cursor():
    # print(x_cursor)
    # print(y_cursor)
    for i in range(-1, 2):
        if not (0 <= i + y_cursor < rows):
            continue
        for j in range(-1, 2):
            if not (0 <= j + x_cursor < cols):
                continue
            cursor_frames[i + y_cursor][j + x_cursor].configure(
                bg=c.BG_COLOR
            )
    cursor_frames[y_cursor][x_cursor].configure(
        bg=c.CURSOR_COLOR
    )
    # for i in range(rows):
    #     for j in range(cols):
    #         cursor_frames[i][j].update_idletasks()
    # frame.update_idletasks()

def update_GUI():
    for i in range(rows):
        for j in range(cols):
            grid_value = grid_user[i][j]
            if grid_user[y_cursor][x_cursor] == -1:
                cells[y_cursor][x_cursor]["frame"].configure(bg=c.BG_COLORS[-1])
                cells[y_cursor][x_cursor]["number"].configure(text="", bg=c.BG_COLORS[-1], fg=c.NUMBER_COLORS[-1])
            if grid_value == -1:
                continue
            cell_value = cells[i][j]
            cell_value["frame"].configure(bg=c.BG_COLORS[grid_value])
            cell_value["number"].configure(bg=c.BG_COLORS[grid_value],
                                            fg=c.NUMBER_COLORS[grid_value])
            if 0 < grid_value <= 8:
                cell_value["number"].configure(text=str(grid_value))
            elif grid_user[i][j] == 10:
                cell_value["number"].configure(text="F")
            elif grid_user[i][j] == 9:
                cell_value["number"].configure(text="B")
            else:
                cell_value["number"].configure(text="")
    flag = False
    open = False

def clear_GUI():
    for i in range(rows):
        for j in range(cols):
            cell_value = cells[i][j]
            cell_value["frame"].configure(bg=c.BG_COLORS[-1])
            cell_value["number"].configure(bg=c.BG_COLORS[-1],
                                           fg=c.NUMBER_COLORS[-1],
                                           text="")
def game_over():
    # global game_over_frame
    for i in range(rows):
        for j in range(cols):
            if grid_user[i][j] == 9:
                game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
                game_over_label.configure(
                    text="Game Over!",
                    bg=c.LOSER_BG,
                )
                game_over_label.pack()


def game_win():
    # global game_over_frame
    cnt = 0
    for i in range(rows):
        for j in range(cols):
            if grid_user[i][j] == 10 and grid_answer[i][j] == 9:
                cnt += 1
    if cnt == no_bomb:
        game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
        game_over_label.configure(
            text="You Won!",
            bg=c.WINNER_BG,
        )
        game_over_label.pack()

def down(event):
    global y_cursor
    y_cursor += 1
    if y_cursor >= len(grid_user):
        y_cursor = 0
    update_GUI_Cursor()

def up(event):
    global y_cursor
    y_cursor -= 1
    if y_cursor < 0:
        y_cursor = len(grid_user) - 1
    update_GUI_Cursor()
def right(event):
    global x_cursor
    x_cursor += 1
    if x_cursor >= len(grid_user[0]):
        x_cursor = 0
    update_GUI_Cursor()

def left(event):
    global x_cursor
    x_cursor -= 1
    if x_cursor < 0:
        x_cursor = len(grid_user[0]) - 1
    update_GUI_Cursor()

def space(event):
    global grid_answer, first
    open = True
    if first is True:
        grid_answer = generateGrid(rows, cols, no_bomb, y_cursor, x_cursor)
        first = False
    if 0 <= grid_user[y_cursor][x_cursor] <= 8:
        open3x3(grid_user, grid_answer, y_cursor, x_cursor)
    if grid_user[y_cursor][x_cursor] == -1:
        grid_user[y_cursor][x_cursor] = grid_answer[y_cursor][x_cursor]
    game_over()
    update_GUI()

def put_flag(event):
    flag = True
    if grid_user[y_cursor][x_cursor] == -1:
        grid_user[y_cursor][x_cursor] = 10
    elif  grid_user[y_cursor][x_cursor] == 10:
        grid_user[y_cursor][x_cursor] = -1
    game_win()
    update_GUI()

def auto_comp(event):
    test = 0

def restart(event):
    global first, grid_user, grid_answer, game_over_frame
    first = True
    grid_user = generateGrid_with_num(rows, cols, -1)
    grid_answer = generateGrid_with_num(rows, cols, -1)
    game_over_frame.place_forget()
    game_over_label.pack_forget()
    clear_GUI()

def sayHello(event):
    print("Hello")


op = False
flag = False

def setOK():
    global rows, cols, no_bomb
    rows = int_row.get()
    cols = int_col.get()
    no_bomb = num_bomb.get()

setting_win = tk.Tk()
setting_win.geometry('450x150+800+100')

rows = 10
cols = 10
no_bomb = 15

num_bomb = tk.IntVar(
    value=8
)
int_row = tk.IntVar(
    value=9
)
int_col = tk.IntVar(
    value=9
)
box_size = tk.IntVar()


row_label = ttk.Label(setting_win, text="row")
row_entry = ttk.Scale(
    setting_win,
    length=300,
    from_=9,
    to=40,
    command=lambda e : int_row.set(int(float(e))))

row_label_num = ttk.Label(setting_win, textvariable=int_row)

col_label = ttk.Label(setting_win, text="column")
col_entry = ttk.Scale(
    setting_win,
    length=300,
    from_=9,
    to=60,
    command=lambda e : int_col.set(int(float(e))))
col_label_num = ttk.Label(setting_win, textvariable=int_col)

bomb_label = ttk.Label(setting_win, text="No of Bomb")
bomb_scale = ttk.Scale(
    setting_win,
    length=300,
    from_=10,
    to=100,
    command=lambda e : num_bomb.set(int(float(e) / 100 * int_row.get() * int_col.get())))
bomb_label_num = ttk.Label(setting_win, textvariable=num_bomb)

box_size_label = ttk.Label(setting_win, text="Box Size")
box_size_entry = ttk.Scale(
    setting_win,
    length=300,
    from_=0,
    to=100,
    command=lambda e : box_size.set(int(float(e))))
box_size_entry.set(100)
box_size_num_label = ttk.Label(setting_win, textvariable=box_size)

Btn_OK = ttk.Button(setting_win, text="OK", command= lambda : [setOK(), setting_win.destroy()])

row_label.grid(row=0, column=0)
row_entry.grid(row=0, column=1)
row_label_num.grid(row=0, column=2)

col_label.grid(row=1, column=0)
col_entry.grid(row=1, column=1)
col_label_num.grid(row=1, column=2)

bomb_label.grid(row=2, column=0)
bomb_scale.grid(row=2, column=1)
bomb_label_num.grid(row=2, column=2)

box_size_label.grid(row=3, column=0)
box_size_entry.grid(row=3, column=1)
box_size_num_label.grid(row=3, column=2)

Btn_OK.grid(row=4, column=1)

setting_win.mainloop()

screen_width = 1080
screen_height = 1920

if cols > rows:
    box_height = int(screen_height // cols * 0.580 * box_size.get() / 100)
    box_width = int(screen_height // cols  * 0.675 * box_size.get() / 100)
else:
    box_height = int(screen_width // rows * 0.580 * box_size.get() / 100)
    box_width = int(screen_width // rows  * 0.675 * box_size.get() / 100)

margin_box = int(box_width * 0.1)
Number_font = ("Helvetica", int(box_width / 2.3), "bold")
x_cursor = 0
y_cursor = 0

first = True
grid_user = generateGrid_with_num(rows, cols, -1)
grid_answer = generateGrid_with_num(rows, cols, -1)

frame = tk.Frame()
frame.grid()
frame.master.title("2048")

# frame.configure(bg="red", width=1200, height=200)
frame.main_grid = tk.Frame(
    frame, bd=4, bg=c.BG_COLOR, width=box_width * cols, height=box_height * rows
)

frame.main_grid.pack(pady=(0, 0))

cursor_frames = []
for i in range(rows):
    row = []
    for j in range(cols):
        cursor_frame = tk.Frame(
            frame.main_grid,
            bg=c.BG_COLOR,
            width=box_width + margin_box * 2,
            height=box_height + margin_box * 2
        )
        cursor_frame.grid(row=i, column=j)
        row.append(cursor_frame)
    cursor_frames.append(row)
cursor_frames[y_cursor][x_cursor].configure(bg=c.CURSOR_COLOR)

cells = []
for i in range(rows):
    row = []
    for j in range(cols):
        cell_frame = tk.Frame(
            frame.main_grid,
            bg=c.CLOSED_BOX_COLOR,
            width=box_width,
            height=box_height
        )
        cell_frame.grid(row=i, column=j, padx=margin_box, pady=margin_box)
        cell_number = tk.Label(frame.main_grid, bg=c.CLOSED_BOX_COLOR, font=Number_font)
        cell_number.grid(row=i, column=j)

        cell_data = {"frame" : cell_frame, "number" : cell_number}
        row.append(cell_data)
    cells.append(row)

game_over_frame = tk.Frame(frame.main_grid, borderwidth=2)
game_over_label = tk.Label(
            game_over_frame,
            fg=c.GAME_OVER_FONT_COLOR,
            font=c.GAME_OVER_FONT)

frame.master.bind("<Left>", left)
frame.master.bind("<Right>", right)
frame.master.bind("<Up>", up)
frame.master.bind("<Down>", down)
frame.master.bind("<space>", space)
frame.master.bind('f', put_flag)
frame.master.bind('r', restart)
# cursor_frame.grid(row=y_cursor, column=x_cursor)
frame.mainloop()