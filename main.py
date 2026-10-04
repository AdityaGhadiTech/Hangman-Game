
import tkinter as tk
import random
import string
import wordpack
import hangmanStages


# ==========================================
# GAME VARIABLES
# ==========================================

random_word = ""
guessed_letters = set()
lives = 6
game_over = False

BG_COLOR = "#1e1e2f"
CARD_COLOR = "#292940"
TEXT_COLOR = "#ffffff"
ACCENT_COLOR = "#ffd166"
GREEN_COLOR = "#06d6a0"
RED_COLOR = "#ef476f"


# ==========================================
# MAIN WINDOW
# ==========================================

window = tk.Tk()
window.title("Hangman Game")
window.geometry("700x760")
window.resizable(False, False)
window.configure(bg=BG_COLOR)


# ==========================================
# FUNCTIONS
# ==========================================

def update_word_display():
    display = []

    for letter in random_word:
        if letter in guessed_letters:
            display.append(letter.upper())
        else:
            display.append("_")

    word_label.config(text="   ".join(display))


def update_hangman():
    # Stage 6 is empty; stage 0 is the complete figure.
    hangman_label.config(
        text=hangmanStages.HANGMAN_STAGES[lives]
    )

    lives_label.config(
        text=f"Lives Remaining: {lives}"
    )


def disable_letter_buttons():
    for button in letter_buttons.values():
        button.config(state="disabled")


def guess_letter(letter):
    global lives, game_over

    if game_over or letter in guessed_letters:
        return

    guessed_letters.add(letter)

    # Disable the selected button
    letter_buttons[letter].config(
        state="disabled",
        bg="#55556e",
        fg="#cccccc"
    )

    if letter.lower() in random_word:
        message_label.config(
            text="Correct guess!",
            fg=GREEN_COLOR
        )
    else:
        lives -= 1
        message_label.config(
            text="Wrong guess! Try another letter.",
            fg=RED_COLOR
        )

    update_word_display()
    update_hangman()

    # Check win
    if all(letter in guessed_letters for letter in random_word):
        game_over = True

        message_label.config(
            text=f"YOU WIN! The word was {random_word.upper()}",
            fg=GREEN_COLOR
        )

        disable_letter_buttons()
        return

    # Check loss
    if lives == 0:
        game_over = True

        word_label.config(
            text="   ".join(random_word.upper())
        )

        message_label.config(
            text=f"GAME OVER! Word: {random_word.upper()}",
            fg=RED_COLOR
        )

        disable_letter_buttons()


def restart_game():
    global random_word, guessed_letters, lives, game_over

    random_word = random.choice(wordpack.WORDS).lower()
    guessed_letters = set()
    lives = 6
    game_over = False

    update_word_display()
    update_hangman()

    message_label.config(
        text="Choose a letter to start guessing!",
        fg=TEXT_COLOR
    )

    for letter, button in letter_buttons.items():
        button.config(
            state="normal",
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        )


# ==========================================
# TITLE
# ==========================================

title_label = tk.Label(
    window,
    text="HANGMAN",
    font=("Arial", 30, "bold"),
    bg=BG_COLOR,
    fg=ACCENT_COLOR
)
title_label.pack(pady=(20, 5))


subtitle_label = tk.Label(
    window,
    text="Guess the hidden word!",
    font=("Arial", 13),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
subtitle_label.pack(pady=(0, 10))


# ==========================================
# HANGMAN DRAWING
# ==========================================

hangman_frame = tk.Frame(
    window,
    bg=CARD_COLOR,
    padx=20,
    pady=10
)
hangman_frame.pack(pady=5)

hangman_label = tk.Label(
    hangman_frame,
    text="",
    font=("Courier New", 12, "bold"),
    bg=CARD_COLOR,
    fg=ACCENT_COLOR,
    justify="left"
)
hangman_label.pack()


# ==========================================
# LIVES COUNTER
# ==========================================

lives_label = tk.Label(
    window,
    text="Lives Remaining: 6",
    font=("Arial", 14, "bold"),
    bg=BG_COLOR,
    fg=RED_COLOR
)
lives_label.pack(pady=10)


# ==========================================
# HIDDEN WORD
# ==========================================

word_label = tk.Label(
    window,
    text="",
    font=("Arial", 23, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
word_label.pack(pady=15)


# ==========================================
# MESSAGE
# ==========================================

message_label = tk.Label(
    window,
    text="Choose a letter to start guessing!",
    font=("Arial", 12, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR,
    wraplength=620
)
message_label.pack(pady=10)


# ==========================================
# LETTER BUTTONS
# ==========================================

keyboard_frame = tk.Frame(
    window,
    bg=BG_COLOR
)
keyboard_frame.pack(pady=10)

letter_buttons = {}

letters = string.ascii_uppercase

for index, letter in enumerate(letters):
    button = tk.Button(
        keyboard_frame,
        text=letter,
        font=("Arial", 12, "bold"),
        width=4,
        height=1,
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        activebackground=ACCENT_COLOR,
        activeforeground=BG_COLOR,
        relief="flat",
        cursor="hand2",
        command=lambda char=letter.lower(): guess_letter(char)
    )

    # 7 letters in each row
    button.grid(
        row=index // 7,
        column=index % 7,
        padx=4,
        pady=5
    )

    letter_buttons[letter.lower()] = button


# ==========================================
# RESTART BUTTON
# ==========================================

restart_button = tk.Button(
    window,
    text="PLAY AGAIN",
    font=("Arial", 13, "bold"),
    width=18,
    height=2,
    bg=ACCENT_COLOR,
    fg=BG_COLOR,
    activebackground="#ffe29a",
    relief="flat",
    cursor="hand2",
    command=restart_game
)
restart_button.pack(pady=20)


# ==========================================
# START GAME
# ==========================================

restart_game()

window.mainloop()