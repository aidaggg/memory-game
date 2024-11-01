import tkinter as tk
import random
import time
from tkinter import messagebox
import math

#Create the main window
window = tk.Tk()
window.title("Memory Game")

#Window size
window.geometry("600x600")

#Create the cards and the list
num_pairs = 8
num_cards = num_pairs * 2
cards = list(range(num_pairs )) * 2  
random.shuffle(cards)  #Shuffle cards -- mezclar

#List to store the buttons
buttons = []

'''VARIABLES'''
first_card = None
second_card = None
failed_attempts = 0
matched_pairs = 0
start_time = 0
game_started = False


'''FUNCTIONS'''
def start_game():
    global game_started, start_time
    game_started = True
    start_time = time.time()
    update_timer()

    #hide the start button and show the game screen
    start_screen.pack_forget()  
    game_screen.pack()
    
    for button in buttons:
        button.config(state=tk.NORMAL) #if the game has started it is possible to click on the cards

#if the restart button is pressed
def restart_game():
    global first_card, second_card, failed_attempts, matched_pairs, game_started, timer_running, start_time, cards
    
    #reset variables
    first_card = None
    second_card = None
    failed_attempts = 0
    matched_pairs = 0
    game_started = False
    timer_running = False
    start_time = 0

    #Shuffle cards
    random.shuffle(cards)

    #Reset all button texts and disable them
    for button in buttons:
        button.config(text="", state=tk.DISABLED)

    #Reset labels
    timer.config(text="Time in seconds: 0s")
    attempts.config(text="Failed attempts: 0")

    game_screen.pack_forget()   #hide the screen of the game
    start_screen.pack()         #show the start button

def update_timer():
    if game_started:
        elapsed_time = int(time.time() - start_time)
        timer.config(text=f"Time in seconds: {elapsed_time}s")
        window.after(1000, update_timer)

#When we click a card
def flip_card(card, index):
    global first_card, second_card, failed_attempts, matched_pairs    #global to be able to access them outside the function

    #when I click a card it shows its text (number)
    if not card["text"]:  #If the card is not flipped yet --> flip
        card["text"] = cards[index]

        if first_card is None:  #If this is the first flipped card --> 
            first_card = (card, index)
            
        elif not second_card:  #If this is the second flipped card
            second_card = (card, index)
            
            #Check if the cards match
            if cards[first_card[1]] == cards[second_card[1]]:
                matched_pairs += 1
                first_card = None   #reset variables
                second_card = None

                if matched_pairs == num_pairs:  #if all the cards are matched
                    show_win_message()
                
            else:
                #If the cards don't match, flip again (with delay)
                window.after(500, reset_cards)
                failed_attempts += 1
                attempts.config(text=f"Failed attempts: {failed_attempts}")

#to reset cards if they don't match
def reset_cards():
    global first_card, second_card
    first_card[0]["text"] = ""  #Hide the first card again
    second_card[0]["text"] = ""  #Hide the second card again
    first_card = None
    second_card = None

def show_win_message():
    elapsed_time = int(time.time() - start_time)
    messagebox.showinfo("You Win!", f"Time: {elapsed_time} seconds\nFailed Attempts: {failed_attempts}")
    global game_started
    game_started = False
                

'''START SCREEN (button)'''
start_screen = tk.Frame(window) #create the window for the start button
start_button = tk.Button(start_screen, text="Start Game", command=start_game, font=("Helvetica", 14, "bold"), bg="lightblue")
start_button.pack(pady=20)
start_screen.pack()

game_screen = tk.Frame(window) #create the window for the game

'''RESTART BUTTON'''
restart_button = tk.Button(game_screen, text="Exit game", command=restart_game, font=("Helvetica", 14, "bold"), bg="purple")
restart_button.pack(pady=10)

'''LABELS (timer + attempts)'''
timer = tk.Label(game_screen, text="Time in seconds: 0s", font=("Helvetica", 14))
timer.pack(pady=10)

attempts = tk.Label(game_screen, text="Failed attempts: 0", font=("Helvetica", 14))
attempts.pack(pady=10)

frame = tk.Frame(game_screen)

#Create the buttons in a grid
grid_size = math.ceil(math.sqrt(num_cards))

for i in range(grid_size):
    for j in range(grid_size):
        index = i * grid_size + j
        if index < num_cards:
            button = tk.Button(frame, text="", width=8, height=4, state=tk.DISABLED) #cards cannot be click at first

        #Use a closure to capture the current button and index
        button.config(command=lambda b=button, idx=index: flip_card(b, idx))
        button.grid(row=i, column=j)
        buttons.append(button)

frame.pack(pady=20)
game_screen.pack_forget() 

#Run the main loop of the window
window.mainloop()
