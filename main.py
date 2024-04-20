from tkinter import *
import pandas
import random

#global value
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

#setup
window = Tk()
window.title("Word")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.option_add('*Dialog.msg.font', 'Helvetica 12')

#import csv file
try:
    #try to read the file 'words_to_know.csv' first
    words = pandas.read_csv("data/words_to_know.csv")
except FileNotFoundError:
    #for an exception(FileNotFoundError, doesn't exist), read the file 'korean_word.csv', and rearrange it and store in to_learn
    original_data = pandas.read_csv("data/korean_word.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    #if no problems, rearrange csv file to read easily and store in to_learn
    to_learn = words.to_dict(orient="records")

#korean card
def korean_card():
    global current_card, flip_timer
    #stop flipping
    window.after_cancel(flip_timer)
    canvas.itemconfig(canvas_image, image=card_back_image)
    current_card = random.choice(to_learn)
    random_korean_word = current_card["Koreanisch"]
    canvas.itemconfig(korean, text="Koreanisch", fill='#FFFFFF')
    canvas.itemconfig(korean_word, text=random_korean_word, fill='#FFFFFF')
    #resume flipping
    flip_timer = window.after(3000,german_card)

#german card
def german_card():
    canvas.itemconfig(canvas_image, image=card_front_image)
    random_german_word = current_card["Deutsch"]
    canvas.itemconfig(korean, text="Deutsch", fill='#000000')
    canvas.itemconfig(korean_word, text=random_german_word, fill='#000000')
    
def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("words_to_learn.csv", index=False)
    korean_card()

#flip to german card after 3 seconds
flip_timer = window.after(3000, func=german_card)

#import images
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
right_image = PhotoImage(file="images/right.png")
wrong_image = PhotoImage(file="images/wrong.png")

#arrangement
#images
canvas = Canvas(width=800, height=526, highlightthickness=0)
canvas_image = canvas.create_image(400,263, image=card_front_image)
canvas.config(bg=BACKGROUND_COLOR)
canvas.grid(column=0, row=0, columnspan=2)

#buttons
right_button = Button(image=right_image, highlightthickness=0, command=korean_card)
right_button.grid(column=0, row=1)
wrong_button = Button(image=wrong_image, highlightthickness=0, command=is_known)
wrong_button.grid(column=1, row=1)

#texts
korean = canvas.create_text(400,150, text="", font=("Ariel",40,"italic"))
korean_word = canvas.create_text(400, 283, text="", font=("Ariel",60,"bold"))

korean_card()

window.mainloop()