from tkinter import *
import math
import winsound  # For sound notifications

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
reps = 0
timer = None

# Preset timer durations (in minutes)
TIMER_OPTIONS = {
    "Short (5 min)": 5,
    "Medium (30 min)": 30,
    "Long (60 min)": 60
}
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    """Resets the timer and UI elements."""
    global reps
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer", fg=GREEN)
    check_marks.config(text="")
    reps = 0

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    """Starts the Pomodoro timer based on the selected duration."""
    global reps
    reps += 1

    work_min = TIMER_OPTIONS[selected_timer.get()]
    work_sec = work_min * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
    elif reps % 2 == 0:
        count_down(short_break_sec)
    else:
        count_down(work_sec)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    """Handles countdown and UI updates."""
    count_min = math.floor(count / 60)
    count_sec = count % 60

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec:02d}")

    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        play_sound()  # Play notification sound
        start_timer()
        update_checkmarks()

# ---------------------------- UI UPDATES ------------------------------- #
def update_checkmarks():
    """Updates the checkmarks UI after each work session."""
    work_sessions = math.floor(reps / 2)
    check_marks.config(text="✔" * work_sessions)

# ---------------------------- SOUND NOTIFICATION ------------------------------- #
def play_sound():
    """Plays a beep sound when a session ends."""
    winsound.Beep(2500, 500)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro Timer")
window.config(padx=50, pady=20, bg=YELLOW)

title_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 40))
title_label.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

# Radio buttons for selecting the work session duration
selected_timer = StringVar(value="Short (25 min)")
Label(text="Select Timer:", bg=YELLOW).grid(column=0, row=2, sticky="w")
for i, (text, value) in enumerate(TIMER_OPTIONS.items()):
    Radiobutton(window, text=text, variable=selected_timer, value=text, bg=YELLOW).grid(column=1, row=2+i, sticky="w")

# Buttons
start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=5, pady=10)

reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=5, pady=10)

# Checkmarks for completed work sessions
check_marks = Label(fg=GREEN, bg=YELLOW)
check_marks.grid(column=1, row=6)

window.mainloop()
