from tkinter import *
from random import *
from winsound import *
from time import *

def play_sound_ok():
    files = []
    for i in range(1, 7):
        files.append(f"hit{i}.wav")
    file = choice(files)
    PlaySound(file, SND_ASYNC | SND_FILENAME)

def play_sound_fail():
    files = []
    for i in range(1, 8):
        files.append(f"fail{i}.wav")
    file = choice(files)
    PlaySound(file, SND_ASYNC | SND_FILENAME)

def collision_detection(x, y):
    position = canvas.coords(npc_id)
    left = position[0]
    right = position[0] + npc_width
    top = position[1]
    bottom = position[1] + npc_height
    return left <= x <= right and top <= y <= bottom

def hit():
    global score
    score += 1
    update_points()
    play_sound_ok()
    spawn()

def missclick():
    global score
    score -= 1
    if score < 0:
        game_over()
    else:
        update_points()
        play_sound_fail()



def game_update():
    global canvas
    spawn()
    if randint(1, 2) == 1:
        canvas.itemconfig(npc_id, image=bottom_image)
    else:
        canvas.itemconfig(npc_id, image=top_image)
    window.after(1000, game_update)

def update_points():
    canvas.itemconfigure(text_id, text=f'Очки: {score}')

def game_over():
    global gameover
    canvas.itemconfigure(text_id, text='ПОТРАЧЕНО')
    gameover = True
    PlaySound('gameover.wav', SND_ASYNC | SND_FILENAME)

def mouse_click(e):
    if gameover:
        return
    if collision_detection(e.x, e.y):
        hit()
    else:
        missclick()

def mouse_motion(event):
    global mouse_x, mouse_y
    mouse_x, mouse_y = event.x, event.y

def show_start_screen():
    global start_message
    canvas.config(bg="black")
    start_message = canvas.create_text(game_width / 2, game_height / 2, text="Поймай муху,пока она не поймала тебя", fill="white", font="Arial 30")
    window.after(4000, hide_start_screen)

def hide_start_screen():
    canvas.delete(start_message)
    start_game()

def spawn():
    global npc_id
    for i in range(100):
        x = randint(0, game_width - npc_width)
        y = randint(0, game_height - npc_height)
        if abs(mouse_x - x) > 200 or abs(mouse_y - y) > 200:
            canvas.moveto(npc_id, x, y)
            canvas.itemconfig(npc_id, state='normal')  # Показываем изображение при спавне
            break

def start_game():
    global game_time_left, gameover
    score = 0  # Сбросим счёт в начале игры
    game_time_left = 5000
    gameover = False
    canvas.config(bg="white")
    update_points()  # Обновляем отображение счёта
    spawn()  # Сначала мы спавним муху
    update_timer()
    game_update()


def update_timer():
    global game_time_left
    if game_time_left > 0:
        game_time_left -= 1000
        timer_label.config(text=f"Время: {game_time_left // 1000}")
        window.after(1000, update_timer)
    else:
        end_game()

def end_game():
    global gameover
    gameover = True
    # canvas.config(bg="pink")
    # canvas.delete("all")
    canvas.itemconfig(fon, state='normal')
    final_score_label = Label(canvas, text=f"Конец игры!\nВаш счёт: {score}", font="Arial 40")
    final_score_label.place(relx=0.5, rely=0.5, anchor=CENTER)

game_width = 720
game_height = 720
npc_width = 120
npc_height = 95
score = 10
mouse_x = mouse_y = 0
gameover = False
game_time_left = 0
window = Tk()

bottom_image = PhotoImage(file='myxa_niz.png')
top_image = PhotoImage(file='myxa_verx.png')

window.title('Проучи тролля')
window.resizable(width=False, height=False)
canvas = Canvas(window, width=game_width, height=game_height, bg="black")
npc_id = canvas.create_image(0, 0, anchor='nw', image=bottom_image)
canvas.itemconfig(npc_id, state='hidden')  # Скрываем изображение перед началом игры
timer_label = Label(canvas, text="", font="Arial 16", fg="black", bg="white")
timer_label.place(x=10, y=10)






screamer_image = PhotoImage(file='screamer.png')
screamer_id = canvas.create_image(0, 0, image=screamer_image,
                                  anchor=NW)
canvas.itemconfig(screamer_id, state='hidden')

background_image = PhotoImage(file='forest.png')
fon  = canvas.create_image(0, 0, image=background_image, anchor=NW, state='hidden')
text_id = canvas.create_text(
    game_width - 10, 10,
    fill='black',
    font='Times 20 bold',
    text=f'Очки: {score}',
    anchor=NE)

canvas.bind('<Button>', mouse_click)
canvas.bind('<Motion>', mouse_motion)

canvas.pack()
show_start_screen()
window.mainloop()