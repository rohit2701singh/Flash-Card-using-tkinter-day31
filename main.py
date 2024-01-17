from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"
TITLE = "french"
current_word_selection = {}
to_learn = {}

'''
how orient= "records" work?
df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
dict_records = df.to_dict(orient="records")
print(dict_records)
output: [{'A': 1, 'B': 3}, {'A': 2, 'B': 4}]
'''

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except (FileNotFoundError, pandas.errors.EmptyDataError):
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")     # {'French': 'affaire', 'English': 'case'}
else:
    to_learn = data.to_dict(orient="records")

french_word_list = []
english_word_list = []


def unknown_random_word():
    """❌ button clicked, i.e. user don't know the word meaning."""

    global current_word_selection, flip_timer
    window.after_cancel(flip_timer)

    current_word_selection = random.choice(to_learn)
    # print(current_word_selection)

    canvas.itemconfig(card_title, text="french", fill="black")
    canvas.itemconfig(card_word, text=current_word_selection['French'], fill="black")
    canvas.itemconfig(canvas_image, image=card_front_img)

    # list of those words which appears recently
    french_word_list.append(current_word_selection["French"])
    english_word_list.append(current_word_selection['English'])

    unknown_word = {
        "French": french_word_list,
        "English": english_word_list,
    }
    new_data = pandas.DataFrame(unknown_word)
    new_data.to_csv("data/word_seen_recently.csv", index=False)

    flip_timer = window.after(3000, func=english_word_flip)


def english_word_flip():
    canvas.itemconfig(canvas_image, image=card_back_img)
    canvas.itemconfig(card_title, text="english", fill="white",)
    canvas.itemconfig(card_word, text=current_word_selection['English'], fill="white")


def is_known():
    """✔️ button clicked, user knows meaning"""

    to_learn.remove(current_word_selection)  # remove word so that it don't appear again.
    new_data = pandas.DataFrame(to_learn)   # create new data file which contain words not appeared yet.
    new_data.to_csv("data/words_to_learn.csv", index=False)
    unknown_random_word()   # to show a new word


window = Tk()
window.title("Flash card")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=english_word_flip)     # after 3 sec call function
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front_img, )
card_title = canvas.create_text(400, 150, text="", font=("ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2, padx=5)

wrong_img = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_img, bd=0, highlightthickness=0, command=unknown_random_word)
wrong_button.grid(column=0, row=1)

right_img = PhotoImage(file="./images/right.png")
right_button = Button(image=right_img, bd=0, highlightthickness=0, command=is_known)
right_button.grid(column=1, row=1)

unknown_random_word()

window.mainloop()
