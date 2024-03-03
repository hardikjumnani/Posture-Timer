# Importing Modules
from datetime import datetime
from customtkinter import *
import customtkinter as ctk
import pyautogui as pg
from PIL import Image
import time
from threading import Thread

# lambda:True -> To do nothing :)

root = CTk()

var_timer_label = StringVar(value='Hey! You have been working for a while now, let\'s take a break.')
var_timer_minutes = IntVar(value=5) # Break Time
var_timer_wait = IntVar(value=3) # Snooze Time
var_work_time = IntVar(value=25) # Work Time
SCREEN_WIDTH, SCREEN_HEIGHT= pg.size()

root.grab_set() # used to force focus the window

root.attributes('-fullscreen', True)
# root.overrideredirect(True)
root.geometry(f'{SCREEN_WIDTH}x{SCREEN_HEIGHT}')

def fn_show_screen() -> None:
    root.deiconify()

def fn_hide_screen() -> None:
    root.withdraw()

def fn_start_timer() -> None:
    var_timer_label.set('Hey! You have been working for a while now, let\'s take a break.')

    fn_hide_screen()
    lbl_break.configure(text=var_timer_label.get())
    root.update()
    win_break_timer()
    fn_show_screen()

def fn_wait_timer() -> None:
    var_timer_label.set('C\'mon, no snoozing now!')

    # root.quit()
    fn_hide_screen()
    time.sleep(int(var_timer_wait.get()*60))
    lbl_break.configure(text=var_timer_label.get())
    fn_show_screen()


def win_settings() -> None:
    win_sett = CTkToplevel(root)

    win_sett.title('Settings')
    win_sett.geometry(f'400x300+400+600')
    win_sett.resizable(False, False) # width, height
    win_sett.grab_set()
    # win_sett.grab_set_global() # 🔥🔥🔥🔥🔥🔥

    def fn_close():
        win_sett.destroy()
        win_sett.update()
        root.update()
    
    def fn_save():
        var_timer_minutes.set(new_entry_timer_minutes.get())
        var_timer_wait.set(new_entry_timer_wait.get())

        btn_yes.configure(text=f'Yes, be back\nin {var_timer_minutes.get()} minutes')
        btn_no.configure(text=f'Just give\nme {var_timer_wait.get()} min.')

        fn_close()

    # ====Widgets====
    # Frame main
    new_frame_1 = CTkFrame(win_sett, fg_color='transparent')
    new_frame_1.pack(pady=10)
    
    # Row 1
    new_lbl_timer_minutes = CTkLabel(new_frame_1, text='Break Time (minutes)')
    new_lbl_timer_minutes.grid(row=0, column=0, padx=10, pady=10)

    new_entry_timer_minutes = CTkEntry(new_frame_1, textvariable=var_timer_minutes)
    new_entry_timer_minutes.grid(row=0, column=1, padx=10, pady=10)

    # Row 2
    new_lbl_timer_wait = CTkLabel(new_frame_1, text='Snooze Time (minutes)')
    new_lbl_timer_wait.grid(row=1, column=0, padx=10, pady=10)

    new_entry_timer_wait = CTkEntry(new_frame_1, textvariable=var_timer_wait)
    new_entry_timer_wait.grid(row=1, column=1, padx=10, pady=10)

    # Row 3
    new_lbl_timer_work = CTkLabel(new_frame_1, text='Work Time (minutes)')
    new_lbl_timer_work.grid(row=2, column=0, padx=10, pady=10)

    new_entry_timer_work = CTkEntry(new_frame_1, textvariable=var_work_time)
    new_entry_timer_work.grid(row=2, column=1, padx=10, pady=10)

    # Save Button
    new_btn_save = CTkButton(win_sett, text='Save', command=fn_save)
    new_btn_save.pack(pady=10)

    win_sett.protocol("WM_DELETE_WINDOW", fn_close)

