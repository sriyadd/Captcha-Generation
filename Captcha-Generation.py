from io import BytesIO
from tkinter import *
from random import *
from tkinter import messagebox
from captcha.image import ImageCaptcha
from PIL import Image, ImageTk

# Initialize ImageCaptcha object with custom fonts
image = ImageCaptcha(
    fonts=[
        "./Fonts/ChelseaMarketsr.ttf",
        "./Fonts/DejaVuSanssr.ttf",
    ]
)

# Difficulty levels and their corresponding timer settings (in seconds)
difficulty_levels = {
    "Beginner": 45,
    "Intermediate": 30,
    "Advanced": 20
}

# Initialize current difficulty level
current_difficulty = "Beginner"
timer = None
timer_event = None

# Initialize the Tkinter window
root = Tk()

# Create Tkinter widgets for CAPTCHA display
l1 = Label(root, height=100, width=200)
t1 = Text(root, height=5, width=50)
b1 = Button(root, text="Submit")
b2 = Button(root, text="Refresh")
timer_label = Label(root)
difficulty_label = Label(root)

# Function to generate a random CAPTCHA value and save the image
def generate_captcha():
    global random_value
    random_value = str(randint(100000, 999999))
    data = image.generate(random_value)
    assert isinstance(data, BytesIO)
    image.write(random_value, "captcha.png")
    img = Image.open("captcha.png")
    img = img.resize((200, 100), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(img)
    l1.config(image=photo)
    l1.image = photo

# Function to verify the entered CAPTCHA
def verify():
    x = t1.get("1.0", END)
    if int(x) == int(random_value):
        messagebox.showinfo("Success", "Verified")
    else:
        messagebox.showinfo("Alert", "Not verified")
        refresh()

# Function to refresh CAPTCHA and start timer
def refresh():
    global timer, timer_event
    generate_captcha()
    timer = difficulty_levels[current_difficulty]
    timer_label.config(text=f"Time left: {timer}")
    if timer_event:
        root.after_cancel(timer_event)
    timer_event = root.after(1000, start_timer)

# Function to start timer based on current difficulty level
def start_timer():
    global timer, timer_event
    if timer > 0:
        timer -= 1
        timer_label.config(text=f"Time left: {timer}")
        timer_event = root.after(1000, start_timer)
    else:
        messagebox.showinfo("Time's Up!", "Please refresh the CAPTCHA.")
        t1.delete("1.0", END)
        refresh()

# Function to change difficulty level
def change_difficulty(difficulty):
    global current_difficulty, timer, timer_event
    current_difficulty = difficulty
    difficulty_label.config(text=f"Difficulty: {current_difficulty}")
    timer = difficulty_levels[current_difficulty]
    timer_label.config(text=f"Time left: {timer}")
    refresh()

# Load the initial CAPTCHA image
generate_captcha()

b1.config(command=verify)
b2.config(command=refresh)
timer_label.config(text=f"Time left: {difficulty_levels[current_difficulty]}")
difficulty_label.config(text=f"Difficulty: {current_difficulty}")

# Pack Tkinter widgets
l1.pack()
t1.pack()
b1.pack()
b2.pack()
timer_label.pack()
difficulty_label.pack()

# Create buttons for changing difficulty level
for difficulty in difficulty_levels.keys():
    button = Button(root, text=difficulty, command=lambda d=difficulty: change_difficulty(d))
    button.pack(side=LEFT)

# Start the Tkinter event loop
root.mainloop()
