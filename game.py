import tkinter as tk
from tkinter import messagebox
import random
import winsound
import os
import sys
def resource_path(filename):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, filename)
# Game Logic

def generate_secret():
    return "".join(
        random.choice("0123456789")
        for _ in range(4)
    )


def count_bulls_cows(secret, guess):

    bulls = 0
    cows = 0

    secret_count = {}
    guess_count = {}

    # Bulls
    for i in range(4):
        if secret[i] == guess[i]:
            bulls += 1
        else:
            secret_count[secret[i]] = secret_count.get(secret[i], 0) + 1
            guess_count[guess[i]] = guess_count.get(guess[i], 0) + 1

    # Cows
    for digit in guess_count:
        if digit in secret_count:
            cows += min(
                guess_count[digit],
                secret_count[digit]
            )

    return bulls, cows



# GUI

class BullsCowsGame:

    def init(self, root):

        self.root = root

        self.root.title("Bulls and Cows")
        self.root.geometry("450x550")
        self.root.configure(bg="#F2E9D0")


        self.secret = ""
        self.attempts = 0
        self.max_attempts = 0


        self.create_widgets()



    def create_widgets(self):

        tk.Label(
            self.root,
            text="🐂 Bulls and Cows 🐄",
            font=("Arial",22,"bold"),
            bg="#F2E9D0"
        ).pack(pady=20)



        tk.Label(
            self.root,
            text="Maximum Attempts:",
            font=("Arial",12),
            bg="#F2E9D0"
        ).pack()


        self.attempt_entry = tk.Entry(
            self.root,
            font=("Arial",14),
            justify="center"
        )

        self.attempt_entry.pack(pady=5)



        tk.Button(
            self.root,
            text="Start Game",
            command=self.start_game,
            bg="#4CAF50",
            fg="white",
            font=("Arial",12,"bold")
        ).pack(pady=10)



        tk.Label(
            self.root,
            text="Enter 4 digit guess:",
            font=("Arial",12),
            bg="#F2E9D0"
        ).pack()



        self.guess_entry = tk.Entry(
            self.root,
            font=("Arial",18),
            justify="center"
        )

        self.guess_entry.pack(pady=5)



        tk.Button(
            self.root,
            text="Guess",
            command=self.check_guess,
            bg="#2196F3",
            fg="white",
            font=("Arial",12,"bold")
        ).pack(pady=10)



        self.status = tk.Label(
            self.root,
            text="Start a new game",
            font=("Arial",12),
            bg="#F2E9D0"
        )

        self.status.pack(pady=10)



        self.history = tk.Text(
            self.root,
            height=10,
            width=40,
            font=("Consolas",11)
        )

        self.history.pack(pady=10)



        tk.Button(
            self.root,
            text="New Game",
            command=self.reset,
            bg="#E53935",
            fg="white",
            font=("Arial",12,"bold")
        ).pack(pady=10)



    def start_game(self):

        try:

            self.max_attempts = int(
                self.attempt_entry.get()
            )

            if self.max_attempts <= 0:
                raise ValueError


        except:

            messagebox.showerror(
                "Error",
                "Enter a valid number of attempts"
            )

            return



        self.secret = generate_secret()

        self.attempts = 0


        self.history.delete(
            "1.0",
            tk.END
        )


        self.status.config(
            text="Game started!"
        )



    def check_guess(self):

        if not self.secret:

            messagebox.showwarning(
                "Warning",
                "Start the game first"
            )

            return



        guess = self.guess_entry.get()



        if len(guess) != 4 or not guess.isdigit():
messagebox.showerror(
                "Invalid",
                "Enter exactly 4 digits"
            )

            return



        self.attempts += 1



        bulls, cows = count_bulls_cows(
            self.secret,
            guess
        )


        self.history.insert(
            tk.END,
            f"🔢 {guess} | 🐂 {bulls} Bulls | 🐄 {cows} Cows\n"
        )



        self.guess_entry.delete(
            0,
            tk.END
        )



        if bulls == 4:

            messagebox.showinfo(
                "Winner",
                "🎉 You found the number!"
            )

            return



        if self.attempts >= self.max_attempts:

            messagebox.showinfo(
                "Game Over",
                f"The number was {self.secret}"
            )

            return



        self.status.config(
            text=f"Attempts: {self.attempts}/{self.max_attempts}"
        )



    def reset(self):

        self.secret = ""
        self.attempts = 0
        self.max_attempts = 0


        self.history.delete(
            "1.0",
            tk.END
        )


        self.guess_entry.delete(
            0,
            tk.END
        )


        self.attempt_entry.delete(
            0,
            tk.END
        )


        self.status.config(
            text="Start a new game"
        )




# Run


window = tk.Tk()

# تشغيل الموسيقى
winsound.PlaySound(
    resource_path("HD.wav"),
    winsound.SND_FILENAME |
    winsound.SND_ASYNC |
    winsound.SND_LOOP
)

# تحميل اللوجو
try:
    icon = tk.PhotoImage(
        file=resource_path("logo.png")
    )

    window.iconphoto(
        True,
        icon
    )

except Exception as e:
    print("Logo error:", e)

game = BullsCowsGame(window)


def close_game():
    winsound.PlaySound(None, winsound.SND_PURGE)
    window.destroy()


window.protocol(
    "WM_DELETE_WINDOW",
    close_game
)

window.mainloop()
