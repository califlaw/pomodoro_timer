from tkinter import *
import math
import platform
import os
import subprocess

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 0.1
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None


# ---------------------------- POP UP ON TOP OF ALL APPS ------------------------------- #
def raise_app(root: Tk):
    root.attributes("-topmost", True)
    if platform.system() == 'Darwin':
        tmpl = 'tell application "System Events" to set frontmost of every process whose unix id is {} to true'
        script = tmpl.format(os.getpid())
        output = subprocess.check_call(['/usr/bin/osascript', '-e', script])
    root.after(0, lambda: root.attributes("-topmost", False))


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    label.config(text="Timer")
    checkmark.config(text="")
    global reps
    reps = 0


# ---------------------------- POP UP MESSAGE ------------------------------- #
def popupmsg_break_work(action):
    popup = Tk()
    popup.wm_title(f"{action}")
    popup_label = Label(popup, text=f"{action}", font=FONT_NAME)
    popup_label.pack(side="top", fill="x", pady=10)
    b1 = Button(popup, text="Okay", command=popup.destroy)
    b1.pack()
    raise_app(popup)
    popup.mainloop()


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        label.config(text="BREAK", fg=RED)
        popupmsg_break_work("Break time")
    elif reps % 2 == 0:
        count_down(short_break_sec)
        label.config(text="BREAK", fg=PINK)
        popupmsg_break_work("Break time")
    else:
        count_down(work_sec)
        label.config(text="WORK", fg=GREEN)
        popupmsg_break_work("Work time")


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps / 2)
        for _ in range(work_sessions):
            marks += "✔"
        checkmark.config(text=marks)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

label = Label(text="TIMER", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50))
label.grid(column=1, row=0)

start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
photo_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=photo_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

checkmark = Label(text="✔", fg=GREEN, bg=YELLOW)
checkmark.grid(column=1, row=3)

window.mainloop()
