
from pathlib import Path
from just_playback import Playback
import time
import keyboard
from tkinter import *
from tkinter import ttk
import threading


def namelist():             #список файлов вывод в консоль
    for n in mp3_files: 
        print(n.name)




def toggle():
    global number_track, my_pause, ignore_click
    ignore_click = True
    if not Player.active:
        Player.load_file(str(mp3_files[number_track]))
        Player.play()
        my_pause = False
        update_ui_selection()
                 
    elif my_pause == True:
        Player.resume()
        my_pause = False
    else:
        Player.pause()
        my_pause = True
    window.after(200, lambda *args: globals().update(ignore_click=False))

def down():
    global my_pause, number_track
    number_track +=1
    if number_track > len(mp3_files) - 1:
        number_track = 0
    Player.stop()
    Player.load_file(str(mp3_files[number_track]))
    Player.play()
    my_pause = False
    update_ui_selection()

def up():
    global my_pause, number_track
    number_track -=1
    if number_track < 0:
        number_track = len(mp3_files) - 1
    Player.stop()
    Player.load_file(str(mp3_files[number_track]))
    Player.play()
    my_pause = False
    update_ui_selection()


def main_button_click():
    global ignore_click
    ignore_click = True
    toggle()
    window.after(200, lambda *args: globals().update(ignore_click=False))





def update_ui_selection():                                             #обновление подсветки трека
     global ignore_click
     ignore_click = True
     mp3_files_listbox.selection_clear(0, END)
     mp3_files_listbox.selection_set(number_track)
     mp3_files_listbox.see(number_track)
     window.after(200, lambda *args: globals().update(ignore_click=False))



def on_song_select(*args):                                                   #функция для прослушивания клика по листбоксу
    global number_track, old_index, Space_pause, my_pause, ignore_click
    if ignore_click:
             return
    old_index = number_track
    selected_index = mp3_files_listbox.curselection()
    if selected_index:
        new_index = selected_index[0]

        if new_index == number_track:
            if my_pause == True:
                 Player.resume()
                 my_pause = False
                 return
            elif my_pause == False:
                 Player.pause()
                 my_pause = True
                 return
    
            
                    
        number_track = selected_index[0]
        Player.stop()
        Player.load_file(str(mp3_files[number_track]))
        Player.play()


def control_buttons():                                                                     # ==взаимодействие с кнопками==
    global Down, Up, Space_past, number_track, ignore_click, my_pause
    while True:


        Space_now = keyboard.is_pressed('Space')                         #Space
        if Space_now and not Space_past:
           toggle()
        Space_past = Space_now
        
        
        
        Down_now = keyboard.is_pressed("Down")
        if Down_now and not Down:
            down()
        Down = Down_now


        Up_now = keyboard.is_pressed("Up")
        if Up_now and not Up:                                                  # Up
                up()
        Up = Up_now


        if keyboard.is_pressed('Esc'):                                          #Esc
            Player.stop()
            break
        time.sleep(0.05)





#------------------------------------------------------------------------------------------------


user = Path.home()   # индивидуальный путь
mpfoldread = user/'Music'   #итоговый путь


mp3_files = list(mpfoldread.rglob('*.mp3'))  #пути всех файлов

Player = Playback() #плеер





window = Tk()                             #окно
window.geometry("1200x675")
window.title("wind mp3 player")
window.config(bg=("#0c1114"))

window.bind_class("Button", "<space>", lambda e: "break")





mp3_files_listbox = Listbox(window)              #настройка листбокса
mp3_files_listbox.config(font=("Arial", 15),
                          bg=('#1c272e'), 
                         fg=("#fcfcfc"),
                         selectbackground=("#314552"),
                         height=10,
                         highlightthickness=0,
                         activestyle='none',
                         bd=0)
mp3_files_listbox.place(x=30, y=150, height=400, width=480, anchor="nw")

for track in mp3_files:
    mp3_files_listbox.insert(END, track.stem)



style = ttk.Style()                                       #стиль для рамки
style.configure('My.TFrame', background="#0c1114")

frame_buttons_control = ttk.Frame(window, style='My.TFrame')                 #настройка рамки
frame_buttons_control.place(x=650, y=550, width=400, height=140)




play_button = ttk.Button(frame_buttons_control, command=main_button_click, takefocus=0)                                    
play_button.config(text="Play")
play_button.place(x=200, y=10, width=65, height=65)

up_button = ttk.Button(frame_buttons_control, command=up, takefocus=0)
up_button.config(text="Up")
up_button.place(x=125, y=15, width=55, height=55)


down_button = ttk.Button(frame_buttons_control, command=down, takefocus=0)
down_button.config(text="Down")
down_button.place(x=285, y=15, width=55, height=55)


Space_past = False
Down = False
Up = False
is_paused = False
ignore_click = False
my_pause = False
number_track = 0

mp3_files_listbox.bind("<<ListboxSelect>>", on_song_select)                 #прослушивание клика по листбоксу
mp3_files_listbox.bind("<space>", lambda event: "break")                    #прослушивание пробела по листбоксу




t = threading.Thread(target=control_buttons, daemon=True)
t.start()
window.mainloop()