def win_break_timer() -> None:
    win_brea = CTkToplevel(root)
    win_brea.grab_set()

    win_brea.title('Timer')
    win_brea.attributes('-fullscreen', True)
    win_brea.geometry(f'{SCREEN_WIDTH}x{SCREEN_HEIGHT}')
    win_brea.grab_set()
    # win_brea.grab_set_global() # 🔥🔥🔥🔥🔥🔥

    def fn_close() -> None:
        win_brea.destroy()
        # waits here for work time
        fn_hide_screen()
        
        time.sleep(int(var_work_time.get() *60))

        win_brea.update()
        root.update()
        fn_show_screen()
    
    def fn_countdown() -> None:
        curr_time_sec = var_timer_minutes.get() * 60 #secs
        while curr_time_sec: 
            mins, secs = divmod(curr_time_sec, 60) 
            # timer = '{:02d}:{:02d}'.format(mins, secs) 
            timer = f'{mins:02d}:{secs:02d}'
            lbl_timer.configure(text=timer)

            time.sleep(1)
            curr_time_sec -= 1
        fn_close()


    
    # Widgets
    btn_close = CTkButton(win_brea, text='', command=fn_close, image=icon_quit, width=50, fg_color='#202020', hover_color='#404040')
    btn_close.place(x=SCREEN_WIDTH*0.02, y=SCREEN_HEIGHT*0.03)

    lbl_timer = CTkLabel(win_brea, text='', font=custom_font_prim)
    lbl_timer.pack(pady=100)

    # Thread so that person can use X or close window if needed.
    countdown_thread = Thread(target=fn_countdown)
    countdown_thread.start()

    win_brea.protocol("WM_DELETE_WINDOW", fn_close)


# ======= Root App Widgets ============
custom_font_prim = CTkFont(family='Arial', size=int(SCREEN_WIDTH*0.02))
custom_font_secn = CTkFont(family='Helvetica', size=int(SCREEN_WIDTH*0.01))

# Quit Button
icon_quit = CTkImage(dark_image=Image.open('AppData/icons/png/close.png'), size=(30, 30))
btn_close = CTkButton(root, text='', command=lambda:root.quit(), image=icon_quit, width=50, fg_color='red', hover_color='darkred')
btn_close.place(x=SCREEN_WIDTH*0.02, y=SCREEN_HEIGHT*0.03)

# Settings Button
icon_setting = CTkImage(dark_image=Image.open('AppData/icons/png/setting.png'), size=(30, 30))
btn_settings = CTkButton(root, text='', command=win_settings, image=icon_setting, width=50)
btn_settings.place(x=SCREEN_WIDTH*0.75, y=SCREEN_HEIGHT*0.03)

# Header Label
lbl_break = CTkLabel(root, text=var_timer_label.get(), font=custom_font_prim)
lbl_break.pack(pady=SCREEN_HEIGHT*0.1)


# Buttons
frame_buttons = CTkFrame(root, fg_color='transparent')
frame_buttons.pack(pady=SCREEN_HEIGHT*0.1)

btn_yes = CTkButton(frame_buttons, 
                    text=f'Yes, be back\nin {var_timer_minutes.get()} minutes', 
                    font=custom_font_secn, 
                    command=fn_start_timer,
                    text_color='black',
                    fg_color='lightgrey',
                    hover_color='darkgrey')
btn_yes.grid(row=0, column=0, padx=SCREEN_WIDTH*0.05, ipadx=50, ipady=8)

btn_no = CTkButton(frame_buttons, 
                   text=f'Just give\nme {var_timer_wait.get()} min.', 
                   font=custom_font_secn, 
                   command=fn_wait_timer,
                   text_color='#505050',
                   fg_color='transparent',
                   hover_color='#404040')
btn_no.grid(row=0, column=1, padx=SCREEN_WIDTH*0.05, ipadx=50, ipady=8)

root.protocol("WM_DELETE_WINDOW", lambda: True)
root.mainloop()