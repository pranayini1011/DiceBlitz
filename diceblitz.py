import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

# Setup CustomTkinter Appearance
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Create the Main Window
root = ctk.CTk()
root.title("DiceBlitz - Two Player Dice Game")
root.geometry("800x600")
root.resizable(False, False)

# Load Background Image and Resize to Fit Window
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

bg_image = Image.open("assets/dice bg.png")
bg_image = bg_image.resize((screen_width, screen_height))
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)


# Load Dice Images
dice_images = []
for i in range(1, 7):
    img = Image.open(f"assets/dice{i}.png").resize((100, 100))
    dice_images.append(ImageTk.PhotoImage(img))

# Game Variables
player1_score = 0
player2_score = 0
rounds = 0
max_rounds = 7
power_used = {"p1": False, "p2": False}

# Title Label
label_title = tk.Label(root, text="🎲 DiceBlitz 🎲", font=("Verdana", 26, "bold"), bg="#ffffff", fg="#333333")
label_title.pack(pady=10)

# Player Name Inputs
entry_frame = tk.Frame(root, bg="#ffffff")
entry_frame.pack(pady=5)

tk.Label(entry_frame, text="Player 1 Name:", font=("Verdana", 12), bg="#ffffff").grid(row=0, column=0, padx=10)
player1_name_var = tk.StringVar(value="Player 1")
entry_p1 = ctk.CTkEntry(entry_frame, textvariable=player1_name_var, width=140, font=("Verdana", 12))
entry_p1.grid(row=0, column=1)

tk.Label(entry_frame, text="Player 2 Name:", font=("Verdana", 12), bg="#ffffff").grid(row=0, column=2, padx=10)
player2_name_var = tk.StringVar(value="Player 2")
entry_p2 = ctk.CTkEntry(entry_frame, textvariable=player2_name_var, width=140, font=("Verdana", 12))
entry_p2.grid(row=0, column=3)

# Dice Area
frame = tk.Frame(root, bg="#ffffff")
frame.pack()

label_p1 = tk.Label(frame, textvariable=player1_name_var, font=("Verdana", 18, "bold"), bg="#ffffff", fg="#1f4e79")
label_p1.grid(row=0, column=0, padx=20)

label_p2 = tk.Label(frame, textvariable=player2_name_var, font=("Verdana", 18, "bold"), bg="#ffffff", fg="#9c2c77")
label_p2.grid(row=0, column=2, padx=20)

dice_label1 = tk.Label(frame, image=dice_images[0], bg="#ffffff")
dice_label1.grid(row=1, column=0, padx=20)

vs_label = tk.Label(frame, text="VS", font=("Verdana", 16, "bold"), bg="#ffffff", fg="#000000")
vs_label.grid(row=1, column=1)

dice_label2 = tk.Label(frame, image=dice_images[0], bg="#ffffff")
dice_label2.grid(row=1, column=2, padx=20)

# Labels for Results
result_label = tk.Label(root, text="", font=("Verdana", 14, "italic"), bg="#ffffff", fg="#222222")
result_label.pack(pady=10)

final_result_label = tk.Label(root, text="", font=("Verdana", 16, "bold"), bg="#ffffff", fg="#007f5f")
final_result_label.pack()

# Game Logic
def roll_dice(power_p1=False, power_p2=False):
    global player1_score, player2_score, rounds

    if rounds >= max_rounds:
        result_label.config(text="Game has ended. Please reset to play again.")
        return

    if power_p1 and not power_used["p1"]:
        roll1 = max(random.randint(1, 6), random.randint(1, 6))
        power_used["p1"] = True
        button_power1.configure(state="disabled")
    else:
        roll1 = random.randint(1, 6)

    if power_p2 and not power_used["p2"]:
        roll2 = max(random.randint(1, 6), random.randint(1, 6))
        power_used["p2"] = True
        button_power2.configure(state="disabled")
    else:
        roll2 = random.randint(1, 6)

    dice_label1.config(image=dice_images[roll1 - 1])
    dice_label2.config(image=dice_images[roll2 - 1])

    if roll1 > roll2:
        player1_score += 1
        result = f"{player1_name_var.get()} wins this round!"
    elif roll2 > roll1:
        player2_score += 1
        result = f"{player2_name_var.get()} wins this round!"
    else:
        result = "It's a tie!"

    rounds += 1
    result += f" (Round {rounds}/{max_rounds})"
    result_label.config(text=result)

    if rounds == max_rounds:
        if player1_score > player2_score:
            winner = f"🎉 {player1_name_var.get()} Wins!"
        elif player2_score > player1_score:
            winner = f"🎉 {player2_name_var.get()} Wins!"
        else:
            winner = "🤝 It's a Draw!"
        final_result_label.config(text=winner)

# Buttons
button_roll = ctk.CTkButton(root, text="🎲 Roll Dice", command=roll_dice, width=200, height=40, corner_radius=20, font=("Verdana", 14))
button_roll.pack(pady=10)

# Power Roll Buttons
power_frame = tk.Frame(root, bg="#ffffff")
power_frame.pack(pady=5)

button_power1 = ctk.CTkButton(power_frame, text="Power Roll - P1", command=lambda: roll_dice(power_p1=True), width=150, height=35, corner_radius=20, font=("Verdana", 12))
button_power1.grid(row=0, column=0, padx=10)

button_power2 = ctk.CTkButton(power_frame, text="Power Roll - P2", command=lambda: roll_dice(power_p2=True), width=150, height=35, corner_radius=20, font=("Verdana", 12))
button_power2.grid(row=0, column=1, padx=10)

# Reset Function
def reset_game():
    global player1_score, player2_score, rounds, power_used
    player1_score = 0
    player2_score = 0
    rounds = 0
    power_used = {"p1": False, "p2": False}
    result_label.config(text="")
    final_result_label.config(text="")
    dice_label1.config(image=dice_images[0])
    dice_label2.config(image=dice_images[0])
    button_power1.configure(state="normal")
    button_power2.configure(state="normal")

# Reset and Quit Buttons
button_reset = ctk.CTkButton(root, text="Reset Game", command=reset_game, width=200, height=35, corner_radius=20, font=("Verdana", 12))
button_reset.pack(pady=5)

button_quit = ctk.CTkButton(root, text="Quit", command=root.destroy, width=200, height=35, corner_radius=20, font=("Verdana", 12))
button_quit.pack(pady=5)

# Main Loop
root.mainloop()
