
from pathlib import Path
from just_playback import Playback
import time
import keyboard
from tkinter import *
import threading


def namelist():             #список файлов вывод в консоль
    for n in mp3_files: 
        print(n.name)


user = Path.home()   # индивидуальный путь
mpfoldread = user/'Music'   #итоговый путь


mp3_files = list(mpfoldread.rglob('*.mp3'))  #пути всех файлов

Player = Playback() #плеер







window = Tk()                             #окно
window.geometry("1000x562")
window.title("wind mp3 player")
window.config(bg=("#0c1114"))


mp3_files_listbox = Listbox(window)              #настройка листбокса
mp3_files_listbox.config(font=("Arial", 15),
                          bg=('#1c272e'), 
                         fg=("#fcfcfc"),
                         selectbackground=("#314552"),
                         height=10,
                         highlightthickness=0,
                         activestyle='none',
                         bd=0)
mp3_files_listbox.grid(row=1, column=1,
                       ipadx=120, ipady=60,
                       sticky="nsew",
                       padx=30,pady=20)

for track in mp3_files:
    mp3_files_listbox.insert(END, track.stem)



Space_past = False
Down = False
Up = False
is_paused = False
ignore_click = False
my_pause = False
number_track = 0



def update_ui_selection():
     global ignore_click
     ignore_click = True
     window.after(0, lambda *args: mp3_files_listbox.selection_clear(0, END))
     window.after(0, lambda *args: mp3_files_listbox.selection_set(number_track))
     window.after(0, lambda *args: mp3_files_listbox.see(number_track))
     window.after(100, lambda *args: globals().update(ignore_click = False))



def on_song_select(*args):
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

mp3_files_listbox.bind("<<ListboxSelect>>", on_song_select)

def control_buttons():
    global Down, Up, Space_past, number_track, ignore_click, my_pause
    while True:


        Space_now = keyboard.is_pressed('Space')                         #Space
        if Space_now and not Space_past:
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

            window.after(100, lambda: globals().update(ignore_click=False))
        Space_past = Space_now
        
        
        
        Down_now = keyboard.is_pressed("Down")
        if Down_now and not Down:                                         #Down
            number_track +=1
            if number_track > len(mp3_files) - 1:
                            number_track = 0
            Player.stop()
            Player.load_file(str(mp3_files[number_track]))
            Player.play()
            my_pause = False
            update_ui_selection()
        Down = Down_now


        Up_now = keyboard.is_pressed("Up")
        if Up_now and not Up:                                                  # Up
                number_track -=1 
                if number_track < 0:
                    number_track = len(mp3_files) - 1
                Player.stop()
                Player.load_file(str(mp3_files[number_track]))
                Player.play()
                my_pause = False
                update_ui_selection()
        Up = Up_now


        if keyboard.is_pressed('Esc'):                                          #Esc
            Player.stop()
            break
        time.sleep(0.05)


t = threading.Thread(target=control_buttons, daemon=True)
t.start()
window.mainloop()

